import asyncio
import json
import logging
import os
import re
import shutil  # Used for finding executable and file operations
import subprocess
import sys     # For sys.exit
import shlex   # For quoting commands in logs
from contextlib import asynccontextmanager
from pathlib import Path
from typing import (Any, AsyncIterator, Dict, List, Optional, Set, Tuple,
                    Union)

# --- MCP Imports ---
try:
    from mcp.server.fastmcp import Context, FastMCP
except ImportError:
    sys.stderr.write(
        "CRITICAL: MCP SDK (FastMCP) not found. "
        "Please install it: pip install \"mcp[cli]\"\n"
    )
    sys.exit(1)
# --- End MCP Imports ---

# --- Logging Configuration ---
# Configure logging (level can be overridden by LOG_LEVEL env var)
log_level_str = os.environ.get("LOG_LEVEL", "INFO").upper()
numeric_level = getattr(logging, log_level_str, logging.INFO)
logging.basicConfig(
    level=numeric_level,
    format='%(asctime)s - %(levelname)-8s - %(name)-18s - [%(funcName)s:%(lineno)d] %(message)s'
)
log = logging.getLogger("ArduinoMCPServer")
# --- End Logging Configuration ---

# --- Fuzzy Search Import ---
try:
    from thefuzz import fuzz
    try:
        import Levenshtein  # noqa: F401
        FUZZY_ENABLED = True
        log.debug("Using thefuzz with python-Levenshtein for faster fuzzy search.")
    except ImportError:
        FUZZY_ENABLED = True
        log.warning(
            "Using thefuzz for fuzzy search. "
            "Install 'python-Levenshtein' for optimal performance: "
            "pip install python-Levenshtein"
        )
except ImportError:
    FUZZY_ENABLED = False
    log.warning(
        "Fuzzy search library 'thefuzz' not found. Fuzzy search in "
        "lib_search fallback disabled. Install it: pip install \"thefuzz[speedup]\""
    )
# --- End Fuzzy Search Import ---


# ==============================================================================
# Configuration & Constants
# ==============================================================================
USER_HOME: Path = Path.home()
SKETCHES_BASE_DIR: Path = USER_HOME / "Documents" / "Arduino_MCP_Sketches"
BUILD_TEMP_DIR: Path = SKETCHES_BASE_DIR / "_build_temp"
FUZZY_SEARCH_THRESHOLD: int = 75  # Minimum score (0-100) for fuzzy matches
DEFAULT_FQBN: str = "arduino:avr:uno" # Default FQBN for write_file auto-compile

# --- Arduino Directories Detection ---
ARDUINO_DATA_DIR: Path
ARDUINO_USER_DIR: Path = USER_HOME / "Documents" / "Arduino" # Standard user dir

if os.name == 'nt':  # Windows
    # %APPDATA% might not be set in all environments, try LOCALAPPDATA first
    localappdata = os.environ.get('LOCALAPPDATA')
    if localappdata:
        ARDUINO_DATA_DIR = Path(localappdata) / "Arduino15"
    else:
        # Fallback to older AppData location if LOCALAPPDATA isn't set
        appdata = os.environ.get('APPDATA')
        if appdata:
             ARDUINO_DATA_DIR = Path(appdata) / "Arduino15" # Less common now
        else:
             # Absolute fallback if no appdata vars found (unlikely)
             ARDUINO_DATA_DIR = USER_HOME / "AppData" / "Local" / "Arduino15"
             log.warning("Could not find LOCALAPPDATA or APPDATA env vars, guessing Arduino15 path.")
else:  # macOS, Linux
    # Default Linux/other path
    ARDUINO_DATA_DIR = USER_HOME / ".arduino15"
    # Check for standard macOS path
    macos_data_dir = USER_HOME / "Library" / "Arduino15"
    if macos_data_dir.is_dir():
        ARDUINO_DATA_DIR = macos_data_dir
        log.debug(f"Detected macOS Arduino data directory: {ARDUINO_DATA_DIR}")
    elif not ARDUINO_DATA_DIR.is_dir() and not macos_data_dir.exists(): # Only warn if neither exists
         log.warning(f"Default Arduino data directory ({ARDUINO_DATA_DIR}) or macOS path not found. "
                     "arduino-cli might use a different location or need initialization.")

# --- Arduino CLI Path Detection ---
_cli_path_override = os.environ.get("ARDUINO_CLI_PATH")
if _cli_path_override:
    ARDUINO_CLI_PATH = _cli_path_override
    log.info(f"Using arduino-cli path from environment variable: {ARDUINO_CLI_PATH}")
else:
    ARDUINO_CLI_PATH = "arduino-cli" # Default if not found
    # Add .exe for Windows check with shutil.which
    cli_executable_name = "arduino-cli.exe" if os.name == 'nt' else "arduino-cli"
    _cli_found_path = shutil.which(cli_executable_name)

    if _cli_found_path:
        ARDUINO_CLI_PATH = _cli_found_path
        log.debug(f"Found '{cli_executable_name}' via shutil.which: {ARDUINO_CLI_PATH}")
    else:
        log.debug(f"'{cli_executable_name}' not found via shutil.which, checking common paths...")
        # Common paths to check if 'which' fails
        common_paths_to_check = [
            # Unix paths
            "/opt/homebrew/bin/arduino-cli",    # macOS Homebrew (Apple Silicon)
            "/usr/local/bin/arduino-cli",       # macOS Homebrew (Intel), Linux manual install
            "/usr/bin/arduino-cli",             # Linux package manager
            str(USER_HOME / "bin" / "arduino-cli"), # User bin directory
            # Windows paths (adjust based on typical installations)
            "C:\\Program Files\\Arduino CLI\\arduino-cli.exe",
            "C:\\Program Files (x86)\\Arduino CLI\\arduino-cli.exe",
            str(USER_HOME / "AppData" / "Local" / "Programs" / "Arduino CLI" / "arduino-cli.exe"),
        ]
        for path_str in common_paths_to_check:
            path = Path(path_str)
            # On Windows, check for .exe specifically if needed, though Path should handle it
            if path.is_file() and os.access(path, os.X_OK):
                ARDUINO_CLI_PATH = str(path)
                log.debug(f"Found arduino-cli in common path: {ARDUINO_CLI_PATH}")
                break
        else: # Use default if not found in common paths either
             log.warning(
                 f"arduino-cli not found via 'which' or common paths. Using default "
                 f"'{ARDUINO_CLI_PATH}'. Ensure it's installed and accessible in PATH, "
                 "or set the ARDUINO_CLI_PATH environment variable."
             )

log.info(f"Configuration Loaded:")
log.info(f"  - User Home Dir    : {USER_HOME}")
log.info(f"  - Sketch Base Dir  : {SKETCHES_BASE_DIR}")
log.info(f"  - Build Temp Dir   : {BUILD_TEMP_DIR}")
log.info(f"  - Arduino Data Dir : {ARDUINO_DATA_DIR} (Exists: {ARDUINO_DATA_DIR.is_dir()})")
log.info(f"  - Arduino User Dir : {ARDUINO_USER_DIR} (Exists: {ARDUINO_USER_DIR.is_dir()})")
log.info(f"  - Arduino CLI Path : {ARDUINO_CLI_PATH}")
log.info(f"  - Default FQBN     : {DEFAULT_FQBN}")
log.info(f"  - Fuzzy Search     : {'Enabled' if FUZZY_ENABLED else 'Disabled'}")

# --- ANSI Escape Code Regex ---
ANSI_ESCAPE_RE = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
# ---

# ==============================================================================
# MCP Server Initialization
# ==============================================================================
mcp = FastMCP(
    "Arduino Tools",
    description=(
        "Tools for managing Arduino sketches (create, list, read, write with auto-compile), "
        "code verification (compile), uploading, libraries (search, install, examples), "
        "board discovery via arduino-cli, and basic file operations."
    ),
    dependencies=["mcp[cli]", "thefuzz[speedup]"] # Inform users of dependencies
)
# ==============================================================================
# Helper Functions
# ==============================================================================

async def _run_arduino_cli_command(
    cmd_args: List[str],
    check: bool = True,
    cwd: Optional[Path] = None
) -> Tuple[str, str, int]:
    """
    Helper to run arduino-cli commands asynchronously.

    Manages environment variables (DATA, USER, TMPDIR, HOME) required by arduino-cli.
    Handles stdout, stderr, return code, and raises specific exceptions on failure if check=True.

    Args:
        cmd_args: List of arguments to pass to arduino-cli (e.g., ['board', 'list']).
        check: If True, raise an Exception if the command returns a non-zero exit code.
        cwd: Optional Path object for the working directory.

    Returns:
        Tuple containing (stdout string, stderr string, return code).

    Raises:
        FileNotFoundError: If ARDUINO_CLI_PATH is not found or if the command output
                           indicates a missing file/library needed by the CLI itself.
        PermissionError: If execution permission is denied for CLI or related files/ports.
        ConnectionError: If upload fails due to port communication issues.
        TimeoutError: If upload times out.
        Exception: For other command failures when check=True.
    """
    full_cmd = [ARDUINO_CLI_PATH] + cmd_args
    env = os.environ.copy()
    # Ensure required directories are set for the CLI environment
    env["ARDUINO_DIRECTORIES_DATA"] = str(ARDUINO_DATA_DIR.resolve())
    env["ARDUINO_DIRECTORIES_USER"] = str(ARDUINO_USER_DIR.resolve())
    env['TMPDIR'] = str(BUILD_TEMP_DIR.resolve())
    env['HOME'] = str(USER_HOME.resolve()) # Some tools might need HOME

    effective_cwd_str = str(cwd.resolve()) if cwd else None
    cmd_str_for_log = ' '.join(shlex.quote(arg) for arg in full_cmd) # Use shlex.quote

    log.debug(f"Running Command : {cmd_str_for_log}")
    log.debug(f"  Environment   : DATA='{env['ARDUINO_DIRECTORIES_DATA']}', "
              f"USER='{env['ARDUINO_DIRECTORIES_USER']}', "
              f"TMPDIR='{env['TMPDIR']}', HOME='{env['HOME']}'")
    if effective_cwd_str:
        log.debug(f"  Working Dir   : {effective_cwd_str}")

    process = None
    try:
        # Set buffer limit for stdout/stderr (e.g., 10MB)
        buffer_limit = 10 * 1024 * 1024
        process = await asyncio.create_subprocess_exec(
            *full_cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            env=env,
            cwd=effective_cwd_str,
            limit=buffer_limit # Apply limit here
        )
        # Use communicate() for commands expected to finish relatively quickly
        # Add a timeout to prevent hangs if CLI gets stuck
        try:
            stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=300.0) # 5 min timeout
        except asyncio.TimeoutError:
             log.error(f"Command '{cmd_str_for_log}' timed out after 300 seconds.")
             if process and process.returncode is None: process.kill() # Force kill if timed out
             raise TimeoutError(f"Command '{cmd_str_for_log}' timed out.")

        # Ensure stdout/stderr are always strings, even if None
        stdout_str = stdout.decode(errors='replace').strip() if stdout else ""
        stderr_str = stderr.decode(errors='replace').strip() if stderr else ""
        return_code = process.returncode if process and process.returncode is not None else -1

        log_level = logging.DEBUG if return_code == 0 else logging.WARNING
        log.log(log_level, f"Command finished: Code={return_code}, Cmd='{cmd_str_for_log}'")
        if stdout_str:
            log.debug(f"Command STDOUT:\n---\n{stdout_str}\n---")
        if stderr_str:
            # Log stderr at WARNING level if command failed, DEBUG otherwise
            stderr_log_level = logging.WARNING if return_code != 0 else logging.DEBUG
            log.log(stderr_log_level, f"Command STDERR:\n---\n{stderr_str}\n---")

        if check and return_code != 0:
            error_message = stderr_str if stderr_str else stdout_str
            if not error_message: error_message = f"arduino-cli command failed with exit code {return_code} but produced no output."
            log.error(f"arduino-cli command failed! Code: {return_code}. Error: {error_message}")

            # Raise more specific errors based on common stderr messages
            error_lower = error_message.lower()
            if "no such file or directory" in error_lower:
                 # Distinguish between missing tool and missing sketch/lib file
                 if "bossac" in error_lower or "esptool" in error_lower or "dfu-util" in error_lower:
                     raise FileNotFoundError(f"Required uploader tool not found. Ensure platform core is installed ('arduino-cli core install ...'). Error: {error_message}")
                 else:
                     raise FileNotFoundError(f"File or directory not found. Check paths or required build artifacts. Error: {error_message}")
            if "library not found" in error_lower:
                 raise FileNotFoundError(f"Library not found. Use 'lib_search' and 'lib_install'. Error: {error_message}")
            if "permission denied" in error_lower or "access is denied" in error_lower:
                 raise PermissionError(f"Permission denied. Check user rights for files/ports. Error: {error_message}")
            if "no device found" in error_lower or "can't open device" in error_lower or "serial port not found" in error_lower:
                 raise ConnectionError(f"Device/port not found or cannot be opened. Check connection. Error: {error_message}")
            if "programmer is not responding" in error_lower or "timed out" in error_lower or "error resetting" in error_lower or "not in sync" in error_lower:
                 raise TimeoutError(f"Communication error with board. Check connection/board state. Error: {error_message}")

            # Generic exception for other failures
            raise Exception(f"arduino-cli command failed (code {return_code}): {error_message}")

        return stdout_str, stderr_str, return_code

    except FileNotFoundError as e:
        # Handle case where ARDUINO_CLI_PATH itself is not found
        if ARDUINO_CLI_PATH in str(e):
            error_msg = f"Command '{ARDUINO_CLI_PATH}' not found. Is arduino-cli installed and in PATH or correctly detected/configured via ARDUINO_CLI_PATH env var?"
            log.error(error_msg)
            raise FileNotFoundError(error_msg) from e
        else: # Re-raise specific FileNotFoundError from check block
            log.error(f"Command failed due to missing file/resource: {e}")
            raise e
    except PermissionError as e:
         # Re-raise specific PermissionError from check block
         log.error(f"Command failed due to permissions: {e}")
         raise e
    except ConnectionError as e:
         log.error(f"Command failed due to connection error: {e}")
         raise e
    except TimeoutError as e:
         log.error(f"Command failed due to timeout/communication error: {e}")
         raise e
    except Exception as e:
        # Catch generic Exception from check block or unexpected errors
        if isinstance(e, Exception) and e.args and "arduino-cli command failed" in str(e.args[0]):
            log.error(f"Caught specific command failure: {e}")
            raise e # Re-raise the specific exception from the check block
        error_msg = f"Unexpected error running command '{cmd_str_for_log}': {type(e).__name__}: {e}"
        log.exception(error_msg) # Log with traceback
        raise Exception(error_msg) from e
    finally:
        # Ensure process is cleaned up if it exists and hasn't finished
        if process and process.returncode is None:
            log.warning(f"Command process '{cmd_str_for_log}' did not exit cleanly, attempting termination.")
            try:
                process.terminate()
                await asyncio.wait_for(process.wait(), timeout=2.0)
            except asyncio.TimeoutError:
                log.error(f"Process '{cmd_str_for_log}' did not terminate after 2s, sending kill signal.")
                try:
                    process.kill()
                    await asyncio.sleep(0.1) # Short pause after kill
                except ProcessLookupError: pass # Already gone
                except Exception as kill_err: log.error(f"Error killing process: {kill_err}")
            except ProcessLookupError:
                log.debug("Process already terminated.") # Process finished between check and terminate
            except Exception as term_err:
                log.error(f"Error during process termination: {term_err}")

# --- Synchronous File I/O Helpers (Run in Executor Thread) ---
# These helpers ensure blocking file I/O doesn't block the asyncio event loop.

async def _async_file_op(func, *args, **kwargs):
    """Runs a synchronous function in a thread pool."""
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, func, *args, **kwargs)

def _sync_write_file(filepath: Path, content: str, encoding: str = "utf-8"):
    """Synchronously writes content to a file."""
    log.debug(f"Executing sync write to: {filepath}")
    try:
        filepath.parent.mkdir(parents=True, exist_ok=True)
        filepath.write_text(content, encoding=encoding)
        log.debug(f"Sync write successful: {filepath}")
    except OSError as e:
        log.error(f"Sync write failed for {filepath}: {e}")
        raise # Re-raise to be caught by the async wrapper

def _sync_read_file(filepath: Path, encoding: str = "utf-8") -> str:
    """Synchronously reads content from a file."""
    log.debug(f"Executing sync read from: {filepath}")
    try:
        content = filepath.read_text(encoding=encoding)
        log.debug(f"Sync read successful: {filepath} ({len(content)} chars)")
        return content
    except FileNotFoundError:
        log.warning(f"Sync read failed: File not found at {filepath}")
        raise
    except OSError as e:
        log.error(f"Sync read failed for {filepath}: {e}")
        raise

def _sync_rename_file(old_path: Path, new_path: Path):
    """Synchronously renames/moves a file or directory."""
    log.debug(f"Executing sync rename from {old_path} to {new_path}")
    try:
        # Ensure target directory exists if moving across directories
        new_path.parent.mkdir(parents=True, exist_ok=True)
        old_path.rename(new_path)
        log.debug(f"Sync rename successful: {old_path} -> {new_path}")
    except OSError as e:
        log.error(f"Sync rename failed for {old_path} -> {new_path}: {e}")
        raise

def _sync_check_exists(path: Path) -> Tuple[bool, bool, bool]:
    """Synchronously checks if a path exists and its type."""
    exists = path.exists()
    is_file = path.is_file() if exists else False
    is_dir = path.is_dir() if exists else False
    log.debug(f"Sync check exists for {path}: exists={exists}, is_file={is_file}, is_dir={is_dir}")
    return exists, is_file, is_dir

def _sync_list_dir(dir_path: Path) -> List[str]:
    """Synchronously lists items in a directory."""
    log.debug(f"Executing sync listdir for: {dir_path}")
    try:
        return [item.name for item in dir_path.iterdir()]
    except FileNotFoundError:
        log.warning(f"Sync listdir failed: Directory not found at {dir_path}")
        raise
    except OSError as e:
        log.error(f"Sync listdir failed for {dir_path}: {e}")
        raise

def _sync_mkdir(dir_path: Path):
    """Synchronously creates a directory, including parents."""
    log.debug(f"Executing sync mkdir for: {dir_path}")
    try:
        dir_path.mkdir(parents=True, exist_ok=True)
        log.debug(f"Sync mkdir successful: {dir_path}")
    except OSError as e:
        log.error(f"Sync mkdir failed for {dir_path}: {e}")
        raise

def _sync_remove_file(filepath: Path):
    """Synchronously removes a file."""
    log.debug(f"Executing sync remove file: {filepath}")
    try:
        filepath.unlink(missing_ok=False) # Raise error if not found
        log.debug(f"Sync remove file successful: {filepath}")
    except IsADirectoryError:
        log.error(f"Sync remove file failed: Path is a directory: {filepath}")
        raise
    except FileNotFoundError:
        log.error(f"Sync remove file failed: File not found: {filepath}")
        raise
    except PermissionError:
        log.error(f"Sync remove file failed: Permission denied for {filepath}")
        raise
    except OSError as e:
        log.error(f"Sync remove file failed for {filepath}: {e}")
        raise
# --- End Synchronous Helpers ---

# --- Path Validation Helper ---
async def _resolve_and_validate_path(
    filepath_str: str,
    allowed_bases: Optional[List[Path]] = None,
    check_existence: bool = False # Only resolve, don't check if it exists yet
) -> Path:
    """
    Resolves a user-provided path string and validates it against allowed base directories.

    Args:
        filepath_str: The path string (can contain '~').
        allowed_bases: A list of Path objects. The resolved path must be within one of these bases.
                       Defaults to [USER_HOME]. Provide an empty list or None to allow any path
                       (USE WITH EXTREME CAUTION).
        check_existence: If True, raises FileNotFoundError if the resolved path doesn't exist.

    Returns:
        The resolved, absolute Path object.

    Raises:
        ValueError: If the path string is invalid or cannot be resolved.
        PermissionError: If the resolved path is outside all allowed_bases or targets
                         potentially sensitive system directories.
        FileNotFoundError: If check_existence is True and the path does not exist.
    """
    if not filepath_str:
        raise ValueError("File path cannot be empty.")

    try:
        # Expand ~ and resolve to absolute path
        if "~" in filepath_str:
            expanded_path = Path(filepath_str).expanduser()
        else:
            expanded_path = Path(filepath_str)

        # Resolve symbolic links and make absolute
        # Use strict=False initially to allow resolving paths that might not exist yet (for write/rename)
        resolved_path = expanded_path.resolve(strict=False)

    except Exception as e:
        log.error(f"Failed to resolve path '{filepath_str}': {e}")
        raise ValueError(f"Invalid path specified: '{filepath_str}'. Error: {e}") from e

    # Determine the set of allowed base paths
    effective_allowed_bases: List[Path]
    if allowed_bases is None: # Default to USER_HOME if None is explicitly passed
         effective_allowed_bases = [USER_HOME.resolve(strict=False)]
    else:
         effective_allowed_bases = [p.resolve(strict=False) for p in allowed_bases]


    # --- Security Checks ---
    # 1. Check against explicitly restricted system directories
    restricted_starts_unix = ["/etc", "/bin", "/sbin", "/usr/bin", "/usr/sbin", "/System", "/dev", "/proc"]
    restricted_starts_win = ["c:\\windows", "c:/windows"] # Add other drives if needed
    restricted_starts = restricted_starts_unix + restricted_starts_win

    resolved_path_str_lower = str(resolved_path).lower()
    for restricted in restricted_starts:
        # Allow access if an allowed_base *is* or *is within* the restricted path
        is_exception_allowed = any(
            str(base).lower().startswith(restricted) or restricted.startswith(str(base).lower())
            for base in effective_allowed_bases
        )
        if resolved_path_str_lower.startswith(restricted) and not is_exception_allowed:
            log.error(f"Attempted access to restricted system directory: {resolved_path}")
            raise PermissionError(f"Access to potentially sensitive system directory '{resolved_path}' is restricted.")

    # 2. Check if path is within any of the allowed base directories
    if effective_allowed_bases: # Only check if bases are specified
        is_within_allowed = False
        for base in effective_allowed_bases:
            try:
                # Use is_relative_to for robust check (requires Python 3.9+)
                # Check both ways in case base itself is the target
                if resolved_path == base or resolved_path.is_relative_to(base):
                    is_within_allowed = True
                    break
            except (ValueError, AttributeError): # Handle different drives (Win) or older Python
                 try:
                      common = os.path.commonpath([str(base), str(resolved_path)])
                      if common == str(base):
                          is_within_allowed = True
                          break
                 except ValueError: # Handles case where paths have no common prefix (e.g. different drives)
                      continue


        if not is_within_allowed:
            allowed_strs = ', '.join(f"'{str(p)}'" for p in effective_allowed_bases)
            log.error(f"Path validation failed: '{resolved_path}' is outside allowed bases: {allowed_strs}")
            raise PermissionError(f"Path '{filepath_str}' resolves to '{resolved_path}', which is outside the allowed base directories: {allowed_strs}.")

    log.debug(f"Resolved path '{filepath_str}' to '{resolved_path}' (Allowed within: {effective_allowed_bases or 'Anywhere'})")

    # 3. Optional existence check
    if check_existence:
         exists, _, _ = await _async_file_op(_sync_check_exists, resolved_path)
         if not exists:
             raise FileNotFoundError(f"Path does not exist: {resolved_path}")

    return resolved_path
# --- End Path Validation Helper ---

# --- Compile Execution & Output Parsing Helper ---
def _parse_compile_output(stdout_str: str, stderr_str: str) -> str:
    """Parses arduino-cli compile output for sketch size and RAM usage."""
    size_info = ""
    # Combine outputs as size info might be in either stdout or stderr
    combined_output = stdout_str + "\n" + stderr_str

    # Regex patterns (case-insensitive, multiline)
    # Sketch uses 1084 bytes (5%) of program storage space. Maximum is 20480 bytes.
    sketch_size_match = re.search(
        r"Sketch uses\s+(\d+)\s+bytes.*?maximum is\s+(\d+)",
        combined_output, re.IGNORECASE | re.DOTALL
    )
    # Global variables use 9 bytes (0%) of dynamic memory, leaving 2039 bytes for local variables. Maximum is 2048 bytes.
    ram_size_match = re.search(
        r"Global variables use\s+(\d+)\s+bytes.*?maximum is\s+(\d+)",
        combined_output, re.IGNORECASE | re.DOTALL
    )

    if sketch_size_match:
        try:
            used_s, max_s = int(sketch_size_match.group(1)), int(sketch_size_match.group(2))
            percent_s = (used_s / max_s * 100) if max_s > 0 else 0
            size_info += f" Program storage: {used_s} / {max_s} bytes ({percent_s:.1f}%)."
        except (ValueError, ZeroDivisionError, IndexError):
            log.warning("Could not parse sketch size numbers from compile output.")

    if ram_size_match:
         try:
             used_r, max_r = int(ram_size_match.group(1)), int(ram_size_match.group(2))
             percent_r = (used_r / max_r * 100) if max_r > 0 else 0
             size_info += f" Dynamic memory: {used_r} / {max_r} bytes ({percent_r:.1f}%)."
         except (ValueError, ZeroDivisionError, IndexError):
             log.warning("Could not parse RAM size numbers from compile output.")

    return size_info.strip()

async def _execute_compile(sketch_path_abs: Path, build_path_abs: Path, board_fqbn: str) -> str:
    """Executes the arduino-cli compile command and returns success message with size info."""
    log.info(f"Executing compilation: Sketch='{sketch_path_abs.name}', FQBN='{board_fqbn}', BuildPath='{build_path_abs}'")
    await _async_file_op(_sync_mkdir, build_path_abs) # Ensure build path exists

    cmd_args = [
        "compile",
        "--fqbn", board_fqbn,
        "--verbose", # Get detailed output for parsing size
        "--build-path", str(build_path_abs),
        str(sketch_path_abs) # Path to the sketch directory
    ]
    cmd_str_for_log = ' '.join(shlex.quote(arg) for arg in cmd_args) # Use shlex.quote
    log.info(f"Compile Command: arduino-cli {cmd_str_for_log}")

    try:
        stdout_str, stderr_str, _ = await _run_arduino_cli_command(cmd_args, check=True)
        size_info = _parse_compile_output(stdout_str, stderr_str)
        success_message = f"Compilation successful.{' ' + size_info if size_info else ''}"
        log.info(f"Compilation successful for '{sketch_path_abs.name}'.{(' ' + size_info) if size_info else ''}")
        return success_message
    except (FileNotFoundError, PermissionError, ValueError, Exception) as e:
        # Errors like FileNotFoundError (missing core), PermissionError,
        # or generic Exception (compile errors) are caught by _run_arduino_cli_command
        log.error(f"Compilation failed for '{sketch_path_abs.name}' with FQBN '{board_fqbn}': {e}")
        # Re-raise the specific error caught by the helper
        raise Exception(f"Compilation failed: {e}") from e

# --- Board Info Helper ---
async def _fetch_and_format_board_info(port_address: str, board_name: str, fqbn: str) -> str:
    """Helper to fetch platform libs for a board and format its output string."""
    platform_libraries: Dict[str, List[str]] = {}
    lib_cmd_args = ["lib", "list", "-b", fqbn, "--format", "json"]
    log.debug(f"Fetching platform libraries for FQBN '{fqbn}'")
    try:
        # Run command, don't check=True as failure here is non-critical for board listing
        lib_stdout, lib_stderr, lib_retcode = await _run_arduino_cli_command(lib_cmd_args, check=False)

        if lib_retcode == 0 and lib_stdout:
            try:
                lib_data = json.loads(lib_stdout)
                # Handle potential variations in JSON structure
                installed_libs_outer = lib_data.get("libraries", lib_data.get("installed_libraries"))
                if isinstance(installed_libs_outer, list):
                    for lib_item in installed_libs_outer:
                         # Handle nested 'library' key if present
                         lib_details = lib_item.get("library", lib_item)
                         if isinstance(lib_details, dict) and lib_details.get("location") == "platform":
                             lib_name = lib_details.get("name")
                             provides_includes = lib_details.get("provides_includes", [])
                             if lib_name and isinstance(provides_includes, list):
                                 platform_libraries[lib_name] = provides_includes
                    log.debug(f"Found {len(platform_libraries)} platform libraries for {fqbn}")
                else:
                    log.warning(f"Unexpected format for 'libraries'/'installed_libraries' in JSON for FQBN '{fqbn}'.")
            except json.JSONDecodeError as json_e:
                log.warning(f"Failed to decode lib list JSON for FQBN '{fqbn}'. Error: {json_e}. Raw: {lib_stdout[:200]}...")
            except Exception as parse_e:
                log.warning(f"Error parsing lib list JSON for FQBN '{fqbn}'. Error: {parse_e}")
        elif lib_retcode != 0:
            log.warning(f"Failed to list libs for FQBN '{fqbn}'. Exit: {lib_retcode}. Stderr: {lib_stderr}")

    except Exception as fetch_err:
        log.error(f"Error fetching libraries for FQBN '{fqbn}': {fetch_err}")

    # Format the output string
    line = f"- Port: {port_address}, Board: {board_name}, FQBN: {fqbn}"
    if platform_libraries:
        line += "\n    Platform Libraries:"
        for lib_name, includes in sorted(platform_libraries.items()):
            include_str = ", ".join(includes) if includes else "(no includes listed)"
            line += f"\n      - {lib_name} (Includes: {include_str})"
    else:
        line += "\n    Platform Libraries: (None found or error fetching)"
    return line
# --- End Board Info Helper ---


# ==============================================================================
# MCP Tool Definitions
# ==============================================================================

@mcp.tool()
async def create_new_sketch(sketch_name: str) -> str:
    """
    Creates a new Arduino sketch directory and .ino file with the given name
    inside the designated sketches directory ('~/Documents/Arduino_MCP_Sketches/').
    The sketch name must be a valid directory name and cannot contain path separators.
    If a directory or file with that name already exists, it returns an error.

    Args:
        sketch_name: The desired name for the sketch (e.g., 'MyBlink').
                     Cannot be empty or contain '/', '\\', or '..'.

    Returns:
        Success message indicating the absolute path of the created sketch directory.

    Raises:
        ValueError: If sketch_name is invalid.
        FileExistsError: If a file or directory with that name already exists.
        PermissionError: If directory creation fails due to permissions.
        Exception: For other errors during creation reported by arduino-cli.
    """
    log.info(f"Tool Call: create_new_sketch(sketch_name='{sketch_name}')")
    # Basic name validation
    if not sketch_name or any(c in sketch_name for c in ['/', '\\']) or ".." in sketch_name:
         raise ValueError("Invalid sketch_name. Cannot be empty, contain path separators ('/', '\\'), or '..'.")

    sketch_dir = SKETCHES_BASE_DIR / sketch_name
    # Resolve *before* checking existence to get the final intended path
    sketch_dir_abs = sketch_dir.resolve(strict=False)

    # Check if path exists using our async helper
    exists, _, _ = await _async_file_op(_sync_check_exists, sketch_dir_abs)
    if exists:
        error_msg = f"Failed to create sketch: Path '{sketch_dir_abs}' already exists."
        log.error(error_msg)
        raise FileExistsError(error_msg)

    # Use the absolute path for the arduino-cli command
    cmd_args = ["sketch", "new", str(sketch_dir_abs)]
    try:
        # Run the command, check=True will raise specific errors on failure
        await _run_arduino_cli_command(cmd_args, check=True)
        success_message = f"Successfully created sketch '{sketch_name}' at '{sketch_dir_abs}'."
        log.info(success_message)
        return success_message
    except (FileExistsError, PermissionError, ValueError) as e:
        # Re-raise specific errors if they occurred during validation or execution
        log.error(f"Sketch creation failed for '{sketch_name}': {e}")
        raise e
    except Exception as e:
        # Catch generic exceptions from _run_arduino_cli_command or other issues
        log.error(f"Unexpected error creating sketch '{sketch_name}' at {sketch_dir_abs}: {e}")
        # Attempt cleanup only if the directory was likely created by the failed command
        try:
            if sketch_dir_abs.is_dir() and not any(sketch_dir_abs.iterdir()):
                log.warning(f"Attempting cleanup of empty sketch directory created during failed attempt: {sketch_dir_abs}")
                await _async_file_op(sketch_dir_abs.rmdir)
        except Exception as cleanup_err:
            log.warning(f"Cleanup failed for {sketch_dir_abs}: {cleanup_err}")
        raise Exception(f"Failed to create sketch '{sketch_name}': {e}") from e


@mcp.tool()
async def list_sketches() -> str:
    """
    Lists all valid Arduino sketches found within the designated sketches directory
    ('~/Documents/Arduino_MCP_Sketches/'). A valid sketch is defined as a directory
    containing an '.ino' file that shares the same base name as the directory.
    Excludes hidden files/directories and the build temp directory.

    Returns:
        A string listing the names of valid sketches, or a message indicating none were found
        or the base directory doesn't exist.

    Raises:
        Exception: If there's an error reading the sketches directory.
    """
    log.info(f"Tool Call: list_sketches (in '{SKETCHES_BASE_DIR}')")
    base_exists, _, base_is_dir = await _async_file_op(_sync_check_exists, SKETCHES_BASE_DIR)

    if not base_exists:
        log.warning(f"Sketch base directory '{SKETCHES_BASE_DIR}' not found.")
        return f"Sketch base directory '{SKETCHES_BASE_DIR}' not found."
    if not base_is_dir:
        log.error(f"Path '{SKETCHES_BASE_DIR}' exists but is not a directory.")
        return f"Error: Path '{SKETCHES_BASE_DIR}' is not a directory."

    try:
        items = await _async_file_op(_sync_list_dir, SKETCHES_BASE_DIR)
    except Exception as e:
        log.error(f"Error listing directory '{SKETCHES_BASE_DIR}': {e}")
        raise Exception(f"Error listing sketches directory: {e}") from e

    # Asynchronously check each item to see if it's a valid sketch directory
    async def check_item_is_sketch(item_name: str) -> Optional[str]:
        if item_name.startswith('.') or item_name == BUILD_TEMP_DIR.name:
            return None # Skip hidden items and build dir

        item_path = SKETCHES_BASE_DIR / item_name
        # Check if it's a directory
        exists, _, is_dir = await _async_file_op(_sync_check_exists, item_path)
        if not (exists and is_dir):
            return None

        # Check if the corresponding .ino file exists inside
        sketch_file_path = item_path / f"{item_name}.ino"
        file_exists, is_file, _ = await _async_file_op(_sync_check_exists, sketch_file_path)
        if file_exists and is_file:
            return item_name # It's a valid sketch

        return None

    # Run checks concurrently
    results = await asyncio.gather(*(check_item_is_sketch(item) for item in items))

    # Filter out None results and sort
    valid_sketches = sorted([name for name in results if name is not None])

    if not valid_sketches:
        log.info(f"No valid sketches found in '{SKETCHES_BASE_DIR}'.")
        return f"No valid sketches found in '{SKETCHES_BASE_DIR}'."

    log.info(f"Found {len(valid_sketches)} valid sketches.")
    return "Available sketches:\n" + "\n".join(f"- {sketch}" for sketch in valid_sketches)


@mcp.tool()
async def list_boards() -> str:
    """
    Lists connected Arduino boards detected by 'arduino-cli board list'.
    Provides Port, Board Name, and the crucial Fully Qualified Board Name (FQBN)
    needed for verification and uploading. Also attempts to list associated
    platform libraries for each detected board for additional context.

    Returns:
        A formatted string listing detected boards with their details and platform libraries,
        or a message indicating no boards were detected or an error occurred.

    Raises:
        Exception: If the 'arduino-cli board list' command fails unexpectedly or
                   if the JSON output cannot be parsed.
    """
    log.info("Tool Call: list_boards")
    board_list_cmd_args = ["board", "list", "--format", "json"]
    try:
        # Run command, don't check=True initially to handle "no boards found" gracefully
        board_list_json, board_list_stderr, board_list_retcode = await _run_arduino_cli_command(
            board_list_cmd_args, check=False
        )

        # Handle cases where the command might succeed but return empty or indicate no boards
        if board_list_retcode == 0 and not board_list_json.strip():
            log.info("arduino-cli board list returned success but empty JSON output.")
            return "No connected Arduino boards detected (Command succeeded, but no boards found)."

        # Handle explicit "no boards found" messages even if retcode is 0 or non-zero
        combined_output_lower = (board_list_json + board_list_stderr).lower()
        if "no boards found" in combined_output_lower or "could not find any board" in combined_output_lower:
            log.info("arduino-cli board list reported no boards found.")
            return "No connected Arduino boards detected."

        # If retcode is non-zero and it wasn't a "no boards" message, raise error
        if board_list_retcode != 0:
            raise Exception(f"arduino-cli board list failed (code {board_list_retcode}): {board_list_stderr or board_list_json}")

        # Proceed with JSON parsing if command succeeded and output is not empty
        try:
            boards_data = json.loads(board_list_json)
        except json.JSONDecodeError as e:
            log.error(f"Error decoding JSON from 'board list': {e}. Raw: {board_list_json[:500]}...")
            raise Exception(f"Error decoding JSON from 'board list': {e}") from e

        # Parse the potentially varied JSON structure
        ports_list = []
        if isinstance(boards_data, dict):
            ports_list = boards_data.get("detected_ports", []) # Newer format
        elif isinstance(boards_data, list):
            ports_list = boards_data # Older format
        else:
            log.error(f"Could not parse board list output (unexpected JSON root type): {board_list_json[:500]}...")
            raise Exception("Could not parse board list output (unexpected JSON root type).")

        if not isinstance(ports_list, list):
            log.error(f"Could not parse board list output (expected list of ports): {board_list_json[:500]}...")
            raise Exception("Could not parse board list output (expected list of ports).")

        # Create tasks to fetch library info for each board concurrently
        tasks = []
        for port_info in ports_list:
             if not isinstance(port_info, dict): continue
             port_details = port_info.get("port", {})
             if not isinstance(port_details, dict): continue
             port_address = port_details.get("address")

             # Handle different keys for board info ('matching_boards' vs 'boards')
             matching_boards = port_info.get("matching_boards", port_info.get("boards", []))

             if port_address and isinstance(matching_boards, list):
                 for board in matching_boards:
                     if isinstance(board, dict) and board.get("fqbn"):
                         fqbn = board["fqbn"]
                         board_name = board.get("name", "Unknown Board")
                         # Schedule the helper function call
                         tasks.append(_fetch_and_format_board_info(port_address, board_name, fqbn))

        # Gather results from library fetching tasks
        detected_boards_info = []
        if tasks:
            detected_boards_info = await asyncio.gather(*tasks)

        # Format final output
        if not detected_boards_info:
            ports_without_boards = [
                p.get("port", {}).get("address") for p in ports_list
                if p.get("port", {}).get("address") and not p.get("matching_boards") and not p.get("boards")
            ]
            if ports_without_boards:
                return f"No connected boards with recognized FQBN detected.\nFound ports without recognized boards: {', '.join(ports_without_boards)}"
            else:
                return "No connected Arduino boards with recognized FQBN detected."

        output_lines = ["Detected Arduino Boards:"]
        output_lines.extend(detected_boards_info)
        formatted_output = "\n".join(output_lines).strip()
        log.info(f"Detected boards (summary):\n{formatted_output}") # Log summary
        return formatted_output

    except Exception as e:
        log.exception("Error during list_boards execution.")
        # Avoid leaking raw internal errors directly if possible
        raise Exception(f"Failed to list boards: {type(e).__name__}") from e


@mcp.tool()
async def verify_code(sketch_name: str, board_fqbn: str) -> str:
    """
    Verifies (compiles) the specified Arduino sketch for the given board FQBN
    to check for errors, without uploading.

    Args:
        sketch_name: Name of the sketch directory within '~/Documents/Arduino_MCP_Sketches/'.
                     Must be a valid directory name (no path separators).
        board_fqbn: The Fully Qualified Board Name identifying the target board hardware
                    (e.g., 'arduino:avr:uno', 'arduino:renesas_uno:unor4wifi').
                    Format must be 'vendor:arch:board'. Use 'list_boards' or 'board_search'.

    Returns:
        Success message including compilation stats (program storage, dynamic memory usage),
        or raises an error if verification fails.

    Raises:
        ValueError: If sketch_name or board_fqbn is invalid or badly formatted.
        FileNotFoundError: If the sketch directory, main .ino file, or required
                           cores/tools are not found.
        PermissionError: If there are permission issues accessing files.
        Exception: For compilation errors reported by arduino-cli or other issues.
    """
    log.info(f"Tool Call: verify_code(sketch='{sketch_name}', fqbn='{board_fqbn}')")
    if not sketch_name or any(c in sketch_name for c in ['/', '\\']) or ".." in sketch_name:
        raise ValueError("Invalid sketch_name. Cannot be empty or contain path separators or '..'.")
    if not board_fqbn or ":" not in board_fqbn or len(board_fqbn.split(':')) < 3:
        raise ValueError("Invalid or missing board_fqbn. Format must be 'vendor:arch:board'. Use list_boards or board_search.")

    sketch_dir = SKETCHES_BASE_DIR / sketch_name
    # Resolve first to ensure we have the absolute path for checks and commands
    sketch_path_abs = sketch_dir.resolve(strict=False)
    build_path_abs = (BUILD_TEMP_DIR / f"{sketch_name}_verify_{board_fqbn.replace(':', '_')}").resolve(strict=False)

    # Check sketch directory existence
    exists, _, is_dir = await _async_file_op(_sync_check_exists, sketch_path_abs)
    if not exists or not is_dir:
         raise FileNotFoundError(f"Sketch directory not found or is not a directory: {sketch_path_abs}")

    # Check main .ino file existence
    main_ino_file = sketch_path_abs / f"{sketch_name}.ino"
    ino_exists, is_file, _ = await _async_file_op(_sync_check_exists, main_ino_file)
    if not ino_exists or not is_file:
         raise FileNotFoundError(f"Main sketch file '{main_ino_file.name}' not found or is not a file in {sketch_path_abs}")

    try:
        # _execute_compile handles mkdir for build_path_abs
        compile_message = await _execute_compile(sketch_path_abs, build_path_abs, board_fqbn)
        # compile_message already contains "Compilation successful." prefix
        success_message = f"Verification successful for sketch '{sketch_name}'.{compile_message.replace('Compilation successful.', '')}"
        log.info(success_message)
        return success_message
    except (FileNotFoundError, PermissionError, ValueError, Exception) as e:
        # Specific errors raised by _execute_compile or _run_arduino_cli_command
        log.error(f"Verification failed for sketch '{sketch_name}' with FQBN '{board_fqbn}': {e}")
        # Re-raise the original specific error for clarity
        raise Exception(f"Verification failed for sketch '{sketch_name}': {e}") from e


@mcp.tool()
async def upload_sketch(sketch_name: str, port: str, board_fqbn: str) -> str:
    """
    Verifies (compiles) AND uploads the specified sketch to the Arduino board
    connected to the given serial port, using the specified FQBN.

    Args:
        sketch_name: Name of the sketch directory within '~/Documents/Arduino_MCP_Sketches/'.
                     Must be a valid directory name.
        port: The serial port address of the target board (e.g., '/dev/ttyACM0', 'COM3').
              Use 'list_boards' to find the correct port. Cannot be empty.
        board_fqbn: The Fully Qualified Board Name identifying the target board hardware
                    (e.g., 'arduino:avr:uno', 'arduino:renesas_uno:unor4wifi').
                    Format must be 'vendor:arch:board'. Use 'list_boards' or 'board_search'. MANDATORY.

    Returns:
        Success message confirming the upload, potentially including compilation stats.

    Raises:
        ValueError: If any argument is invalid (empty, bad format).
        FileNotFoundError: If the sketch directory, main .ino file, or required
                           cores/tools/uploaders are not found.
        PermissionError: If there are permission issues accessing the port or files.
        ConnectionError: If the board cannot be found or communicated with on the specified port.
        TimeoutError: If communication with the board times out during upload.
        Exception: For compilation errors or other upload issues reported by arduino-cli.
    """
    log.info(f"Tool Call: upload_sketch(sketch='{sketch_name}', port='{port}', fqbn='{board_fqbn}')")
    # Input validation
    if not sketch_name or any(c in sketch_name for c in ['/', '\\']) or ".." in sketch_name:
        raise ValueError("Invalid sketch_name. Cannot be empty or contain path separators or '..'.")
    if not port:
        raise ValueError("Serial port must be specified.")
    if not board_fqbn or ":" not in board_fqbn or len(board_fqbn.split(':')) < 3:
        raise ValueError("Invalid or missing board_fqbn. Format must be 'vendor:arch:board'.")

    sketch_dir = SKETCHES_BASE_DIR / sketch_name
    sketch_path_abs = sketch_dir.resolve(strict=False)
    # Use a consistent build path per sketch/FQBN for potential caching by CLI
    build_path_abs = (BUILD_TEMP_DIR / f"{sketch_name}_upload_{board_fqbn.replace(':', '_')}").resolve(strict=False)

    # Check sketch directory and main file existence
    exists, _, is_dir = await _async_file_op(_sync_check_exists, sketch_path_abs)
    if not exists or not is_dir:
        raise FileNotFoundError(f"Sketch directory not found or is not a directory: {sketch_path_abs}")
    main_ino_file = sketch_path_abs / f"{sketch_name}.ino"
    ino_exists, is_file, _ = await _async_file_op(_sync_check_exists, main_ino_file)
    if not ino_exists or not is_file:
        raise FileNotFoundError(f"Main sketch file '{main_ino_file.name}' not found or is not a file in {sketch_path_abs}")

    try:
        # Ensure build directory exists (handled within _execute_compile now)
        # log.info(f"Using build path: {build_path_abs}")

        # --- Step 1: Compile ---
        log.info("Starting verification (compilation) step before upload...")
        compile_message = await _execute_compile(sketch_path_abs, build_path_abs, board_fqbn)
        log.info(f"Verification successful. {compile_message.replace('Compilation successful.', '').strip()}") # Log size info

        # --- Step 2: Upload ---
        log.info("Starting upload step...")
        cmd_args_upload = [
            "upload",
            "--port", port,
            "--fqbn", board_fqbn,
            "--verbose", # Useful for debugging upload issues
            "--build-path", str(build_path_abs), # Reuse build path
            str(sketch_path_abs) # Path to sketch directory
        ]
        cmd_str_for_log = ' '.join(shlex.quote(arg) for arg in cmd_args_upload) # Use shlex.quote
        log.info(f"Upload Command: arduino-cli {cmd_str_for_log}")

        # Run upload command, check=True will raise specific errors on failure
        upload_stdout, upload_stderr, _ = await _run_arduino_cli_command(cmd_args_upload, check=True)

        # Construct success message
        success_message = f"Successfully uploaded sketch '{sketch_name}' to board '{board_fqbn}' on port '{port}'."
        # Optionally add compile stats back if desired
        # success_message += compile_message.replace('Compilation successful.', '').strip()

        # Check output for common success indicators (optional, as check=True handles failure)
        combined_output = (upload_stdout + "\n" + upload_stderr).lower()
        success_indicators = ["leaving...", "hard resetting via", "done uploading", "upload successful", "verify successful", "bytes written"]
        if any(indicator in combined_output for indicator in success_indicators):
            log.info(success_message)
        else:
            # This case is less likely if check=True worked, but good for logging
            log.warning(f"{success_message} (Standard confirmation message not found in output; verify on device). Output:\n{upload_stdout}\n{upload_stderr}")

        return success_message

    except (FileNotFoundError, PermissionError, ValueError, ConnectionError, TimeoutError, Exception) as e:
        # Catch specific errors raised by _execute_compile or _run_arduino_cli_command
        log.error(f"Upload process failed for sketch '{sketch_name}': {e}")
        # Re-raise the specific error for better feedback
        raise Exception(f"Upload failed for sketch '{sketch_name}': {e}") from e


@mcp.tool()
async def board_search(board_name_query: str) -> str:
    """
    Searches the online Arduino board index for boards matching the query.
    Useful for finding the correct FQBN (Fully Qualified Board Name) for a board
    that is not currently connected or detected by 'list_boards'.

    Args:
        board_name_query: A partial or full name of the board to search for
                          (e.g., "uno r4 wifi", "esp32", "seeed xiao").

    Returns:
        A string listing matching boards and their FQBNs, or a message indicating
        no matches were found or an error occurred.

    Raises:
        ValueError: If board_name_query is empty.
        Exception: If the search command fails unexpectedly.
    """
    log.info(f"Tool Call: board_search(query='{board_name_query}')")
    if not board_name_query:
        raise ValueError("Board name query cannot be empty.")

    cmd_args = ["board", "search", board_name_query]
    try:
        # Don't check=True initially to handle "no boards found"
        stdout, stderr, retcode = await _run_arduino_cli_command(cmd_args, check=False)
        output = (stdout or stderr).strip() # Combine output, prefer stdout
        output_lower = output.lower()

        if retcode != 0 or not output or "no boards found" in output_lower or "no matching board" in output_lower:
             log.info(f"Board search for '{board_name_query}' found no results or failed (Code: {retcode}). Output: {output}")
             return f"No boards found matching '{board_name_query}' in the online index."

        log.info(f"Board search results for '{board_name_query}':\n{output}")
        # Return the raw output from the CLI as it's usually well-formatted
        return output

    except Exception as e:
        log.exception(f"Board search failed unexpectedly for query '{board_name_query}'")
        raise Exception(f"Board search failed: {type(e).__name__}") from e


@mcp.tool()
async def lib_search(library_name: str, limit: int = 15) -> str:
    """
    Searches for Arduino libraries matching the given name. Performs BOTH:
    1. An online search via the Arduino Library Manager index.
    2. A fuzzy search against locally installed platform libraries (if 'thefuzz' is installed).

    Args:
        library_name: The name (or part of the name) of the library to search for
                      (e.g., "FastLED", "DHT sensor", "Adafruit GFX").
        limit: The maximum number of results to return for *each* search type
               (online, local fuzzy). Defaults to 15. Must be a positive integer.

    Returns:
        A formatted string containing results from both online and local searches,
        separated clearly. Returns a message if no matches are found in either source.

    Raises:
        ValueError: If library_name is empty or limit is invalid.
        Exception: If underlying CLI commands fail unexpectedly.
    """
    log.info(f"Tool Call: lib_search(library_name='{library_name}', limit={limit})")
    if not library_name:
        raise ValueError("Library name cannot be empty.")
    if not isinstance(limit, int) or limit <= 0:
        log.warning(f"Invalid limit '{limit}' provided, using default 15.")
        limit = 15

    final_output_lines = []
    online_results_found = False
    fuzzy_results_found = False

    # --- Online Search ---
    online_output_section = ["--- Online Search Results (Library Manager) ---"]
    online_search_cmd_args = ["lib", "search", library_name]
    try:
        # Don't check=True initially
        stdout, stderr, retcode = await _run_arduino_cli_command(online_search_cmd_args, check=False)
        full_output = (stdout or stderr).strip() # Combine output
        output_lower = full_output.lower()

        if retcode == 0 and full_output and "no libraries found" not in output_lower and "no matching libraries" not in output_lower:
            online_results_found = True
            lines = full_output.splitlines()
            header = ""
            data_lines = lines
            # Try to detect and format header nicely
            if lines and "Name" in lines[0] and ("Author" in lines[0] or "Version" in lines[0]):
                header = lines[0] + "\n" + ("-" * len(lines[0]))
                data_lines = lines[1:]
                online_output_section.append(header)

            limited_data_lines = data_lines[:limit]
            online_output_section.extend(limited_data_lines)
            if len(data_lines) > limit:
                online_output_section.append(f"... (truncated to {limit} online results)")
            log.info(f"Online lib search found {len(data_lines)} results for '{library_name}'.")
        else:
            if retcode != 0:
                log.warning(f"Online lib search command failed (code {retcode}): {stderr}")
                online_output_section.append(f"(Online search command failed: {stderr or 'Unknown error'})")
            else:
                log.info(f"Online lib search for '{library_name}' found no results.")
                online_output_section.append("(No results found in online index)")
    except Exception as e:
        log.exception(f"Error during online library search for '{library_name}'")
        online_output_section.append(f"(Error during online search: {type(e).__name__})")

    final_output_lines.extend(online_output_section)
    final_output_lines.append("\n") # Separator

    # --- Local Fuzzy Search ---
    fuzzy_output_section = ["--- Local Platform Library Matches (Fuzzy Search) ---"]
    if FUZZY_ENABLED:
        log.info(f"Performing fuzzy search on local platform libraries for '{library_name}'.")
        platform_list_cmd_args = ["lib", "list", "--all", "--format", "json"]
        fuzzy_matches = []
        try:
            # Don't check=True
            plat_stdout, plat_stderr, plat_retcode = await _run_arduino_cli_command(platform_list_cmd_args, check=False)

            if plat_retcode == 0 and plat_stdout:
                try:
                    plat_lib_data = json.loads(plat_stdout)
                    installed_libs_outer = plat_lib_data.get("libraries", plat_lib_data.get("installed_libraries", []))

                    if isinstance(installed_libs_outer, list):
                        for lib_item in installed_libs_outer:
                            lib_details = lib_item.get("library", lib_item)
                            if isinstance(lib_details, dict) and lib_details.get("location") == "platform":
                                lib_name = lib_details.get("name", "")
                                provides_includes = lib_details.get("provides_includes", [])
                                if not lib_name: continue # Skip if no name

                                best_score = 0
                                # Score against library name
                                name_score = fuzz.partial_ratio(library_name.lower(), lib_name.lower())
                                best_score = max(best_score, name_score)
                                # Score against include files (and their stems)
                                if isinstance(provides_includes, list):
                                    for include_file in provides_includes:
                                        if not include_file: continue
                                        include_stem = Path(include_file).stem
                                        include_score = fuzz.partial_ratio(library_name.lower(), include_file.lower())
                                        stem_score = fuzz.partial_ratio(library_name.lower(), include_stem.lower())
                                        best_score = max(best_score, include_score, stem_score)

                                if best_score >= FUZZY_SEARCH_THRESHOLD:
                                    fuzzy_matches.append({"name": lib_name, "includes": provides_includes, "score": best_score})
                    else:
                        log.warning("Could not parse 'libraries'/'installed_libraries' list from platform lib JSON.")
                except json.JSONDecodeError as json_e:
                    log.warning(f"Failed to decode platform lib JSON for fuzzy search. Error: {json_e}. Raw: {plat_stdout[:200]}...")
                except Exception as parse_e:
                    log.warning(f"Error parsing platform lib JSON for fuzzy search. Error: {parse_e}")
            elif plat_retcode != 0:
                log.warning(f"Failed to list all libs for fuzzy search. Exit: {plat_retcode}. Stderr: {plat_stderr}")
                fuzzy_output_section.append("(Failed to retrieve local library list for fuzzy search)")

        except Exception as e:
            log.error(f"Error during fuzzy platform lib search: {e}")
            fuzzy_output_section.append(f"(Error during fuzzy search: {type(e).__name__})")

        # Format fuzzy results
        if fuzzy_matches:
            fuzzy_results_found = True
            fuzzy_matches.sort(key=lambda x: x["score"], reverse=True)
            limited_fuzzy_matches = fuzzy_matches[:limit]
            for match in limited_fuzzy_matches:
                include_str = ", ".join(match['includes']) if match['includes'] else "(none listed)"
                fuzzy_output_section.append(f"- Name: {match['name']} (Score: {match['score']})")
                fuzzy_output_section.append(f"    Includes: {include_str}")
            if len(fuzzy_matches) > limit:
                fuzzy_output_section.append(f"... (truncated to {limit} fuzzy matches)")
            log.info(f"Fuzzy search found {len(fuzzy_matches)} potential platform library matches for '{library_name}'.")
        # Add "no results" message only if no error occurred during listing/parsing
        elif not any("(Failed" in line or "(Error" in line for line in fuzzy_output_section):
            fuzzy_output_section.append("(No relevant platform libraries found)")
    else:
        fuzzy_output_section.append("(Fuzzy search disabled - 'thefuzz' library not installed)")

    final_output_lines.extend(fuzzy_output_section)

    # Final message if nothing was found anywhere
    if not online_results_found and not fuzzy_results_found:
        no_results_msg = f"No libraries found matching '{library_name}' online or in local platform libraries."
        log.info(no_results_msg)
        return no_results_msg

    return "\n".join(final_output_lines).strip()


@mcp.tool()
async def lib_install(library_name: str) -> str:
    """
    Installs or updates an Arduino library from the official Library Manager index.
    Specify the library name exactly as found using 'lib_search'. You can optionally
    specify a version using the format 'LibraryName@Version' (e.g., "FastLED@3.5.0").
    If no version is specified, the latest version is installed.

    Args:
        library_name: The exact name of the library to install, optionally with a version.
                      (e.g., "FastLED", "DHT sensor library", "Adafruit GFX Library@2.5.7").

    Returns:
        A success message indicating installation or update status. Includes a hint
        to use 'list_library_examples' after successful installation.

    Raises:
        ValueError: If library_name is empty.
        FileNotFoundError: If the specified library name (or version) is not found in the index.
        Exception: For other installation errors (e.g., network issues, conflicts,
                   permission errors writing to the library directory).
    """
    log.info(f"Tool Call: lib_install(library_name='{library_name}')")
    if not library_name:
        raise ValueError("Library name cannot be empty.")

    install_cmd_args = ["lib", "install", library_name]
    install_success_message = ""
    try:
        # Run command, check=True will raise specific errors on failure
        install_stdout, install_stderr, _ = await _run_arduino_cli_command(install_cmd_args, check=True)

        # Parse output for success confirmation (even though check=True handles errors)
        install_output = (install_stdout or install_stderr).strip()
        log.info(f"Library install command output for '{library_name}':\n{install_output}")
        install_output_lower = install_output.lower()

        # Determine the outcome based on output messages
        if "already installed" in install_output_lower:
             if "updating" in install_output_lower or "updated" in install_output_lower:
                 install_success_message = f"Library '{library_name}' was already installed and has been updated."
             else:
                 install_success_message = f"Library '{library_name}' is already installed at the specified/latest version."
        elif "successfully installed" in install_output_lower or "downloaded" in install_output_lower:
            install_success_message = f"Successfully installed/updated library '{library_name}'."
        else:
            # Fallback success message if output isn't recognized but command didn't fail
            install_success_message = f"Library install command finished successfully for '{library_name}'. Check logs for details."
            log.warning(f"Unrecognized success message from lib install: {install_output}")

        # Add hint about examples
        # Extract base library name if version was specified
        base_lib_name = library_name.split('@')[0]
        install_success_message += f"\nYou can now use 'list_library_examples' for '{base_lib_name}' to see available examples."
        log.info(install_success_message)
        return install_success_message

    except FileNotFoundError as e:
        # Specifically catch FileNotFoundError which _run_arduino_cli_command raises for "library not found"
        log.error(f"Library install failed: '{library_name}' not found in index. {e}")
        raise FileNotFoundError(f"Install failed: Library '{library_name}' not found in the index. Use 'lib_search' to find the correct name/version.") from e
    except (PermissionError, Exception) as e:
        # Catch other errors like permission issues writing to lib folder
        log.exception(f"Library install failed for '{library_name}'")
        raise Exception(f"Library install failed for '{library_name}': {type(e).__name__}: {e}") from e


@mcp.tool()
async def list_library_examples(library_name: str) -> str:
    """
    Lists the available example sketches provided by a specific *installed* Arduino library.

    Args:
        library_name: The exact name of the INSTALLED library (e.g., "FastLED", "DHT sensor library").
                      Use 'lib_search' to find names, and 'lib_install' to install them first.

    Returns:
        A formatted string listing the examples, including their full, resolved paths.
        Returns a specific message if the library is not found among installed libraries
        or if it contains no examples.

    Raises:
        ValueError: If library_name is empty.
        FileNotFoundError: If the specified library is not found among installed libraries.
        Exception: If the command fails for other reasons (e.g., corrupted index, permission issues).
    """
    log.info(f"Tool Call: list_library_examples(library_name='{library_name}')")
    if not library_name:
        raise ValueError("Library name cannot be empty.")

    examples_cmd_args = ["lib", "examples", library_name]
    try:
        # Don't check=True initially to handle "not found" / "no examples" gracefully
        examples_stdout, examples_stderr, examples_retcode = await _run_arduino_cli_command(
            examples_cmd_args, check=False
        )
        combined_output = (examples_stdout + "\n" + examples_stderr).strip()
        combined_output_lower = combined_output.lower()

        # Handle command failure or specific "not found" messages
        if examples_retcode != 0:
            if "library not found" in combined_output_lower:
                log.warning(f"Library '{library_name}' not found when listing examples.")
                raise FileNotFoundError(f"Library '{library_name}' not found among installed libraries. Use 'lib_install' first.")
            # Handle "no examples" message even if retcode is non-zero (can happen)
            elif "no examples found" in combined_output_lower:
                 log.info(f"No examples found for library '{library_name}' (reported by command failure).")
                 return f"No examples found for library '{library_name}'."
            else:
                log.error(f"Failed to list examples for library '{library_name}'. Exit: {examples_retcode}. Output: {combined_output}")
                raise Exception(f"Failed to list examples for '{library_name}'. Error: {combined_output}")

        # Handle "no examples" message if command succeeded
        if "no examples found" in combined_output_lower:
            log.info(f"No examples found for library '{library_name}' (command succeeded).")
            return f"No examples found for library '{library_name}'."

        # Clean ANSI codes from stdout before parsing paths
        cleaned_stdout = ANSI_ESCAPE_RE.sub('', examples_stdout).strip()
        log.debug(f"Cleaned 'lib examples' stdout for '{library_name}':\n{cleaned_stdout}")

        if not cleaned_stdout:
            log.warning(f"Command 'lib examples {library_name}' succeeded but produced empty stdout after cleaning.")
            return f"Command succeeded, but no example paths were listed for library '{library_name}'."

        # Parse the cleaned output for example paths
        log.info(f"Parsing library examples output for '{library_name}'.")
        example_paths: List[Path] = []
        # Regex to capture paths, potentially handling variations like leading spaces/hyphens
        # Assumes paths don't contain newline characters.
        example_line_pattern = r"^\s*[-*]?\s*(.+?)\s*$"
        processed_lines = set() # Avoid processing duplicate lines if CLI output is weird

        for line in cleaned_stdout.splitlines():
            line_strip = line.strip()
            if not line_strip or line_strip in processed_lines:
                continue
            processed_lines.add(line_strip)

            match = re.match(example_line_pattern, line_strip)
            if match:
                path_str = match.group(1).strip()
                if not path_str:
                    log.warning(f"Parsed an empty path string from line: '{line_strip}'")
                    continue
                try:
                    # Resolve the path to check existence and get absolute path
                    # Allow non-existent paths initially, check later
                    example_path = Path(path_str).resolve(strict=False)
                    exists, _, _ = await _async_file_op(_sync_check_exists, example_path)
                    if exists:
                        example_paths.append(example_path)
                    else:
                        log.warning(f"Path listed by 'lib examples' resolved to '{example_path}' but does not exist. Skipping.")
                except (ValueError, OSError) as path_err:
                     log.warning(f"Could not process or resolve path from 'lib examples' output: '{path_str}'. Error: {path_err}")
                except Exception as path_err: # Catch unexpected errors
                     log.warning(f"Unexpected error processing path '{path_str}': {path_err}")

        # Format the final output
        if example_paths:
            examples_info = f"Examples for library '{library_name}':\n  Example Sketch Paths:"
            for full_path in sorted(example_paths):
                examples_info += f"\n    - {full_path}"
            examples_info += "\n\n(Use 'read_file' with the full path to view an example's code.)"
            log.info(f"Found {len(example_paths)} examples for '{library_name}'.")
            return examples_info.strip()
        else:
            log.warning(f"Could not parse any valid example paths from 'lib examples {library_name}' output, although command succeeded. Cleaned output:\n{cleaned_stdout}")
            return f"Command succeeded, but failed to parse valid example paths for '{library_name}'. Please check server logs."

    except FileNotFoundError as e:
        # Re-raise specific FileNotFoundError if caught
        raise e
    except Exception as e:
        log.exception(f"Error occurred while trying to list examples for '{library_name}'.")
        raise Exception(f"An error occurred retrieving examples for '{library_name}': {type(e).__name__}") from e


@mcp.tool()
async def read_file(filepath: str) -> str:
    """
    Reads the content of a specified file. Operates within the user's home directory ('~').

    *** Special Sketch Handling ***
    If the filepath points specifically to the main '.ino' file within a standard sketch
    directory structure (e.g., '~/Documents/Arduino_MCP_Sketches/MySketch/MySketch.ino'),
    this tool reads and concatenates the content of ALL '.ino' and '.h' files found within that
    SAME sketch directory ('~/Documents/Arduino_MCP_Sketches/MySketch/'), providing the
    complete code context for that sketch. The files are concatenated in alphabetical order.

    For any other file path (even other files within a sketch directory, or files outside
    the sketch base), it reads only the content of that single specified file.

    Args:
        filepath: The path to the file to read (absolute, relative to CWD, or using '~').
                  Must resolve to a path within the user's home directory.

    Returns:
        The content of the file (or combined content of sketch files) as a string.

    Raises:
        ValueError: If the path string is invalid.
        FileNotFoundError: If the specified file (or initial .ino file for sketch read) is not found.
        IsADirectoryError: If the path points to a directory (and doesn't trigger sketch read).
        PermissionError: If file permissions prevent reading or path is outside home directory.
        Exception: For other I/O errors.
    """
    log.info(f"Tool Call: read_file(filepath='{filepath}')")
    resolved_path: Optional[Path] = None
    try:
        # Validate that the path resolves within the user's home directory
        resolved_path = await _resolve_and_validate_path(
            filepath,
            allowed_bases=[USER_HOME], # Restrict reads to user's home
            check_existence=True # Ensure the target exists before proceeding
        )

        # Check if it's a file (check_existence=True already did this)
        if not resolved_path.is_file():
             raise IsADirectoryError(f"Path exists but is a directory, not a file: {resolved_path}")

        # --- Special Sketch Handling Logic ---
        is_main_ino_in_sketch = False
        sketch_dir_to_read: Optional[Path] = None
        if resolved_path.suffix.lower() == ".ino":
            try:
                # Check if it's inside SKETCHES_BASE_DIR and parent dir name matches stem
                if resolved_path.is_relative_to(SKETCHES_BASE_DIR) and resolved_path.parent.name == resolved_path.stem:
                    is_main_ino_in_sketch = True
                    sketch_dir_to_read = resolved_path.parent
            except ValueError:
                pass # Not relative to sketches base, treat as normal file

        if is_main_ino_in_sketch and sketch_dir_to_read:
            sketch_name = sketch_dir_to_read.name
            log.info(f"Detected read for main sketch file '{resolved_path.name}'. Reading all .ino/.h files in directory: {sketch_dir_to_read}")
            try:
                all_items = await _async_file_op(_sync_list_dir, sketch_dir_to_read)
                files_to_combine: List[Path] = []
                for item_name in all_items:
                     item_path = sketch_dir_to_read / item_name
                     # Check if it's a file and ends with .ino or .h
                     exists, is_file, _ = await _async_file_op(_sync_check_exists, item_path)
                     if exists and is_file and item_name.lower().endswith((".ino", ".h")):
                         files_to_combine.append(item_path)

                if not files_to_combine:
                    # Should not happen if the main .ino exists, but handle defensively
                    log.warning(f"Main .ino '{resolved_path.name}' exists, but no .ino/.h files found to combine in {sketch_dir_to_read}. Reading only main file.")
                    content = await _async_file_op(_sync_read_file, resolved_path)
                    return content

                # Sort files alphabetically for consistent order
                files_to_combine.sort()

                combined_content_parts = [f"// --- Combined content of sketch: {sketch_name} ---"]
                # Read files concurrently
                read_tasks = {fp: _async_file_op(_sync_read_file, fp) for fp in files_to_combine}
                results = await asyncio.gather(*read_tasks.values(), return_exceptions=True)

                # Combine results
                for i, fp in enumerate(files_to_combine):
                    result = results[i]
                    combined_content_parts.append(f"\n\n// --- File: {fp.name} ---")
                    if isinstance(result, Exception):
                        log.error(f"Error reading file {fp} during sketch combine: {result}")
                        combined_content_parts.append(f"// Error reading file: {type(result).__name__}: {result}")
                    elif isinstance(result, str):
                        combined_content_parts.append(result)
                    else: # Should not happen
                         log.error(f"Unexpected result type reading {fp}: {type(result)}")
                         combined_content_parts.append(f"// Error: Unexpected read result type {type(result)}")

                final_output = "\n".join(combined_content_parts)
                log.info(f"Read and combined {len(files_to_combine)} .ino/.h files from {sketch_dir_to_read} ({len(final_output)} chars)")
                return final_output

            except Exception as list_read_err:
                # Fallback to reading only the requested file if combining fails
                log.error(f"Error listing/reading files in sketch directory {sketch_dir_to_read}: {list_read_err}. Falling back to reading only {resolved_path.name}.")
                content = await _async_file_op(_sync_read_file, resolved_path)
                log.info(f"Read single file (fallback after combine error): {resolved_path} ({len(content)} chars)")
                return content
        else:
            # Standard single file read
            content = await _async_file_op(_sync_read_file, resolved_path)
            log.info(f"Read single file: {resolved_path} ({len(content)} chars)")
            return content

    except (FileNotFoundError, ValueError, IsADirectoryError, PermissionError) as e:
        log.error(f"Read file error for '{filepath}' (resolved to {resolved_path}): {type(e).__name__}: {e}")
        raise e # Re-raise specific, expected errors
    except Exception as e:
        error_msg = f"Unexpected error reading '{filepath}' (resolved to {resolved_path}): {type(e).__name__}: {e}"
        log.exception(error_msg) # Log with traceback
        raise Exception(error_msg) from e


@mcp.tool()
async def write_file(filepath: str, content: str, board_fqbn: str = DEFAULT_FQBN) -> str:
    """
    Writes content to a specified file, overwriting it if it exists.

    *** Security Restrictions & Warnings ***
    - Writing '.ino' files is RESTRICTED to the designated sketch directory structure
      ('~/Documents/Arduino_MCP_Sketches/sketch_name/'). The filename must match the
      directory name (e.g., .../MySketch/MySketch.ino).
    - Writing all other file types is RESTRICTED to the user's home directory ('~').
    - This operation OVERWRITES existing files without confirmation. Use with caution.

    *** Automatic Compilation Trigger ***
    If the filepath points to a main '.ino' file within the standard sketch
    directory structure (as described above), this tool will automatically attempt
    to compile the sketch AFTER writing the file. It uses the provided 'board_fqbn'
    (defaulting to 'arduino:avr:uno' if not specified). The compilation result
    (success or failure message) will be appended to the return string.

    Args:
        filepath: The path where the file should be written (absolute, relative to CWD, or ~).
                  Must resolve to a path within the allowed directories based on file type.
        content: The text content to write to the file.
        board_fqbn: Required for automatic compilation when writing a main sketch '.ino' file.
                    Defaults to 'arduino:avr:uno'. Provide the correct FQBN for the
                    target board if different. Format must be 'vendor:arch:board'.

    Returns:
        A string indicating success of the write operation, potentially followed by
        the result of the automatic compilation attempt for main sketch .ino files.

    Raises:
        ValueError: If path or FQBN format is invalid.
        PermissionError: If writing is not allowed at the location (outside restricted areas).
        IsADirectoryError: If the path points to an existing directory.
        FileNotFoundError: If the parent directory for a new file cannot be created.
        Exception: For compilation errors during auto-compile or other I/O errors.
    """
    log.info(f"Tool Call: write_file(filepath='{filepath}', fqbn='{board_fqbn}')")
    resolved_path: Optional[Path] = None
    is_main_ino_in_sketch = False
    sketch_dir_for_compile: Optional[Path] = None
    allowed_bases: List[Path]

    try:
        # Determine allowed base directory based on file type and path structure
        is_potential_ino = filepath.lower().endswith(".ino")
        path_obj_pre_resolve = Path(filepath).expanduser() # For structure check

        if is_potential_ino:
            # Check if it looks like a *main* sketch file (parent dir name == stem)
            # AND is directly under SKETCHES_BASE_DIR
            parent_dir = path_obj_pre_resolve.parent
            if parent_dir.parent == SKETCHES_BASE_DIR and parent_dir.name == path_obj_pre_resolve.stem:
                allowed_bases = [SKETCHES_BASE_DIR] # Allow writing within any sketch dir
                is_main_ino_in_sketch = True # Mark for potential auto-compile
                sketch_dir_for_compile = parent_dir.resolve(strict=False) # Use resolved parent for compile
                log.debug(f"Path '{filepath}' identified as main sketch .ino. Allowed base: {allowed_bases}")
            else:
                # It's an .ino file but not in the standard sketch structure, restrict to home
                allowed_bases = [USER_HOME]
                log.debug(f"Path '{filepath}' is .ino but not main sketch file. Allowed base: {allowed_bases}")
        else:
            # Not an .ino file, restrict to home directory
            allowed_bases = [USER_HOME]
            log.debug(f"Path '{filepath}' is not .ino. Allowed base: {allowed_bases}")

        # Validate and resolve the path against the determined allowed bases
        resolved_path = await _resolve_and_validate_path(
            filepath,
            allowed_bases=allowed_bases,
            check_existence=False # Don't require existence for writing
        )

        # Explicitly re-check if it's the main sketch file *after* resolution
        # This handles cases where symlinks might change the structure
        if resolved_path.suffix.lower() == ".ino":
             try:
                 if resolved_path.is_relative_to(SKETCHES_BASE_DIR) and resolved_path.parent.name == resolved_path.stem:
                     is_main_ino_in_sketch = True
                     sketch_dir_for_compile = resolved_path.parent # Update compile dir based on resolved path
                 else: # If resolved path is not main sketch, disable compile trigger
                      is_main_ino_in_sketch = False
                      sketch_dir_for_compile = None
             except ValueError: # Not relative to sketches base
                 is_main_ino_in_sketch = False
                 sketch_dir_for_compile = None
        else: # Not an ino file after resolution
             is_main_ino_in_sketch = False
             sketch_dir_for_compile = None


        # Validate FQBN format if provided (even if not used for auto-compile)
        if board_fqbn and (":" not in board_fqbn or len(board_fqbn.split(':')) < 3):
             raise ValueError(f"Invalid board_fqbn format provided: '{board_fqbn}'. Must be 'vendor:arch:board'.")

        # Check if the resolved path points to an existing directory
        exists, _, is_dir = await _async_file_op(_sync_check_exists, resolved_path)
        if exists and is_dir:
            raise IsADirectoryError(f"Cannot write file content: path '{resolved_path}' points to an existing directory.")

        # Perform the write operation
        log.warning(f"Attempting to write/overwrite file: {resolved_path}")
        await _async_file_op(_sync_write_file, resolved_path, content)
        write_success_msg = f"Successfully wrote {len(content)} characters to file '{resolved_path}'."
        log.info(write_success_msg)

        # --- Automatic Compilation ---
        compile_result_msg = ""
        if is_main_ino_in_sketch and sketch_dir_for_compile:
            effective_fqbn = board_fqbn # Use provided (and validated) or default FQBN
            log.info(f"Main sketch .ino write detected. Triggering auto-compile for sketch '{sketch_dir_for_compile.name}' with FQBN '{effective_fqbn}'.")
            # Use a consistent build path for potential caching
            build_path_abs = (BUILD_TEMP_DIR / f"{sketch_dir_for_compile.name}_write_{effective_fqbn.replace(':', '_')}").resolve(strict=False)
            try:
                # _execute_compile handles mkdir for build_path_abs
                compile_success_message = await _execute_compile(sketch_dir_for_compile, build_path_abs, effective_fqbn)
                # Append success message from compile (includes size info)
                compile_result_msg = f"\nAutomatic compilation using FQBN '{effective_fqbn}' successful: {compile_success_message.replace('Compilation successful.', '').strip()}"
                log.info(f"Automatic compilation after write succeeded for {resolved_path}")
            except Exception as compile_err:
                # Append failure message
                log.error(f"Automatic compilation after write FAILED for {resolved_path} using FQBN '{effective_fqbn}': {compile_err}")
                compile_result_msg = f"\nWrite succeeded, but automatic compilation using FQBN '{effective_fqbn}' FAILED: {compile_err}"

        return write_success_msg + compile_result_msg

    except (ValueError, IsADirectoryError, PermissionError, FileNotFoundError) as e:
        log.error(f"Write file error for '{filepath}' (resolved to {resolved_path}): {type(e).__name__}: {e}")
        raise e # Re-raise specific, expected errors
    except Exception as e:
        error_msg = f"Unexpected error writing to '{filepath}' (resolved to {resolved_path}): {type(e).__name__}: {e}"
        log.exception(error_msg) # Log with traceback
        raise Exception(error_msg) from e


@mcp.tool()
async def rename_file(old_path: str, new_path: str) -> str:
    """
    Renames or moves a file or directory.

    *** Security Restrictions & Warnings ***
    - Operation is RESTRICTED to occur entirely within the user's home directory ('~').
      Both the source (old_path) and destination (new_path) must resolve within home.
    - Use with EXTREME CAUTION, especially when moving directories, as this can
      restructure user files and is hard to undo.
    - This operation will FAIL if the destination path already exists.

    Args:
        old_path: The current path of the file or directory (absolute, relative to CWD, or ~).
                  Must resolve to a path within the user's home directory.
        new_path: The desired new path for the file or directory (absolute, relative to CWD, or ~).
                  Must resolve to a path within the user's home directory.

    Returns:
        A success message confirming the rename/move operation.

    Raises:
        ValueError: If paths are invalid.
        FileNotFoundError: If the old_path does not exist.
        FileExistsError: If the new_path already exists.
        PermissionError: If permissions prevent the operation or paths are outside home directory.
        Exception: For other I/O errors.
    """
    log.info(f"Tool Call: rename_file(old='{old_path}', new='{new_path}')")
    resolved_old_path: Optional[Path] = None
    resolved_new_path: Optional[Path] = None
    try:
        # Validate both paths must be within USER_HOME
        allowed_bases = [USER_HOME]
        resolved_old_path = await _resolve_and_validate_path(
            old_path,
            allowed_bases=allowed_bases,
            check_existence=True # Source must exist
        )
        resolved_new_path = await _resolve_and_validate_path(
            new_path,
            allowed_bases=allowed_bases,
            check_existence=False # Destination must NOT exist
        )

        # Check if destination already exists (double check after resolve)
        new_exists, _, _ = await _async_file_op(_sync_check_exists, resolved_new_path)
        if new_exists:
            raise FileExistsError(f"Destination path already exists: {resolved_new_path}")

        # Perform the rename/move
        log.warning(f"Attempting to rename/move '{resolved_old_path}' to '{resolved_new_path}'. Use with caution.")
        await _async_file_op(_sync_rename_file, resolved_old_path, resolved_new_path)
        success_msg = f"Successfully renamed/moved '{resolved_old_path}' to '{resolved_new_path}'."
        log.info(success_msg)
        return success_msg

    except (FileNotFoundError, FileExistsError, ValueError, PermissionError) as e:
        log.error(f"Rename file error '{old_path}' -> '{new_path}': {type(e).__name__}: {e}")
        raise e # Re-raise specific, expected errors
    except Exception as e:
        error_msg = f"Unexpected error renaming '{old_path}' (-> {resolved_old_path}) to '{new_path}' (-> {resolved_new_path}): {type(e).__name__}: {e}"
        log.exception(error_msg) # Log with traceback
        raise Exception(error_msg) from e


@mcp.tool()
async def remove_file(filepath: str) -> str:
    """
    Removes (deletes) a specified file.

    *** Security Restrictions & Warnings ***
    - Operation is RESTRICTED to files within the user's home directory ('~').
    - This operation is IRREVERSIBLE and permanently deletes the file.
    - This tool WILL NOT remove directories, only files.
    - Use with EXTREME CAUTION.

    Args:
        filepath: The path to the file to be deleted (absolute, relative to CWD, or ~).
                  Must resolve to a file within the user's home directory.

    Returns:
        A success message confirming the file removal.

    Raises:
        ValueError: If the path is invalid.
        FileNotFoundError: If the file does not exist at the specified path.
        IsADirectoryError: If the path points to a directory instead of a file.
        PermissionError: If permissions prevent deletion or path is outside home directory.
        Exception: For other I/O errors.
    """
    log.info(f"Tool Call: remove_file(filepath='{filepath}')")
    resolved_path: Optional[Path] = None
    try:
        # Validate path is within home and exists
        resolved_path = await _resolve_and_validate_path(
            filepath,
            allowed_bases=[USER_HOME],
            check_existence=True
        )

        # Ensure it's a file, not a directory (check_existence validated it exists)
        if not resolved_path.is_file():
             raise IsADirectoryError(f"Cannot remove: Path points to a directory, not a file: {resolved_path}")

        # Perform the removal
        log.warning(f"Attempting to permanently remove file: {resolved_path}. This is irreversible.")
        await _async_file_op(_sync_remove_file, resolved_path)
        success_msg = f"Successfully removed file: {resolved_path}"
        log.info(success_msg)
        return success_msg

    except (ValueError, FileNotFoundError, IsADirectoryError, PermissionError) as e:
        log.error(f"Remove file error for '{filepath}' (resolved to {resolved_path}): {type(e).__name__}: {e}")
        raise e # Re-raise specific, expected errors
    except Exception as e:
        error_msg = f"Unexpected error removing '{filepath}' (resolved to {resolved_path}): {type(e).__name__}: {e}"
        log.exception(error_msg) # Log with traceback
        raise Exception(error_msg) from e

# ==============================================================================
# Main Execution Block
# ==============================================================================
def main():
    """Main entry point for running the server."""
    log.info("==================================================")
    log.info(" Starting Arduino FastMCP Server (v2.1 - Polished)")
    log.info("==================================================")
    try:
        SKETCHES_BASE_DIR.mkdir(parents=True, exist_ok=True)
        BUILD_TEMP_DIR.mkdir(parents=True, exist_ok=True)
        log.info("Core sketch/build directories verified/created.")
    except OSError as e:
         log.critical(f"CRITICAL ERROR: Could not create essential directories {SKETCHES_BASE_DIR} or {BUILD_TEMP_DIR}. Check permissions. Server cannot function correctly. Error: {e}")
         # Exit the server process immediately if essential directories fail
         sys.exit(1) # Exit with non-zero code
    try:
         log.info("Initializing FastMCP server...")
         # Server instance 'mcp' should be defined globally in the script
         log.info(f"Running MCP server '{mcp.name}' via STDIO transport. Waiting for client connection...")
         mcp.run(transport='stdio') # Blocks here until client disconnects or error
         log.info("Client disconnected.")
    except KeyboardInterrupt:
         log.info("Server stopped by user (KeyboardInterrupt).")
    except Exception as e:
         log.exception("Server exited with an unhandled error:")
         sys.exit(1) # Also exit on other unhandled errors in main
    finally:
        log.info("Server shutdown sequence initiated.")
        # Add any specific cleanup needed here if not handled by lifespan context
        log.info("Server shutdown complete.")
        log.info("==================================================")

# Keep this guard if you still want to run the script directly
# (e.g., python src/mcp_arduino_server/server.py)
# Or rely on the entry point defined in pyproject.toml when installed
if __name__ == "__main__":
    main()