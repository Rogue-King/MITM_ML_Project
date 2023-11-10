from flask import Blueprint, redirect, request
from webapp.controllers.upload_controller import *

upload = Blueprint("upload", __name__, template_folder="../views/templates/", static_folder="../views/static/")

@upload.route('/', methods=["POST"])
def default_page():
    if request.method == "POST":
        if 'pcap-upload' not in request.files:
            return redirect("/FileNotFound")
        
        pcap_file = request.files['pcap-upload']

        return upload_file(pcap_file)
    else: 
        return redirect("/404")