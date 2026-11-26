from datetime import datetime
import os

project = "CX 硬件产品教程"
copyright = f"{datetime.now():%Y}, CX"
author = "CX"
release = "v0.2.0"
html_title = "CX 硬件产品教程"
html_short_title = "CX Tutorials"

extensions = [
    "myst_parser",
    "sphinx.ext.extlinks",
    "sphinx.ext.autosectionlabel",
    "sphinx_copybutton",
]

copybutton_prompt_text = r">>> |\.\.\. |\$ |In \[\d*\]: | {2,5}\.\.\."
copybutton_line_continuation_character = "\\"

autosectionlabel_prefix_document = True

source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

templates_path = ["_templates"]
# 不把 assets 里的说明文档当成站点页面
exclude_patterns = [
    "**/assets/**/*.md",
    "**/assets/**/*.rst",
    "**/outline.md",
    "**/README.md",
]

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