import setuptools

setuptools.setup(
    name="si-clad",
    version="0.0.2",
    author="Nguyen Thi Minh Phu",
    author_email="phunguyenthiminh.hm@gmail.com",
    description="This package provides a Statistical Inference framework for testing the anomaly results obtained by DBSCAN algorithm.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ntmphu/SI-CLAD",
    packages=["si_clad"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires = [
    "mpmath",
    "numpy>=1.23.0",
    "scipy>=1.4.1",
    ],
)
