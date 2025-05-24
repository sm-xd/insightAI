# Tree-sitter Grammars

This directory will contain compiled Tree-sitter grammar files for different programming languages.

## Supported Languages

- Python (.so file will be generated here)
- JavaScript (.so file will be generated here)
- TypeScript (.so file will be generated here)

## Building the Grammars

To build the grammars, you'll need to run the build script:

```bash
# From project root
python -m scripts.build_grammars
```

The build script will:

1. Clone the necessary Tree-sitter grammar repositories
2. Build the shared libraries (.so files)
3. Place them in this directory

## Adding a New Grammar

To add support for a new language:

1. Add the grammar repository URL to `scripts/build_grammars.py`
2. Create a corresponding parser in `parsers/languages/`
3. Register the parser in `parsers/parser_registry.py`

## Note on Grammar Files

The `.so` files are not included in the repository and need to be built locally. 
The build script will automatically download and build them for your platform.