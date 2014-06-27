# -*- coding: utf-8 -*-

import sys
import os
import sphinx

src_path = os.path.abspath('..')
if not src_path in sys.path:
    sys.path.insert(0, src_path)

import cquery

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.viewcode',
    'sphinx.ext.autodoc',
]

if sphinx.version_info >= (1, 3):
    extensions.append('sphinx.ext.napoleon')
else:
    extensions.append('sphinxcontrib.napoleon')

templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'

project = u'cQuery'
copyright = u'2014, Marcus Ottosson'
version = cquery.__version__
release = version

exclude_patterns = []
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