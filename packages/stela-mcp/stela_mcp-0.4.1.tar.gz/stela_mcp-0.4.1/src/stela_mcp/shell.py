"""Shell command execution implementation."""

import os
import subprocess
from typing import Any


class ShellExecutor:
    def __init__(self, working_dir: str | None = None) -> None:
        # Always use the actual system working directory
        self.working_dir = os.getcwd()

    async def execute_command(
        self, command: str, args: list[str], working_dir: str | None = None
    ) -> dict:
        """Execute a shell command with proper error handling and output capture."""
        if not command:
            return {"error": "Command is required", "success": False, "exit_code": -1}

        try:
            # Combine command and args into a list and use shell=False for security
            command_list = [command] + args
            # Command and args are validated by SecurityManager before reaching here
            # shell=False prevents command injection, and the command list is pre-validated
            process = subprocess.Popen(  # noqa: S603
                command_list,  # Pass the list
                shell=False,  # Set shell=False for security
                cwd=working_dir or self.working_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            stdout, stderr = process.communicate()

            return {
                "exit_code": process.returncode,
                "stdout": stdout,
                "stderr": stderr,
                "success": process.returncode == 0,
            }
        except Exception as e:
            return {
                "error": str(e),
                "exit_code": -1,
                "stdout": "",
                "stderr": str(e),
                "success": False,
            }

    async def change_directory(self, path: str) -> dict[str, Any]:
        """Change the working directory with validation."""
        if not path:
            return {"success": False, "error": "Path is required"}

        try:
            if not os.path.exists(path):
                return {"success": False, "error": "Path does not exist"}

            if not os.path.isdir(path):
                return {"success": False, "error": "Path is not a directory"}

            # Update both the instance variable and change the actual working directory
            os.chdir(path)
            self.working_dir = os.path.abspath(path)
            return {"success": True, "path": self.working_dir}
        except Exception as e:
            return {"success": False, "error": str(e)}
