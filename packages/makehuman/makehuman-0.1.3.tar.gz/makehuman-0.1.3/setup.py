from setuptools import setup, find_packages

setup(
    name="makehuman",
    version="0.1.3",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["numpy>=1.17.4", "PyQt5>=5.12.8", "PyOpenGL>=3.1.0"],
)
