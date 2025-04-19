# AusPostGen

A Python library for generating Australia Post Barcode versions 37, 52, and 67.

## Features

- Generate Australia Post barcodes in various formats
- Support for versions 37, 52, and 67
- High-performance C extension for barcode generation
- Simple Python API

## Installation

```bash
# Using Poetry
poetry add auspostgen

# Using pip
pip install auspostgen
```

## Usage

```python
from auspostgen import write_image

# Generate a barcode image
write_image("output.png", "12345678901234567890", version=37)
```

## Development

1. Clone the repository
2. Install dependencies:
   ```bash
   poetry install
   ```
3. Run tests:
   ```bash
   poetry run pytest
   ```

## Project Structure

```
auspostgen/
├── stampix/
│   ├── __init__.py
│   └── auspostgen/
│       └── _c/
│           ├── __init__.py
│           ├── auspost.c
│           └── Makefile
├── tests/
│   └── __init__.py
├── docs/
├── pyproject.toml
└── README.md
```

## License

MIT License - see LICENSE.txt for details
