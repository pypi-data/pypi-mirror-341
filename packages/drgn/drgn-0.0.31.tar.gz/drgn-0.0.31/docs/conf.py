import os.path
import sys

sys.path.append(os.path.abspath(".."))
sys.path.append(os.path.abspath("exts"))

master_doc = "index"

man_pages = [
    ("man/drgn", "drgn", "programmable debugger", "", "1"),
]

option_emphasise_placeholders = True

extensions = [
    "details",
    "drgndoc.ext",
    "linuxsrc",
    "setuptools_config",
    "sphinx.ext.extlinks",
    "sphinx.ext.graphviz",
    "sphinx.ext.intersphinx",
]

drgndoc_paths = ["../drgn", "../_drgn.pyi"]
drgndoc_substitutions = [
    (r"^_drgn\b", "drgn"),
]

extlinks = {
    "contrib": (
        "https://github.com/osandov/drgn/blob/main/contrib/%s",
        "%s",
    ),
}

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
}

manpages_url = "http://man7.org/linux/man-pages/man{section}/{page}.{section}.html"

html_static_path = ["_static"]

html_theme = "alabaster"

html_theme_options = {
    "description": "Programmable debugger",
    "logo": "logo.png",
    "logo_name": True,
    "logo_text_align": "center",
    "github_user": "osandov",
    "github_repo": "drgn",
    "github_button": True,
    "github_type": "star",
}

html_favicon = "favicon.ico"
