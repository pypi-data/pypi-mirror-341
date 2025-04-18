import json
import sys
from pathlib import Path
from setuptools import setup, find_packages


config_json_path = Path(__file__).parent.joinpath("config.json")

def read_version():
    try:
        with open(config_json_path, "r") as json_data:
            config = json.load(json_data)
            return config["version"]
    except Exception as e:
        print(f"Error loading version from '{config_json_path}': {e}", file=sys.stderr)
        sys.exit(1)

setup(
    name="pypi_ci_package",
    version=read_version(),
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=["twine"],
    entry_points={
        "console_scripts": ["cli=src.cli:main"],
    },
)