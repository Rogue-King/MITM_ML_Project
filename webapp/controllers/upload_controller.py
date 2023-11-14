import os
from flask import request, flash, session
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {".pcap", ".PCAP"}


def file_upload_success():
    if 'pcap-upload' not in request.files:
        flash('Could not find file uploaded')
        return False
        
    pcap_file = request.files['pcap-upload']
    
    if pcap_file.filename == '':
        flash('File not found. Please try again')
        return False

    if os.path.splitext(pcap_file.filename)[1] not in ALLOWED_EXTENSIONS:
        flash('File is not a recognized format. Please upload .pcap files only')
        return False

    filename = secure_filename(pcap_file.filename)
    pcap_file.save(os.path.join("webapp/file_uploads", filename))
    
    session['pcap_filepath'] = "webapp/file_uploads/{}".format(filename)

    flash(f'Uploaded {filename} successfully')
    return True
