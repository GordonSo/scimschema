from setuptools import find_packages, setup


def read(file_name: str) -> str:
    with open(file_name, "r") as fh:
        return fh.read()


def main():
    "Executes setup when this script is the top-level"
    import scimschema as app

    setup(
        name="scimschema",
        version=app.__version__,
        author=app.__author__,
        author_email=app.__author_email__,
        description=app.__description__,
        license=[
            c.rsplit("::", 1)[1].strip()
            for c in app.__classifiers__
            if c.startswith("License ::")
        ][0],
        long_description=read("./README.rst"),
        long_description_content_type="text/x-rst",
        url=app.__url__,
        classifiers=app.__classifiers__,
        packages=find_packages(),
        include_package_data=True,
    )


if __name__ == "__main__":
    main()
