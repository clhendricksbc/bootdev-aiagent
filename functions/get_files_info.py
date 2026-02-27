import os

def get_files_info(working_directory, directory="."):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
        # Will be True or False
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        valid_dir = os.path.isdir(target_dir)
        if not valid_dir:
            return f'Error: "{directory}" is not a directory'
        target_dir_items = os.listdir(target_dir)
        item_info_list = []
        for item in target_dir_items:
            filepath = os.path.join(target_dir, item)
            file_size = os.path.getsize(filepath)
            is_dir = os.path.isdir(filepath)
            item_info = f"- {item}: file_size={file_size} bytes, is_dir={is_dir}"
            item_info_list.append(item_info)
        return "\n".join(item_info_list)
        
    except Exception as e: 
        return f"Error: {e}"

    
