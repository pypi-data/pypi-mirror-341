"""
Script d'installation pour EndoriumUtils
"""

import os
from setuptools import setup, find_packages

# Lire la description longue depuis README.md
try:
    with open("README.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()
except FileNotFoundError:
    # Fallback si README.md n'est pas trouvé
    long_description = """
    EndoriumUtils - Bibliothèque d'utilitaires réutilisables pour les projets Endorium
    
    Ce module fournit des fonctionnalités communes pour la gestion des logs et des versions.
    """

setup(
    name="EndoriumUtils",
    version="1.0.0",
    author="Energetiq",
    author_email="energetiq@outlook.com",
    description="Utilitaires communs pour les projets Endorium",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/NergYR/EndoriumUtils",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
