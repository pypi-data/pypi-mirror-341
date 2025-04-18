# EyeLiner

Creates a pip package from the [EyeLiner](https://github.com/QTIM-Lab/EyeLiner) project.

## Manual Deployment

To manually deploy the package to PyPi, run the following commands:

1. Create [PyPI](https://pypi.org/) account online.
2. Clone the repo:
```
git clone git@github.com:QTIM-Lab/eyeliner_reg.git
```
3. Create virtual environment running python 3.10.4 and run `poetry install`.
4. Perform tests to ensure code is running with no execution errors: `poetry run pytest`
5. Build the package by running `poetry build`
7. Generate PyPI token
8. Configure poetry with organization's PyPI token:
```
poetry config pypi-token.pypi "your-organization-api-token"
```
9. Publish by running `poetry publish`

You should be able to pip install eyeliner and run it as a package in your python script or even as a command-line interface (CLI) command. Try the following:

As a python package:

```bash
# Create a new environment for testing
python -m venv test_env
source test_env/bin/activate  # On Windows: test_env\Scripts\activate

# Install your package
pip install dist/eyeliner-0.1.0-py3-none-any.whl --force-reinstall

# Test imports and functionality
python -c "from eyeliner import EyeLinerP; print('Import successful!')"
```

As a CLI command:

```bash
eyeliner --fixed-input assets/image_0_vessel.jpg --moving-input assets/image_1_vessel.jpg --moving-image assets/image_1.jpg --reg affine --save affine.png --device cuda:0
```