import os
from flask import redirect
from werkzeug.utils import secure_filename


ALLOWED_EXTENSIONS = {".pcap", ".PCAP"}

def upload_file(file):
    if file.filename == '':
        return redirect("/");

    if os.path.splitext(file.filename)[1] in ALLOWED_EXTENSIONS:
        filename = secure_filename(file.filename)
        file.save(os.path.join("webapp/file_uploads", filename))
        return redirect("/Upload_Success"); # Redirect to side by side view

    return redirect("/Failed");