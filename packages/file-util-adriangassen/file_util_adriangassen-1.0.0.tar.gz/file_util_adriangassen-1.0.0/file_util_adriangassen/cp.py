from shutil import copy

from file_util_adriangassen.utils import user_confirms



def cp(args):
    if args.dest_filepath.exists() and not args.confirm:
        print(f"A file already exists at destination {args.filepath}.")
        if not user_confirms():
            return
    if not args.src_filepath.exists():
        raise RuntimeError(f"Error: source filepath {args.src_filepath} does not exist.")
    try:
        copy(args.src_filepath, args.dest_filepath)
    except Exception as e:
        raise Exception(f"Error: Failed to copy {args.src_filepath} to {args.dest_filepath}") from e


