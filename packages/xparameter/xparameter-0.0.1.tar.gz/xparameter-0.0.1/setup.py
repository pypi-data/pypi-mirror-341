import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="xparameter",
    version="0.0.1",
    author="Shangyu Liu",
    author_email="liushangyu@sjtu.edu.cn",
    description="A portable configuration tool to manage hyperparameters and settings of your experiments.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ThomasAtlantis/xparameter",
    python_requires='>=3.7',
    install_requires=[
        "rich-argparse>=1.7.0",
    ],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)