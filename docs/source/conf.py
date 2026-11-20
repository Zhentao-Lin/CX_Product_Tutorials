from datetime import datetime
import os

project = "CX_Product_Tutorials"
copyright = f"{datetime.now():%Y}, CX"
author = "CX"
release = "v0.1.0"

extensions = [
    "myst_parser",
    "sphinx.ext.extlinks",
    "sphinx.ext.autosectionlabel",
]

autosectionlabel_prefix_document = True

source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

templates_path = ["_templates"]
exclude_patterns = []

language = "zh_CN"

root_doc = "index"

html_theme = "sphinx_rtd_theme"
html_theme_options = {
    "collapse_navigation": False,
    "navigation_depth": 4,
    "includehidden": True,
    "prev_next_buttons_location": "both",
    "style_external_links": True,
}

html_static_path = ["_static"]
html_css_files = ["css/custom.css"]

# Read the Docs 与 GitHub Pages 共用
html_baseurl = os.environ.get("READTHEDOCS_CANONICAL_URL", "")

myst_enable_extensions = ["colon_fence", "deflist"]
myst_heading_anchors = 3