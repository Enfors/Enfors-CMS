"""
Enfors-CMS by Christer Enfors. Project started 2021-12-31.

This project is derived from the official Flask tutorial.
"""

import os
import subprocess

from flask import Flask


def create_app(test_config=None):
    """
    Create and configure the app.
    """
    try:
        contents_dir = os.environ["MARKDOWNCMS_CONTENTS_DIR"]
    except KeyError:
        print("Environment variable MARKDOWNCMS_CONTENTS_DIR not set.")
        return False

    template_dir = os.path.join(contents_dir, "templates")
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

    # Webhook for updating contents
    updating = False
    @app.route("/admin/update-contents")
    def update_contents():
        for update_script in ["update.sh", "update.batt"]:
            try:
                command = [os.path.join(contents_dir, update_script)]
                output = subprocess.check_output(command)
                return "<h1>Updating contents</h1><pre>" + output.decode("utf-8") + "</pre>"
            except FileNotFoundError:
                # This version of update_script (update.sh or update.bat)
                # exist; try with the next one.
                continue

        return "<h1>Update script not found</h1>"

    from . import page
    app.register_blueprint(page.bp)
    app.add_url_rule("/", endpoint="index")

    return app
