import os

DEFAULT_IGNORED_DIRS = {
    'venv', '.venv', '__pycache__', '.pytest_cache', '.mypy_cache',
    'node_modules', 'dist', 'build', '.next', '.nuxt',
    '.git', '.svn', '.idea', '.vscode',
    '.DS_Store', 'Thumbs.db'
}

def print_tree(path: str = ".", ignore: set = None, prefix: str = ""):
    if ignore is None:
        ignore = DEFAULT_IGNORED_DIRS

    try:
        items = sorted(os.listdir(path))
    except (PermissionError, FileNotFoundError):
        return

    for idx, item in enumerate(items):
        abs_path = os.path.join(path, item)
        if item in ignore or os.path.islink(abs_path):
            continue

        is_last = idx == len(items) - 1
        branch = "└── " if is_last else "├── "
        print(prefix + branch + item)

        if os.path.isdir(abs_path):
            extension = "    " if is_last else "│   "
            print_tree(abs_path, ignore, prefix + extension)
