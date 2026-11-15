"""Core tools for the autonomous engineer assistant agent.
Provides shell command execution, file reading, writing, and editing.
"""

import os
import subprocess
from pathlib import Path


def run_command(command: str, timeout_seconds: int = 60) -> dict:
    """Execute a bash shell command in the local environment.

    Args:
        command: The bash command line string to run.
        timeout_seconds: Maximum time to wait for the command to finish.

    Returns:
        dict: Containing 'exit_code', 'stdout', and 'stderr'.
    """
    try:
        proc = subprocess.run(
            ["bash", "-c", command],
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
            encoding="utf-8",
            errors="replace",
        )
        return {
            "exit_code": proc.returncode,
            "stdout": proc.stdout.strip(),
            "stderr": proc.stderr.strip(),
            "status": "success" if proc.returncode == 0 else "failed",
        }
    except subprocess.TimeoutExpired:
        return {
            "exit_code": -1,
            "stdout": "",
            "stderr": f"Command timed out after {timeout_seconds} seconds.",
            "status": "timeout",
        }
    except Exception as e:
        return {
            "exit_code": -1,
            "stdout": "",
            "stderr": f"Execution error: {str(e)}",
            "status": "error",
        }


def read_file(path: str, start_line: int = 1, end_line: int = 500) -> str:
    """Read contents of a file within an optional line range.

    Args:
        path: Path to the file (supports ~ and absolute/relative paths).
        start_line: First line to read (1-indexed).
        end_line: Last line to read (inclusive).

    Returns:
        str: File content or error description.
    """
    try:
        file_path = Path(os.path.expanduser(path)).resolve()
        if not file_path.exists():
            return f"Error: File '{file_path}' does not exist."
        if not file_path.is_file():
            return f"Error: Path '{file_path}' is not a regular file."

        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            lines = f.readlines()

        total_lines = len(lines)
        start_idx = max(0, start_line - 1)
        end_idx = min(total_lines, end_line)

        selected = lines[start_idx:end_idx]
        formatted = "".join(
            f"{i + start_idx + 1}: {line}" for i, line in enumerate(selected)
        )
        return (
            f"--- File: {file_path} (Lines {start_idx + 1}-{end_idx} of {total_lines}) ---\n"
            + formatted
        )
    except Exception as e:
        return f"Error reading file '{path}': {str(e)}"


def write_file(path: str, content: str, overwrite: bool = True) -> str:
    """Write or overwrite content to a file. Parent directories are created automatically.

    Args:
        path: Path to the target file.
        content: The text content to write.
        overwrite: Whether to overwrite if the file already exists.

    Returns:
        str: Status message.
    """
    try:
        file_path = Path(os.path.expanduser(path)).resolve()
        if file_path.exists() and not overwrite:
            return f"Error: File '{file_path}' already exists and overwrite is set to False."

        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

        return f"Success: File written successfully to '{file_path}' ({len(content)} bytes)."
    except Exception as e:
        return f"Error writing file '{path}': {str(e)}"


def edit_file(path: str, target: str, replacement: str) -> str:
    """Replace an exact substring in an existing file.

    Args:
        path: Path to the file.
        target: The exact string block to be replaced.
        replacement: The replacement string.

    Returns:
        str: Status message.
    """
    try:
        file_path = Path(os.path.expanduser(path)).resolve()
        if not file_path.exists():
            return f"Error: File '{file_path}' does not exist."

        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()

        if target not in content:
            return f"Error: Target string not found in '{file_path}'."

        count = content.count(target)
        new_content = content.replace(target, replacement)

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)

        return f"Success: Replaced {count} occurrence(s) in '{file_path}'."
    except Exception as e:
        return f"Error editing file '{path}': {str(e)}"


def list_directory(path: str = ".") -> str:
    """List directory entries with detailed file metadata.

    Args:
        path: Path to the directory (defaults to current directory).

    Returns:
        str: Formatted directory listing.
    """
    try:
        dir_path = Path(os.path.expanduser(path)).resolve()
        if not dir_path.exists():
            return f"Error: Directory '{dir_path}' does not exist."
        if not dir_path.is_dir():
            return f"Error: Path '{dir_path}' is not a directory."

        entries = sorted(dir_path.iterdir(), key=lambda p: (not p.is_dir(), p.name.lower()))
        result = [f"Directory listing for: {dir_path}"]
        for entry in entries:
            kind = "[DIR] " if entry.is_dir() else "[FILE]"
            size = ""
            if entry.is_file():
                try:
                    size = f" ({entry.stat().st_size} bytes)"
                except Exception:
                    size = ""
            result.append(f"  {kind} {entry.name}{size}")

        return "\n".join(result)
    except Exception as e:
        return f"Error listing directory '{path}': {str(e)}"
