from flask import Blueprint, render_template, redirect

history = Blueprint("history", __name__, template_folder="templates/", static_folder="static/")

@history.route('/')
def default_page():
    return render_template("hist_data.html")