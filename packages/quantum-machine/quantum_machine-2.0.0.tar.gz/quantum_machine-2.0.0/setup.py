from setuptools import setup, find_packages

# Read README.md for long_description
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="quantum-machine",
    version="2.0.0",
    packages=find_packages(),
    install_requires=[
        "typer",
        "rich"
    ],
    entry_points={
        "console_scripts": [
            "quantum=quantum.main:app"
        ]
    },
    author="Nitinkumar Suvagiya",
    author_email="itsupport@quantumdatalytica.com",
    description="Quantum-CLI: A powerful CLI to build, run, and test Quantum Machines.",
    long_description=long_description,
    long_description_content_type="text/markdown",  # ✅ Supports Markdown rendering
    url="https://github.com/QuantumDatalytica-LLC/quantum-cli.git",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)