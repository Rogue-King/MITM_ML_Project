# Importing the necessary modules and libraries
from flask import Flask, send_from_directory

from webapp.views.home import homepage
from webapp.views.hist import history

def create_app():
    app = Flask(__name__)  # flask app object
    app.register_blueprint(homepage)
    app.register_blueprint(history, url_prefix="/history")

    @app.route('/static/js/<filename>')
    def serve_js(filename):
        return send_from_directory('webapp/views/static/js/', filename)
    
    return app


app = create_app()  # Creating the app


if __name__ == '__main__':  # Running the app
    app.run(host='127.0.0.1', port=5000, debug=True)
