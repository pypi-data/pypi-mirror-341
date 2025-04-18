import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="innov8r",
    version="5.0.2",
    author="Shivkumar Chauhan",
    author_email="sksinghat95@gmail.com",
    description="Python-based GUI application designed to streamline software development workflows with innovative tools and utilities. It provides developers with an intuitive and user-friendly interface for building efficient and scalable solutions",
    long_description=long_description,
    include_package_data=True,
        package_data={
        'innov8r': [
            'res/*',
            'res/libraries/*',
        ]
    },

    long_description_content_type="text/markdown",
    url="https://github.com/TechForEverybody/Innov8r-IDE",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)