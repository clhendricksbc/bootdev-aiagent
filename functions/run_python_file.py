
import os
import subprocess

def run_python_file(working_directory, file_path, args=None):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
        if os.path.commonpath([working_dir_abs, target_file_path]) != working_dir_abs:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not target_file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
        
        command = ["python", target_file_path]
        if args:
            command.extend(args)
        run_command = subprocess.run(command, capture_output=True, cwd=working_dir_abs, text=True, timeout=30)
        output = []
        if run_command.returncode != 0:
            output.append(f"Process exited with code {run_command.returncode}")
        if not run_command.stdout and not run_command.stderr:
            output.append("No output produced")
        if run_command.stdout:
            output.append(f"STDOUT: {run_command.stdout}")
        if run_command.stderr:
            output.append(f"STDERR: {run_command.stderr}")
        return "\n".join(output)

    except Exception as e:
        return f"Error: executing Python file: {e}"