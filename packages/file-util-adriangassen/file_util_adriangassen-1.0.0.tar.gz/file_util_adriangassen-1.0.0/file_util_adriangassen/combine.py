from file_util_adriangassen.utils import user_confirms



def combine(args):
    if args.dest_filepath.exists() and not args.confirm:
        print(f"A file already exists at destination {args.filepath}.")
        if not user_confirms():
            return
    if not args.first_filepath.exists():
        raise RuntimeError(f"Error: source filepath {args.first_filepath} does not exist.")
    if not args.second_filepath.exists():
        raise RuntimeError(f"Error: source filepath {args.second_filepath} does not exist.")
    try:
        with open(args.first_filepath, "r") as f1, open(args.second_filepath, "r") as f2, open(args.dest_filepath, "w") as df:
            f1_content = f1.read()
            f2_content = f2.read()
            df.write(f1_content + f2_content)
    except Exception as e:
        raise Exception(f"Error: Failed to combine {args.first_filepath} and {args.second_filepath} into new file {args.dest_filepath}") from e


