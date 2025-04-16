from setuptools import setup, find_packages

setup(
    name="textura",
    version="1.1.0",
    author="imAnesYT",
    author_email="imanesytdev.contact@gmail.com",
    description="Terminal text styling made simple, like colorama but cooler.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/imAnesYT/textura",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[],
    include_package_data=True,
    package_data={
        'textura': ['README.md'],
    },
)