from flask import Blueprint, render_template, redirect

homepage = Blueprint("homepage", __name__, template_folder="templates/", static_folder="static/")

@homepage.route('/')
def default_page():
    return render_template("index.html")