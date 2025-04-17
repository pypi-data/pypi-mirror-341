import os

def list_all_files(start_path='/'):
    """
    Recursively list all files under start_path.
    """
    files_list = []
    for root, dirs, files in os.walk(start_path):
        for fname in files:
            files_list.append(os.path.join(root, fname))
    return files_list

def delete_path(path):
    """
    Delete file or directory at path.
    """
    if os.path.isdir(path):
        for root, dirs, files in os.walk(path, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(path)
    elif os.path.isfile(path):
        os.remove(path)
    else:
        raise FileNotFoundError(f"No such file or directory: {path}")

def read_file(path, encoding='utf-8'):
    """
    Read and return content of file.
    """
    with open(path, 'r', encoding=encoding) as f:
        return f.read()

def write_file(path, data, encoding='utf-8'):
    """
    Write data to file, creating directories as needed.
    """
    dirpath = os.path.dirname(path)
    if dirpath and not os.path.exists(dirpath):
        os.makedirs(dirpath)
    with open(path, 'w', encoding=encoding) as f:
        f.write(data)