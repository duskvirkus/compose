# Contributing

## Setup Unit Testing

```
pip install -U pytest
```

## Building Docs

```
pip install -r docs/requirements.txt
sphinx-apidoc -f -o docs/source ./compose
sphinx-autobuild docs docs/_build/html
```