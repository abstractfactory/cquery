# -*- coding: utf-8 -*-

import sys
import os

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.viewcode',
    'sphinx.ext.autodoc',
    'sphinxcontrib.napoleon',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix of source filenames.
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = u'cQuery'
copyright = u'2014, Marcus Ottosson'

# The short X.Y version.
version = '0.0'
# The full version, including alpha/beta/rc tags.
release = '0.0.1'

exclude_patterns = []

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'


# -- Options for HTML output ----------------------------------------------

if os.environ.get('READTHEDOCS', None) != 'True':
    try:
        import sphinx_rtd_theme
        html_theme = 'sphinx_rtd_theme'
        html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
    except ImportError:
        pass

html_static_path = ['_static']
htmlhelp_basename = 'cQuerydoc'


# -- Options for LaTeX output ---------------------------------------------

latex_elements = {
}

latex_documents = [
  ('index', 'cQuery.tex', u'cQuery Documentation',
   u'Marcus Ottosson', 'manual'),
]

man_pages = [
    ('index', 'cquery', u'cQuery Documentation',
     [u'Marcus Ottosson'], 1)
]

texinfo_documents = [
  ('index', 'cQuery', u'cQuery Documentation',
   u'Marcus Ottosson', 'cQuery', 'Schema-less directory structures',
   'Miscellaneous'),
]