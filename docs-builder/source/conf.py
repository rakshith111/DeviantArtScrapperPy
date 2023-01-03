
import sys
import os

project = 'DeviantArtScrapper'
copyright = '2022, rakshith111'
author = 'rakshith111'
release = '0.0.2'


sys.path.insert(0, os.path.abspath('../../src'))
sys.path.insert(0, os.path.abspath('../../src/libs'))

templates_path = ['_templates']
html_static_path = ['_static']

exclude_patterns = []
# add mock imports since we don't have the dependencies installed when building docs and we have imported modules in the same folder
autodoc_mock_imports = ["urlextractor"]




extensions = ['sphinx.ext.autodoc', 'sphinx.ext.viewcode',
              'myst_parser']

html_theme = 'furo'
pygments_style = "sphinx"
pygments_dark_style = "monokai"

autoclass_content = 'both'  # add __init__ to the list of functions to document

# To generate new files in the source folder
# run the command: sphinx-apidoc -o docs-builder/source src
# usage: sphinx-apidoc [OPTIONS] -o <OUTPUT_PATH> <MODULE_PATH> [EXCLUDE_PATTERN, ...]
#pip install -U sphinx myst_parser furo
