import os
from flask import render_template, redirect, request, flash
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {".pcap", ".PCAP"}

def file_upload_success():
    if 'pcap-upload' not in request.files:
        flash('Could not find file uploaded')
        return False
        
    pcap_file = request.files['pcap-upload']
    
    if pcap_file.filename == '':
        flash('Invalid filename uploaded')
        return False

    if os.path.splitext(pcap_file.filename)[1] not in ALLOWED_EXTENSIONS:
        flash('File is not a recognized format. Please upload .pcap files only')
        return False

    filename = secure_filename(pcap_file.filename)
    pcap_file.save(os.path.join("webapp/file_uploads", filename))
    flash(f'Uploaded {filename} successfully')
    return True