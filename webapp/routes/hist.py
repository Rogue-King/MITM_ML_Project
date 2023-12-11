from flask import Blueprint, render_template

history = Blueprint("history", __name__, template_folder="../views/templates/", static_folder="../views/static/")

@history.route('/')
def default_page():
    return render_template("hist_data.html")