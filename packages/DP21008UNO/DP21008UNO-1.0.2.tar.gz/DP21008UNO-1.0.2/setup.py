import pathlib
from setuptools import find_packages, setup

HERE = pathlib.Path(__file__).parent

VERSION = '1.0.2'
PACKAGE_NAME = 'DP21008UNO'
AUTHOR = 'Julio Cesar Davila Peñate'
AUTHOR_EMAIL = 'dp21008@ues.edu.sv'
URL = 'https://github.com/dp21008/DP21008UNO.git'

LICENSE = 'MIT'
DESCRIPTION = 'Librería para resolver sistemas de ecuaciones lineales con multiples metodos y ecuaciones de orden superior con biseccion'
LONG_DESCRIPTION = (HERE / "README.md").read_text(encoding='utf-8')
LONG_DESC_TYPE = "text/markdown"


#Paquetes necesarios para que funcione la libreía. Se instalarán a la vez si no lo tuvieras ya instalado
INSTALL_REQUIRES = [
      'numpy'
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
    include_package_data=True
)