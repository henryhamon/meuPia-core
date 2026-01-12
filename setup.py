# setup.py no repositório do meuPia
from setuptools import setup, find_packages

setup(
    name="meupia-core",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        # Dependências do core (se houver)
    ],
    entry_points={
        'console_scripts': [
            'mpgp=meuPia.tools.mpgp:main',
            'meupia=meuPia.compiler:main',
        ],
    },
)