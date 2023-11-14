# Importing the necessary modules and libraries
from flask import Flask, render_template

from webapp.routes.home import homepage
from webapp.routes.hist import history
from webapp.routes.upload import upload
from webapp.routes.packet_viewer import packet_viewer

import os

def create_app():
    app = Flask(__name__, template_folder='webapp/views/templates/')  # flask app object
    app.register_blueprint(homepage)
    app.register_blueprint(history, url_prefix="/history")
    app.register_blueprint(upload, url_prefix="/upload")
    app.register_blueprint(packet_viewer, url_prefix="/packet-viewer")
    app.secret_key = os.urandom(24);

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    return app


app = create_app()  # Creating the app


if __name__ == '__main__':  # Running the app
    app.run(host='127.0.0.1', port=5000, debug=True)
