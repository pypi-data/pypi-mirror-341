import os

from file_util_adriangassen.utils import user_confirms



def remove(args):
    if not args.filepath.is_file():
        raise RuntimeError(f"Error: {args.filepath} is not a regular file. This tool can currently only delete regular files.")
    if not args.confirm:
        print(f"Do you really want to delete {args.filepath}?")
        if not user_confirms():
            return
    try:
        os.remove(args.filepath)
    except Exception as e:
        raise Exception(f"Error: failed to delete file {args.filepath}") from e


