from setuptools import setup, find_packages

# For using the README.md file as the project description
with open("README.md", "r") as f:
    description = f.read()

setup(
    name="my_apis",
    version="0.1.0",  # Make sure to update this and the location of the whl file for each modification
    packages=find_packages(),
    install_requires=["pandas", "openai", "requests"],
    # These next two lines are also needed to turn the README.md file into the project description
    long_description=description,
    long_description_content_type="text/markdown",
)
