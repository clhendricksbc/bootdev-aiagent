import os
from google.genai import types

def write_file(working_directory, file_path, content):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        abs_file_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
        if os.path.commonpath([working_dir_abs, abs_file_path]) != working_dir_abs:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(abs_file_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        parent_dir = os.path.dirname(abs_file_path)
        os.makedirs(parent_dir, exist_ok=True)
        with open(abs_file_path, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        print(f"Error: {e}")

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes to a file specified by file_path, within a user-provided working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to the file to be written",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to be written to the specified file",
            ),
        },
        required=["file_path", "content"],
    ),
)