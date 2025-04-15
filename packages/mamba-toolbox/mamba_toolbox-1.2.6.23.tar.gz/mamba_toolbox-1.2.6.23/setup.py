import re
from setuptools import setup, find_packages

mainfile = open('mamba/__init__.py', 'r', encoding='utf-8').read()
appversion = [v.strip() for v in re.search(r'__version__\s*=\s*\(\s*(\d+\s*,\s*\d+\s*,\s*\d+\s*,\s*\d+)\s*\)', mainfile).group(1).split(',')]

setup(
    name="mamba_toolbox",
    version=".".join(appversion),
    description="Mambalib toolbox",
    install_requires=['click==8.1.7', 'requests==2.31.0', 'virtualenv==20.25.0'],
    packages=find_packages(),
    entry_points={
        'console_scripts':[
            'mamba = mamba.__main__:cli'
        ]
    }
)