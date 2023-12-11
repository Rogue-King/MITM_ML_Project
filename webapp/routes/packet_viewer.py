from flask import Blueprint, render_template, session, redirect, url_for
from webapp.controllers.pcap_viewer_controller import get_table_segment

import math

packet_viewer = Blueprint("packet_viewer", __name__, template_folder="../views/templates/", static_folder="../views/static/")

# MAKE THIS MORE READABLE
@packet_viewer.route('/', defaults={'page': 1})
@packet_viewer.route('/<int:page>')
def default_page(page):
    pcap_filepath = session.get('pcap_csv_filepath', None)

    if (pcap_filepath == None):
        return redirect('/')

    packets_per_page = 25

    # Get the total of packets by counting the total number of lines (minus the column headers and the trailing new line)
    total_packets = sum(1 for line in open(pcap_filepath)) - 2
    total_pages = math.ceil(total_packets / packets_per_page + 1)

    if (page > total_pages):
        return redirect(url_for('packet_viewer.default_page', page=(total_pages - 1)))

    packet_table, start_page, end_page = get_table_segment(pcap_filepath, page, total_pages, packets_per_page)


    return render_template("packet_data_display.html", packet_table=packet_table, current_page=page, start_page=start_page, end_page=end_page, total_pages=total_pages)