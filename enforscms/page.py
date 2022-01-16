import os

from flask import (
    Blueprint, render_template
)

from werkzeug.exceptions import abort

import markdown

bp = Blueprint("page", __name__)


@bp.route("/")
def index():
    page = Page("index")

    if page.code != 200:
        abort(page.code, page.html)

    return render_template("page/index.html", content=page.html)


@bp.route("/<page_name>")
def page(page_name):
    page = Page(page_name)

    if page.code != 200:
        abort(page.code, page.html)
    return render_template("page/index.html", content=page.html)
    # return page.html


class Page:
    """
    This class represents a page. It can load a page from disk
    (probably in Markdown format) and convert it to HTML.
    """

    def __init__(self, name="index"):
        self.name = name
        self.code = None
        if name:
            self.code = 200
            self.load()
        else:
            self.html = None
            self.markdown = None

    def load(self):
        try:
            with open(os.path.join("page", f"{self.name}.md"), "r") as f:
                self.markdown = f.read()
        except FileNotFoundError:
            self.code = 404
            self.html = f"File {self.name}.md not found"
            return self.html

        self.html = markdown.markdown(self.markdown)
        return self.html
