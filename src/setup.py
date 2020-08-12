from setuptools import setup, find_packages

with open("./README.rst", "r") as fh:
    long_description = fh.read()

setup(
    name="scimschema",
    version="0.1.69",
    author="Gordon So",
    author_email="gordonkwso@gmail.com",
    description="A validator for System for Cross-domain Identity Management (SCIM) responses given predefine schemas",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/GordonSo/pyscim",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    include_package_data=True,
)
