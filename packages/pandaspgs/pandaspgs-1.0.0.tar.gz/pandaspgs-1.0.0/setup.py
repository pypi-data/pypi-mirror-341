import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pandaspgs",
    version="1.0.0",
    author="Cao Tianze",
    author_email="hnrcao@qq.com",
    description="A Python package for easy retrieval of Polygenic Score Catalog data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tianzelab/pandaspgs",
    project_urls={
        "Bug Tracker": "https://github.com/tianzelab/pandaspgs/issues",
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=['pandaspgs'],
    python_requires=">=3.11",
    install_requires=['pandas>=2.1.4', 'requests>=2.31.0', 'progressbar2>=4.4.2', 'cachetools>=5.3.3'],
    license="MIT",
    keywords=['pgs', 'genomics', 'snp', 'bioinformatics','pandas'],
    package_data={
        "": ["*.csv","*.txt"]
    }
)
