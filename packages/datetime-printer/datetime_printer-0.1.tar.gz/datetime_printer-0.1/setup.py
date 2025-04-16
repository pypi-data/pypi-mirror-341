from setuptools import setup, find_packages

setup(
    name="datetime_printer",
    version="0.1",
    package_dir={"": "src/main/python"},
    packages=find_packages(where="src/main/python"),
    install_requires=[],
    entry_points={
        "console_scripts": ["print-datetime=python.dx_lib:print_datetime"],
    },
    author="DX",
    description="A simple package to print system date and time",
    url="https://github.com/mondi-group/DX_Library",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
