import sys
import argparse
from pathlib import Path
from palgen.readers.pal_reader import PalReader
from palgen.db.sql import save_pals_to_db

def generate_command(args):
    """Generate Pal database from game data files."""
    try:

        # Input path handling.
        input_path = Path(args.input_path) if args.input_path else Path('.data')
        if not input_path.exists():
            # TODO: add a logger.
            sys.exit(1)

        # Output path handling.
        output_path = Path(args.output_path) if args.output_path else Path('output')
        output_path.mkdir(parents=True, exist_ok=True)

        reader = PalReader(str(input_path))
        data = reader.read()

        save_pals_to_db(data, str(output_path))

    except Exception as e:
        sys.exit(1)

def main():
    """Main entry point for the PalGen CLI."""
    parser = argparse.ArgumentParser(
        prog="palgen",
        description="PalGen - Palworld data generation and management tool."
    )

    """Basic CLI arguments."""
    # Verbose output.
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output."
    )

    # Log level configuration.
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "TRACE"],
        default="INFO",
        help="Set the logging level (default: INFO)."
    )

    """Subcommands"""
    subparsers = parser.add_subparsers(dest="command", help="Available commands", metavar="COMMAND")  # noqa: F841

    """Subcommand: [generate]"""
    generate_parser = subparsers.add_parser(
        "generate",
        help="Generate Pal database from game data files."
    )

    generate_parser.add_argument(
        "--input_path", "-i",
        help="Path to the input data files."
    )

    generate_parser.add_argument(
        "--output_path", "-o",
        help="Path to the output database file."
    )

    generate_parser.set_defaults(func=generate_command)

    """=== === === ==="""
    args = parser.parse_args()

    # log_level = "DEBUG" if args.verbose else args.log_level

    if not args.command:
        parser.print_help()
        sys.exit(1)

    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
