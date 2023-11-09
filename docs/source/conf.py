# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import os
import sys

# Указываем путь до root-папки проекта Django
# Путь относительно файла conf.py
sys.path.insert(0, os.path.abspath('./../../'))

project = 'TRPO-project'
copyright = '2023, Kate Marhytina, Leonid Chashkin, Kirill Padalitsa, Alex Stepchenko'
author = 'Kate Marhytina, Leonid Chashkin, Kirill Padalitsa, Alex Stepchenko'
release = '1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc'
]

templates_path = ['_templates']
exclude_patterns = []

language = 'TRPO-project'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']
