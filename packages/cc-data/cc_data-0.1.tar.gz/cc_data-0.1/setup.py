from setuptools import setup, find_packages

setup(
    name="cc_data",
    version="0.1",
    description="A package with data files for AI practicals",
    author="Your Name",
    packages=find_packages(),  # This will find 'ai_data' automatically
    include_package_data=True,  # Ensures data files are included
    package_data={
        "lib_hck": ["data/*"],  # Includes all files in the data folder
    },
    install_requires=[
        # List any required packages here, e.g., pandas, numpy
    ],
)
