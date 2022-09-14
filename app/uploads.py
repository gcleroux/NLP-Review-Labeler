from flask import Blueprint, request, flash, render_template
from werkzeug.utils import secure_filename
import pandas as pd
from . import db
from .models import populate_db, Review, File
import os
from .utils.config import INPUT_DIR

uploads = Blueprint('uploads', __name__)

ALLOWED_EXTENSIONS = set(["csv"])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@uploads.route('/upload', methods=['GET','POST'])
def upload():
    if request.method == "POST":
        file = request.files["file"]
        if file and allowed_file(file.filename):
            try:
                df = pd.read_csv(request.files.get('file'))
                filename = secure_filename(file.filename)
                path = os.path.join(INPUT_DIR, filename)
                df.to_csv(path)
                
                # Add the file to the db
                csv_file = File(filename=filename, path=path)
                db.session.add(csv_file)
                db.session.commit()
                
                # Populate the review table
                populate_db(df, csv_file.id)
                flash('File uploaded sucessfully', category='success')
            except:       
                flash("Error while uploading file", category="error")
                return render_template('upload.html')
        else:
            flash("You can only upload CSV files at the moment", category="error")
        return render_template('upload.html')

    return render_template('upload.html')
