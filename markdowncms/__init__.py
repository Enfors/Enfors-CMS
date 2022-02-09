"""
Enfors-CMS by Christer Enfors. Project started 2021-12-31.

This project is derived from the official Flask tutorial.
"""

import os

from flask import Flask


def create_app(test_config=None):
    """
    Create and configure the app.
    """
    template_dir = os.path.join(os.environ["MARKDOWNCMS_CONTENTS_DIR"], "templates")
    app = Flask(__name__, instance_relative_config=True,
                template_folder=template_dir)
    app.config.from_mapping(SECRET_KEY="dev",
                            # Not sure if a database is needed yet...
                            DATABASE=os.path.join(app.instance_path,
                                                  "MarkdownCMS.sqlite"))

    if test_config is None:
        # Load the instance config if it exists, when not testing.
        app.config.from_pyfile("config.py", silent=True)
    else:
        # Load the test config if passed in.
        app.config.from_mapping(test_config)

    # Ensure that the instance folder exists.
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # A simple testing page
    @app.route("/hello")
    def hello():
        return "<h1>Hello world!</h1>"

    from . import page
    app.register_blueprint(page.bp)
    app.add_url_rule("/", endpoint="index")

    return app
