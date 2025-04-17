# setup.py
from setuptools import setup, find_packages

setup(
    name="insafeConnectToDatabase",  # Name of your package
    version="0.3.0",  # Version of your package
    description="A utility to determine the type of permit based on ID",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="khaled.jabari",
    author_email="khaled.jabari@cntxt.com",
    url="https://github.com",  # Replace with your repo link
    package_dir={"": "src"},
    packages=find_packages(where="src"),  # Automatically find all packages
    include_package_data=True,  # Ensures non-Python files are included
    package_data={
        'insafeConnectToDatabase': ['cloud-sql-proxy'],  # Include the script
    },
    install_requires=[
        "pydantic>=1.10.0",  # Add any dependencies here
        "psycopg2",  # Add psycopg2 dependency
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
