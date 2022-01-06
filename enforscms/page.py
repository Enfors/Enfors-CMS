from flask import (
    Blueprint, render_template
)

import markdown

bp = Blueprint("page", __name__)


@bp.route("/")
def index():
    return render_template("page/index.html")


@bp.route("/<page_name>")
def page(page_name):
    html = load_page(page_name)
    return html


def load_page(page_name: str):
    """
    Load a page from disk or cache, and return it in HTML format.
    """
    try:
        with open(f"page/{page_name}.md", "r") as f:
            md_contents = f.read()
    except FileNotFoundError:
        return "not found"

    return render_template("page/index.html",
                           content=markdown.markdown(md_contents),
                           categories=["Hey", "There"])
    # return markdown.markdown(md_contents)
