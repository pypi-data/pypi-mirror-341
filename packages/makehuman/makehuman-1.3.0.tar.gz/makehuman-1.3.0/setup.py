from setuptools import setup, find_packages

setup(
    name="makehuman",
    version="1.3.0",
    packages=find_packages(),
    package_data={
        'makehuman': ['data/*', 'lib/*', 'apps/*', 'shared/*', 'apps/gui/*', 'core/*'],
    },
    install_requires=[
        'numpy',
        'PyQt5',
    ],
    entry_points={
        'console_scripts': [
            'makehuman=makehuman.makehuman:main',
        ],
    },
)

