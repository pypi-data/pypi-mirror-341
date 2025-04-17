from setuptools import setup, find_packages

setup(
    name="makehuman",
    version="1.3.2",
    packages=find_packages(),
    package_data={
        "makehuman": [
            "data/*",
            "lib/*",
            "apps/*",
            "shared/*",
            "apps/gui/*",
            "core/*",
            "plugins/*",
            "licenses/*",
            "*.py",
        ],
    },
    install_requires=[
        "numpy>=1.17.4",
        "PyQt5>=5.12.8",
        "PyOpenGL>=3.1.0",
    ],
    entry_points={
        "console_scripts": [
            "makehuman=makehuman.test:start_app",
        ],
    },
    python_requires=">=3.6",
)
