import os

from flask import (
    Blueprint, render_template, g
)

from werkzeug.exceptions import abort

import markdown

bp = Blueprint("page", __name__)


@bp.route("/")
def index():
    page = Page("index.html")

    if page.code != 200:
        abort(page.code, page.html)

    return render_template("index.html", content=page.html)


@bp.route("/<page_name>")
def page(page_name):
    page = Page(page_name)

    if page.code != 200:
        abort(page.code, page.html)

    g.categories = ["Foo", "Bar"]
    g.current_category = "Foo"
    return render_template("page_template.html", content=page.html,
                           current_category="value")
    # return page.html


class Page:
    """
    This class represents a page. It can load a page from disk
    (probably in Markdown format) and convert it to HTML.
    """

    def __init__(self, name="index.html"):
        self.name = name
        self.code = None
        if name:
            self.code = 200
            self.load()
        else:
            self.html = None
            self.markdown = None

    def load(self):
        contents_dir = os.path.join(os.getenv("MARKDOWNCMS_CONTENTS_DIR"),
                                    "pages")

        is_html = False

        if self.name[-5:] == ".html":
            is_html = True
            file_name = self.name
        else:
            file_name = f"{self.name}.md"

        file_name = os.path.join(contents_dir, self.name)

        try:
            with open(file_name, "r") as f:
                if is_html:
                    self.html = f.read()
                    print(f"is_html: {self.html[:20]}...")
                else:
                    print("Is not html")
                    self.markdown = f.read()
                    self.html = markdown.markdown(self.markdown)
        except FileNotFoundError:
            self.code = 404
            self.html = f"File {file_name} not found"
            return self.html

        return self.html
