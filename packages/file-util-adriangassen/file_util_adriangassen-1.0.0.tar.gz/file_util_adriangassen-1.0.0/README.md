# file-util

file-util is a Python library that performs simple file operations, including:
* file creation
* file copying
* combining two files into a third
* file deletion

## Installation

Use pip to install file-util

Unix
```
python3 -m venv venv
source venv/bin/activate
pip install .
```

Windows
```
python3 -m venv venv
.\venv\Scripts\activate
pip install .
```

### Testing/Development
For running unit tests or active development, use the following installation command:
```
pip install --editable "./[dev]"
```
The package will be updated for each change you make, and install "dev" requirements like pytest.

## Usage

<!-- [[[cog
import argparse
import cog
from file_util_adriangassen.cli import set_up_arg_parser
parser = set_up_arg_parser()
help_text = parser.format_help()
formatted_usage = f"```\n{help_text}\n```"
subparsers_actions = [
    action for action in parser._actions
    if isinstance(action, argparse._SubParsersAction)]
for subparsers_action in subparsers_actions:
    for choice, subparser in subparsers_action.choices.items():
        formatted_usage += f"\n### Subcommand: {choice}\n"
        sub_help_text = subparser.format_help()
        formatted_usage += f"```\n{sub_help_text}\n```"
cog.out(formatted_usage)
]]] -->
```
usage: file-util [-h] {create,cp,cmb,rm} ...

A simple file utility

options:
  -h, --help          show this help message and exit

Subcommands:
  Choose one of the file-util functions from the follow subcommands

  {create,cp,cmb,rm}

```
### Subcommand: create
```
usage: file-util create [-h] [-c] filepath [content ...]

Create a new file, either empty or with content

positional arguments:
  filepath       File path to create new file at, will ask for confirmation if file already exists at the path
  content        Optional: Content to write to new file

options:
  -h, --help     show this help message and exit
  -c, --confirm  Overwrite existing files without confirmation

```
### Subcommand: cp
```
usage: file-util cp [-h] [-c] src_filepath dest_filepath

Copy existing file to another location

positional arguments:
  src_filepath   File path of source file to be copied
  dest_filepath  File path of destination to copy to, will ask for confirmation if file already exists at the path

options:
  -h, --help     show this help message and exit
  -c, --confirm  Overwrite existing file without confirmation

```
### Subcommand: cmb
```
usage: file-util cmb [-h] [-c] first_filepath second_filepath dest_filepath

Combine two existing files into a new file

positional arguments:
  first_filepath   File path of first source file
  second_filepath  File path of second source file
  dest_filepath    File path of destination to write new file to, will ask for confirmation if file already exists
                   at the path

options:
  -h, --help       show this help message and exit
  -c, --confirm    Overwrite existing file without confirmation

```
### Subcommand: rm
```
usage: file-util rm [-h] [-c] filepath

Delete a file

positional arguments:
  filepath       File path of file to delete, will ask for confirmation before deleting

options:
  -h, --help     show this help message and exit
  -c, --confirm  Delete file without confirmation

```
<!-- [[[end]]] -->

## Running Unit Tests

Unit tests are implemented with Pytest. [Use this command](#testingdevelopment) to install file-util for testing or development.

```
pytest tests/
```

## Uploading

Based off https://packaging.python.org/en/latest/tutorials/packaging-projects/

### TestPyPi

```
python3 -m pip install --upgrade pip build twine
python3 -m pip install . # to install file-util
python3 -m build
python3 -m twine upload --repository testpypi --config <path_to_.pypirc> dist/*
```

### PyPi

```
python3 -m pip install --upgrade pip build twine
python3 -m pip install . # to install file-util
python3 -m build
python3 -m twine upload <path_to_.pypirc> dist/*
```

## Updating this README

This README uses [cog](https://cog.readthedocs.io/en/latest/) to insert the help text of file-util into the [Usage](#usage) section. After making updates to file-util's arguments or help text, install cog and update this documentation:

```
pip install cogapp
cog -r README.md
```

## License

This project is licensed under the terms of the MIT license.


