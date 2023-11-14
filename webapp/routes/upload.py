from flask import Blueprint, redirect, session
from webapp.controllers.upload_controller import *

upload = Blueprint("upload", __name__, template_folder="../views/templates/", static_folder="../views/static/")

@upload.route('/', methods=["GET", "POST"])
def default_page():
    if request.method == "POST" and file_upload_success():
        return redirect('/packet-viewer')
    else: 
        return redirect('/')