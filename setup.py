import setuptools

with open("README.rstrst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="scimschema",
    version="0.0.1",
    author="Gordon So",
    author_email="gordonkwso@gmail.com",
    description="A validator for System for Cross-domain Identity Management (SCIM) responses given predefine schemas",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/GordonSo/pyscim",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)