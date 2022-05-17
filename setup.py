# -*- coding: utf-8 -*-

"""The setup script."""

import sys
from setuptools import setup, find_packages

requirements = [
    'taurus',
    'Click'
]

with open("README.md") as f:
    description = f.read()

setup(
    name="bpm_gui",
    author="Saida Humbert Fernanez",
    author_email="shumbert@axt.email",
    version="1.0.0",
    description="EPS USER GUI",
    long_description=description,
    long_description_content_type="text/markdown",
    entry_points={
        "console_scripts": [
            "epsusergui = EPSUserGui.epsusergui:cli",
        ]
    },
    install_requires=requirements,
    include_package_data=True,
    classifiers=[
        "Natural Language :: English",
        "Intended Audience :: Developers",
        "Development Status :: 2 - Pre-Alpha",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)'
    ],
    license="LGPLv3",
    keywords="epsusergui",
    packages=find_packages(),
    url="https://git.cells.es/controls/eps-gui",
    project_urls={
        "Documentation": "https://git.cells.es/controls/eps-gui",
        "Source": "https://git.cells.es/controls/eps-gui"
    }
)
