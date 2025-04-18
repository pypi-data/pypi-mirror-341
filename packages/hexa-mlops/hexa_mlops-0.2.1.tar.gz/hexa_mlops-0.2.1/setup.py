from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()
setup(
    name='hexa_mlops',
    version='0.2.1',
    author="Thi Thuy Duyen Pham, Liam Mulhall",
    author_email="irene.d.pham@gmail.com, lmulhall@amadeus.com",
    packages=find_packages(where='src'),
    description='Hexa MLOps package',
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_dir={'': 'src'},
    install_requires=[
        'pyyaml',
        'python-dotenv',
        'Jinja2',
    ],
    entry_points={
        'console_scripts': [
            'hexa=hexa_mlops.cli:main',
        ],
    },  
)