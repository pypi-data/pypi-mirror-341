#!/bin/bash

# python -m pip install --upgrade pip
# pip install twine hatch numpy poetry pytest setuptools wheel
# pip install twine

rm -rf ./dist
hatch build

pip install .
pytest ./tests --junitxml=python-report.xml

# twine upload --repository-url "https://pypi.org/project/motoko-cli/" ./dist/*
# twine upload ./dist/*
# echo "twine upload -u '$TWINE_USERNAME' -p '$TWINE_PASSWORD' ./dist/*"
# twine upload -u "$TWINE_USERNAME" -p "$TWINE_PASSWORD" ./dist/*
