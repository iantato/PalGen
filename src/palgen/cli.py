import sys
import argparse
from pathlib import Path
from colorama import Fore, Style
from loguru import logger
from palgen.readers.pal_reader import PalReader
from palgen.readers.combiunique_reader import CombiUniqueReader
from palgen.db.sql import save_pals_to_db, save_unique_combinations_to_db
from palgen.logger import setup_logging

class CustomHelpFormatter(argparse.HelpFormatter):
    """Custom help formatter to adjust the layout of the help message.

    Programmed with the help of reading the `argparse` documentation.
    https://github.com/python/cpython/blob/2.7/Lib/argparse.py

    This is also heavily inspired by the `uv` command line tool's
    custom help format. https://github.com/astral-sh/uv
    """

    HEADER_COLOR = f'{Fore.LIGHTGREEN_EX}{Style.BRIGHT}'
    MAIN_COMM_COLOR = f'{Fore.CYAN}{Style.BRIGHT}'
    OTHER_COLOR = f'{Fore.CYAN}'

    COMMANDS_HELP_SPACING = 25

    def __init__(self, prog):
        super().__init__(prog, max_help_position=30, width=80)

    def _format_usage(self, usage, actions, groups, prefix):
        """Override to add custom styling to the usage line."""
        if prefix is None:
            prefix = f'{self.HEADER_COLOR}Usage: {Style.RESET_ALL}'

        if hasattr(self, '_prog') and ' ' in self._prog:
            prog_parts = self._prog.split(' ')
            base_prog = f'{self.MAIN_COMM_COLOR}{prog_parts[0]}{Style.RESET_ALL}'
            sub_prog = f'{self.MAIN_COMM_COLOR}{prog_parts[1]}{Style.RESET_ALL}'
            options_text = ''
            if any(action.option_strings for action in actions):
                options_text = f' {self.OTHER_COLOR}[OPTIONS] <COMMAND>{Style.RESET_ALL}'

            return f'{prefix}{base_prog} {sub_prog}{options_text}\n'
        else:
            prog = f'{self.MAIN_COMM_COLOR}{self._prog}{Style.RESET_ALL}'
            options_text = ''
            if any(action.option_strings for action in actions):
                options_text = f' {self.OTHER_COLOR}[OPTIONS] <COMMAND>{Style.RESET_ALL}'

            return f'{prefix}{prog}{options_text}\n'

    def _format_commands(self, action):
        """Format subcommands in a custom way."""
        commands = []
        for name, subparser in action.choices.items():
            formatted_name = f'{self.MAIN_COMM_COLOR}{name}{Style.RESET_ALL}'
            help_text = subparser.description or ''

            commands.append(f'\n  {formatted_name}{" " * (self.COMMANDS_HELP_SPACING - len(formatted_name))}{help_text}')

        return ''.join(commands) + '\n'

    def _format_action(self, action):
        """Override to customize option formatting."""
        if isinstance(action, argparse._SubParsersAction):
            return self._format_commands(action)

        if action.option_strings:
            options = []
            for option in action.option_strings:
                options.append(f'{self.MAIN_COMM_COLOR}{option}{Style.RESET_ALL}')

            action_header = ', '.join(options) + (f'{self.OTHER_COLOR} <CHOICES>{Style.RESET_ALL}' if action.choices else '')
            help_text = self._expand_help(action) if action.help else ''

            if help_text:
                return f'  {action_header}\n     {help_text}\n'
            else:
                return f'  {action_header}\n'

    def format_help(self):
        """Override to add custom styling."""
        help_text = super().format_help()
        if len(help_text.splitlines()) > 1:
            description = f'{help_text.splitlines()[1]}\n\n'
            help_text = help_text.replace(description, '')
            help_text = description + help_text

        # Section Headers
        help_text = help_text.replace('options:',
                                      f'\n{self.HEADER_COLOR}Global options:{Style.RESET_ALL}')

        help_text = help_text.replace('Commands:\n',
                                      f'{self.HEADER_COLOR}Commands:{Style.RESET_ALL}')

        return help_text

def generate_command(args):
    """Generate Pal database from game data files."""
    try:
        # Input path handling.
        input_path = Path(args.input_path) if args.input_path else Path('.data')
        if not input_path.exists():
            logger.error(f"Input path '{input_path}' does not exist.")
            sys.exit(1)

        # Output path handling.
        output_path = Path(args.output_path) if args.output_path else Path('output')
        output_path.mkdir(parents=True, exist_ok=True)

        readers = list([])

        if args.pal or args.all:
            readers.append('pals')
        if args.combi_unique or args.all:
            readers.append('combi_unique')
        if not readers:
            readers = ['pals', 'combi_unique']

        logger.info(f"Generating Pal database with readers {', '.join(readers)}...")

        if 'pals' in readers:
            pal_reader = PalReader(str(input_path))
            pals = pal_reader.read()
            logger.info(f"Read {len(pals)} Pal objects from '{input_path}'")

            save_pals_to_db(pals, str(output_path))
            logger.info(f"Pal database generated successfully at '{output_path}/pals.db'")

        if 'combi_unique' in readers:
            reader = CombiUniqueReader(str(input_path))
            data = reader.read()
            logger.info(f"Read {len(data)} unique combinations from '{input_path}'")

            save_unique_combinations_to_db(data, str(output_path))
            logger.info(f"Combi Unique database generated successfully at '{output_path}/pals.db'")

    except Exception as e:
        logger.error(f"An error occurred while generating the Pal database: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        prog='palgen',
        description='PalGen CLI - Generate Pal databases from game data files.',
        formatter_class=CustomHelpFormatter
    )

    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable debug mode.'
    )

    """Subparsers"""
    subparsers = parser.add_subparsers(title='Commands', dest='command', metavar='')

    generate_parser = subparsers.add_parser(
        name='generate',
        description='Generate a Pal database from game data files.',
        formatter_class=CustomHelpFormatter
    )
    generate_parser.add_argument(
        '-i', '--input_path',
        help='Path to the input data files.'
    )
    generate_parser.add_argument(
        '-o', '--output_path',
        help='Path to the output database file.'
    )

    generate_parser.add_argument(
        '-p', '--pal',
        action='store_true',
        help='Generate Pal database.'
    )
    generate_parser.add_argument(
        '-c', '--combi_unique',
        action='store_true',
        help='Generate Combi Unique database.'
    )
    generate_parser.add_argument(
        '-a', '--all',
        action='store_true',
        help='Generate both Pal and Combi Unique databases.'
    )

    generate_parser.set_defaults(func=generate_command)

    args = parser.parse_args()
    log_level = "DEBUG" if args.verbose else "INFO"
    setup_logging(log_level)

    if not args.command:
        parser.print_help()
        sys.exit(1)

    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == '__main__':
    main()
