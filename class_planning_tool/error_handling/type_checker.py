
import os

def check_file_type(file_path, allowed_extensions):
    _, file_extension = os.path.splitext(file_path)
    return file_extension.lower() in allowed_extensions
