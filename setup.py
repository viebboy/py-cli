import setuptools
from mypackage.version import __version__


setuptools.setup(
    name="mypackage",
    version=__version__,
    author="Dat Tran",
    author_email="hello@dats.bio",
    description="mypackage-description",
    long_description="mypackage-description",
    long_description_content_type="text",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Operating System :: POSIX",
    ],
    entry_points={
        "console_scripts": [
            "mypackage = mypackage.cli:main",
        ]
    },
)
