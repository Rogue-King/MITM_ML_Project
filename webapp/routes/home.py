from flask import Blueprint, render_template

homepage = Blueprint("homepage", __name__, template_folder="../views/templates/", static_folder="../views/static/")

@homepage.route('/')
def default_page():
    return render_template("index.html")
