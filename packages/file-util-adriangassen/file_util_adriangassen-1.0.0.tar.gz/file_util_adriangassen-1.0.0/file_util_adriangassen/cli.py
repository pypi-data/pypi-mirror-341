import argparse
from pathlib import Path
import sys

from file_util_adriangassen.create import create
from file_util_adriangassen.cp import cp
from file_util_adriangassen.combine import combine
from file_util_adriangassen.remove import remove



def set_up_arg_parser():
    parser = argparse.ArgumentParser(
        prog="file-util",
        description="A simple file utility"
    )

    subparsers = parser.add_subparsers(required=True,
                                        title="Subcommands",
                                        description="Choose one of the file-util functions from the follow subcommands"
    )

    parser_create = subparsers.add_parser("create", description="Create a new file, either empty or with content")
    parser_create.add_argument("-c", "--confirm", action="store_true", help="Overwrite existing files without confirmation")
    parser_create.add_argument("filepath", type=Path, help="File path to create new file at, will ask for confirmation if file already exists at the path")
    parser_create.add_argument("content", nargs="*", default=[""], help="Optional: Content to write to new file")
    parser_create.set_defaults(func=create)

    parser_cp = subparsers.add_parser("cp", description="Copy existing file to another location")
    parser_cp.add_argument("-c", "--confirm", action="store_true", help="Overwrite existing file without confirmation")
    parser_cp.add_argument("src_filepath", type=Path, help="File path of source file to be copied")
    parser_cp.add_argument("dest_filepath", type=Path, help="File path of destination to copy to, will ask for confirmation if file already exists at the path")
    parser_cp.set_defaults(func=cp)

    parser_cmb = subparsers.add_parser("cmb", description="Combine two existing files into a new file")
    parser_cmb.add_argument("-c", "--confirm", action="store_true", help="Overwrite existing file without confirmation")
    parser_cmb.add_argument("first_filepath", type=Path, help="File path of first source file")
    parser_cmb.add_argument("second_filepath", type=Path, help="File path of second source file")
    parser_cmb.add_argument("dest_filepath", type=Path, help="File path of destination to write new file to, will ask for confirmation if file already exists at the path")
    parser_cmb.set_defaults(func=combine)

    parser_rm = subparsers.add_parser("rm", description="Delete a file")
    parser_rm.add_argument("-c", "--confirm", action="store_true", help="Delete file without confirmation")
    parser_rm.add_argument("filepath", type=Path, help="File path of file to delete, will ask for confirmation before deleting")
    parser_rm.set_defaults(func=remove)

    return parser

def cli(args):
    arg_parser = set_up_arg_parser()
    parsed_args = arg_parser.parse_args(args)
    parsed_args.func(parsed_args)

def main_cli():
    sys_args = sys.argv[1:]
    cli(sys_args)


