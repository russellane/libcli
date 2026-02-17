# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build Commands

This project uses PDM for dependency management and Make for build automation.

```bash
# Install dependencies
pdm install

# Run all checks (lint + test)
make build

# Linting
make lint          # black + isort + flake8 + mypy
make black         # format code
make isort         # sort imports
make flake8        # linting
make mypy          # type checking

# Testing
make test          # run pytest with coverage (90% threshold)
make pytest_debug  # run pytest with --capture=no for debugging

# Run a single test
python -m pytest tests/test_basecli.py::test_help -v
```

## Architecture

libcli is a CLI framework built on argparse that provides colorized help, markdown output, logging integration, config file support, and shell completion.

### Core Classes

- **BaseCLI** (`libcli/basecli.py`): Main class for single-command applications. Subclass and implement `init_parser()`, `add_arguments()`, and `main()`.

- **BaseCmd** (`libcli/basecmd.py`): Base class for subcommands. Subclass and implement `init_command()` and `run()`. Register with `cli.add_subcommand_classes([...])` or `cli.add_subcommand_modules("pkg.commands")`.

### Extension Points

- `libcli/actions/`: Custom argparse actions for help formatting (BaseHelpAction, LongHelpAction, MarkdownHelpAction)
- `libcli/options/`: Custom option handlers (completion, print-config, print-url)
- `libcli/formatters/`: Help formatters (ColorHelpFormatter, MarkdownHelpFormatter)

### Constructor Flow

BaseCLI.__init__ calls in order: `init_config()` → `init_parser()` → `set_defaults()` → `add_arguments()` → parse args

## Code Style

- Line length: 97 characters
- Type hints required (mypy strict mode)
- Google-style docstrings (pydocstyle)
