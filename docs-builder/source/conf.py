# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import sys
import os
import glob
import subprocess
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
              'myst_parser', 'sphinx.ext.napoleon']
autoclass_content = 'both' #add __init__ to the list of functions to document


def setup(app):
    """Run some additional steps after the Sphinx builder is initialized"""

    app.connect('builder-inited', convert)

# Creates backup and converts all .rst files to .md


def convert(app):
    for file in (glob.glob(os.path.join(os.getcwd()+'\docs\source\*.rst'))):
        print("Converting", file)

        subprocess.run(["copy", f"{file}",f"{file}.bak"], shell=True)
        subprocess.run(["rst2myst", "convert",f"{file}"], shell=True)
        subprocess.run(["del", f"{file}", ], shell=True)
