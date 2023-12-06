"""
cli.py: command line interface for this package
-----------------------------------------------


* Copyright: 2023 Dat Tran
* Authors: Dat Tran (hello@dats.bio)
* Date: 2023-12-06
* Version: 0.0.1


This is part of the mypackage package


License
-------
Proprietary License

"""

from __future__ import annotations
import argparse
from mypackage.cli_handlers import sample_handler


COMMAND_TO_HANDLER = {
    "subcommand": sample_handler,
}


def parse_args():
    # Create the main parser
    parser = argparse.ArgumentParser(description="mypackage cli")

    # Create subparsers
    subparsers = parser.add_subparsers(
        dest="subcommand",
        help="Sub-commands to run with mypackage",
    )

    add_sample_parser(subparsers)

    # Parse the arguments
    args = parser.parse_args()
    return args


def add_sample_parser(subparsers):
    parser = subparsers.add_parser("subcommand", help="TODO")
    parser.add_argument(
        "--opt",
        type=str,
        required=True,
        help="TODO",
    )


def main():
    args = parse_args()
    if args.subcommand in COMMAND_TO_HANDLER:
        COMMAND_TO_HANDLER[args.subcommand](args)
    else:
        commands = "\n".join(list(COMMAND_TO_HANDLER.keys()))
        msg = (
            f"Unsupported subcommand: {args.subcommand}.\n"
            "It seems handler for this command has not been added\n"
            f"mypackage supports the following subcommands:\n"
            f"{commands}"
        )
        raise ValueError(msg)


if __name__ == "__main__":
    main()
