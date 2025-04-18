from setuptools import setup, find_packages

setup(
    name="smartreq",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        "console_scripts": [
            "smartreq = smartreq.cli:main"
        ]
    },
    author="Your Name",
    description="CLI tool to auto-generate requirements.txt with exact versions",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.7",
)
