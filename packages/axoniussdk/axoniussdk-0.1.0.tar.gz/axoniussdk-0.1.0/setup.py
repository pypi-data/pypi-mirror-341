from setuptools import setup, find_packages

setup(
    name="axoniussdk",
    version="0.1.0",
    author="Axonius Publisher",
    author_email="package-publisher@axonius.com",
    description="Axonius SDK placeholder package",
    long_description="This is a placeholder package for Axonius SDK.",
    long_description_content_type="text/markdown",
    url="https://github.com/axonius/axoniussdk",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
