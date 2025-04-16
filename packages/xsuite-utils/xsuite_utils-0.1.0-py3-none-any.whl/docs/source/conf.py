# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'XUitl'
copyright = '2025, Kyriacos Skoufaris, Maël Le Garrec'
author = 'Kyriacos Skoufaris, Maël Le Garrec'
release = '0.1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'autoapi.extension',
    'myst_parser',
    'sphinx.ext.mathjax',  # For equations
    'sphinx.ext.viewcode'  # Source links
]
autoapi_dirs = ['../../xutil']  # Auto-generate API docs
autoapi_options = ['members', 'undoc-members', 'show-inheritance']

templates_path = ['_templates']
exclude_patterns = []

language = 'en'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
