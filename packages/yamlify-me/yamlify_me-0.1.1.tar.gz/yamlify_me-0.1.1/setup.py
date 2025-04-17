from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="yamlify-me",
    version="0.1.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=["markdown", "pyyaml", "Jinja2"],
    entry_points={
        "console_scripts": [
            "yamlify=yamlify:main",
        ],
    },
)
