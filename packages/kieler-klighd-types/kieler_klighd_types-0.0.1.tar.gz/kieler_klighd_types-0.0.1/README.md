# KLighD Python Types
This project holds automatically generated types that can be used to implement language servers that can speak the language server protocol variant understood by [klighd](https://github.com/kieler/klighd-vscode).

## Getting Started
Setup a virtual environment and install the required packages.
```
python -m venv ls-env
source ls-env/bin/activate
pip install -r requirements.txt
```

## Generating the KGraph data structure from schema
The schema is defined in [klighd-vscode](https://github.com/kieler/klighd-vscode/tree/main/schema/SKGraphSchema.json).

The generated types are committed in this repository to be published as a python package. If the schemas are updated they can be rebuilt using the `rebuild_types.sh` build script.
For this to work the initial setup under getting started has to have been done.

## Releasing Python package
**TODO**
