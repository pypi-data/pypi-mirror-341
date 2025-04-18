# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
def setup(app):
    app.add_css_file('css/custom.css')
project = 'SBGeom'
copyright = '2022, Timo Bogaarts'
author = 'Timo Bogaarts'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ["breathe", "sphinx.ext.mathjax", 'sphinx.ext.autosectionlabel', 'sphinxcontrib.bibtex']
mathjax3_config = {
  
  'loader': {'load': ['[tex]/physics']},
  'tex': {'packages' : {'[+]': ['physics']}, 
            'macros' : {
                        'diff' :'\,\mathrm{d}',
                        'homega':'\hat{\Omega}',
                        'psiarg' : '(\mathbf{r},\hat{\Omega},E)'
                        }

            }
}

numfig = True
math_numfig = True

breathe_default_project = "DEMETER" 
templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



bibtex_bibfiles = ['refs.bib']
# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
