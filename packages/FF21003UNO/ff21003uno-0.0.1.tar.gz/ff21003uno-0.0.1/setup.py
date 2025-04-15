import pathlib
from setuptools import find_packages, setup

HERE = pathlib.Path(__file__).parent

VERSION = '0.0.1'
PACKAGE_NAME = 'FF21003UNO'
AUTHOR = 'Sofia Franco'
AUTHOR_EMAIL = 'ff21003@ues.edu.sv'
URL = 'https://github.com/ff21003/FF21003UNO'
LICENSE = 'MIT'
DESCRIPTION = 'Librería para resolver sistemas de ecuaciones lineales y no lineales'
LONG_DESCRIPTION = (HERE / "README.md").read_text(encoding='utf-8')
LONG_DESC_TYPE = "text/markdown"

INSTALL_REQUIRES = [
    'numpy',  # Para operaciones numéricas
    'scipy',  # Para métodos avanzados como LU
]

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type=LONG_DESC_TYPE,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    install_requires=INSTALL_REQUIRES,
    license=LICENSE,
    packages=find_packages(),
    include_package_data=True,
)
