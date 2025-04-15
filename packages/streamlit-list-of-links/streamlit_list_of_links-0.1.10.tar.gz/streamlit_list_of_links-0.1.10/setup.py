from pathlib import Path

import setuptools

__version__ = "0.1.10"

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setuptools.setup(
    name="streamlit-list-of-links",
    version=__version__,
    author="Marc Argent",
    author_email="margent@gmail.com",
    description="Streamlit component that renders a list of links",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[],
    python_requires=">=3.10",
    install_requires=[
        "streamlit >= 1.43.0",
    ],
    extras_require={
        "tests": [
            "wheel",
            "pytest==7.4.0",
            "playwright==1.48.0",
            "requests==2.31.0",
            "pytest-playwright-snapshot==1.0",
            "pytest-rerunfailures==12.0",
        ],
    }
)
