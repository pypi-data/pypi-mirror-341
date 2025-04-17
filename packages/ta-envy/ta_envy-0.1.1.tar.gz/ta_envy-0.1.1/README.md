# envy

**ta-envy** is a minimal, dependency-free environment variable loader for Python.  
It reads `.env` files, validates required variables, and converts values to the correct type.

## 🚀 Features

- ✅ Load variables from `.env` files
- ✅ Required key validation
- ✅ Automatic type conversion (str, int, bool, list)
- ✅ No external dependencies

## 📦 Installation

```bash
uv venv
source .venv/bin/activate
uv pip install .

## Sen package to pypi
uv run  python -m build
twine upload dist/*