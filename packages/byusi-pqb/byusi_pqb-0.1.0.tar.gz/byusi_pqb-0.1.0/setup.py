from setuptools import setup, find_packages

setup(
    name="byusi-pqb",
    version="0.1.0",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "rich>=12.5.1",
    ],
    entry_points={
        "console_scripts": [
            "pqb = pqb.cli:main",
        ],
    },
    python_requires=">=3.8",
)