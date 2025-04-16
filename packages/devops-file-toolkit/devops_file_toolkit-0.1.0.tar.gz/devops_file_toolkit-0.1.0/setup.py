from setuptools import setup, find_packages

setup(
    name="devops-file-toolkit",
    version="0.1.0",
    description="A toolkit for Dockerfile optimization and Kubernetes YAML linting",
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    author="Jyotindra KT",
    author_email="jyotindrakt21@gmail.com",
    url="https://github.com/JaguarsCodehub/devops-toolkit",  # Change to your project URL
    packages=find_packages(include=["devops_toolkit", "devops_toolkit.*"]),
    install_requires=[
        "PyYAML",
        "argparse",
    ],
    entry_points={
        "console_scripts": [
            "devops-toolkit=devops_toolkit.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
