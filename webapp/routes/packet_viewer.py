from flask import Blueprint, render_template, redirect, session
from webapp.controllers.pcap_controller import *

packet_viewer = Blueprint("packet_viewer", __name__, template_folder="../views/templates/", static_folder="../views/static/")

@packet_viewer.route('/')
def default_page():
    pcap_filepath = session.pop('pcap_filepath', None)
    
    if (pcap_filepath == None):
        return redirect('/')

    return render_template("packet_data_display.html", packet_table=parse_pcap_file(pcap_filepath)) 