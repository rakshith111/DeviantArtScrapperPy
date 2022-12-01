# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import sys
import os

project = 'DeviantArtScrapper'
copyright = '2022, rakshith111'
author = 'rakshith111'
release = '0.0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration


templates_path = ['_templates']
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']

sys.path.insert(0, os.path.abspath('../../src'))


html_theme = 'furo'
pygments_style = "sphinx"
pygments_dark_style = "monokai"
extensions = ['sphinx.ext.autodoc', 'sphinx.ext.viewcode',
              'myst_parser']
autoclass_content = 'both'  # add __init__ to the list of functions to document

# To generate new files in the source folder
# run the command: sphinx-apidoc -o docs-builder/source src
# usage: sphinx-apidoc [OPTIONS] -o <OUTPUT_PATH> <MODULE_PATH> [EXCLUDE_PATTERN, ...]

