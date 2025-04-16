from file_util_adriangassen.utils import user_confirms



def create(args):
    if args.filepath.exists() and not args.confirm:
        print(f"A file already exists at {args.filepath}.")
        if not user_confirms():
            return
    try:
        content_str = " ".join(args.content)
        with open(args.filepath, "w") as f:
            f.write(content_str)
    except Exception as e:
        raise Exception(f"Error: Failed to create new file {args.filepath}") from e


