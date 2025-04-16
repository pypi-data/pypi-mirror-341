from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name="geomapclip",
    version="0.0.1",
    packages=find_packages(),
    description="",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/junghawoo/GeoMapCLIP",
    author="Jungha Woo",
    author_email="wooj@purdue.edu",
    license="MIT",
    install_requires=requirements,
    include_package_data=True,
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
 
