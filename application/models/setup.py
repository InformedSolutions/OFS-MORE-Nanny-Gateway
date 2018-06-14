import setuptools

with open("README", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nanny_models",
    version="0.0.1",
    author="Hugo Geeves",
    author_email="hugo.geeves@informed.com",
    description="A package to abstract all models/serializers for use across the nanny gateway",
    long_description=long_description,
    url="https://github.com/InformedSolutions/OFS-MORE-Nanny-Gateway/nanny_models",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ),
)