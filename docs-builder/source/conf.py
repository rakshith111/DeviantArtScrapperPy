
import sys
import os

project = 'DeviantArtScrapper'
copyright = '2023, rakshith111'
author = 'rakshith111'
release = '0.1.2'

# add the path to the source folders
sys.path.insert(0, os.path.abspath('../../src'))
sys.path.insert(0, os.path.abspath('../../src/libs'))

templates_path = ['_templates']
html_static_path = ['_static']

exclude_patterns = []
# add mock imports since we don't have the dependencies installed when building docs and we have imported modules in the same folder
autodoc_mock_imports = ["urlextractor"]

# add the extensions
extensions = ['sphinx.ext.autodoc', 'sphinx.ext.viewcode',
              'myst_parser', ]
html_theme = 'furo'
pygments_style = "sphinx"
pygments_dark_style = "monokai"

# add __init__ to the folder of files to add into documentation
autoclass_content = 'both'


# Installation
# pip install -U sphinx myst_parser furo rst-to-myst[sphinx]
# To generate new files in the source folder (Gen rst for files )
# run the command: sphinx-apidoc -o docs-builder/source src
# usage: sphinx-apidoc [OPTIONS] -o <OUTPUT_PATH> <MODULE_PATH> [EXCLUDE_PATTERN, ...]
