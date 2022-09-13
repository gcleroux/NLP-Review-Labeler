import csv
from flask import Blueprint, request, flash, redirect, render_template
from werkzeug.utils import secure_filename
import pandas as pd
from . import db
from .models import populate_db, Review, File
import os
from .utils.config import UPLOAD_DIR

views = Blueprint('views', __name__)

show_all = False
file_id = None

ALLOWED_EXTENSIONS = set(["csv"])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@views.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@views.route('/reviews', methods=['GET', 'POST'])
def reviews():
    global show_all, file_id
    
    # Get all reviews
    reviews = Review.query.order_by(Review.id).all()
    
    if request.method == 'POST':
        # Reverse the show_all
        show_all = not show_all
    
    csv_files = File.query.order_by(File.id).all()
    return render_template('reviews.html', reviews=reviews, show_all=show_all, csv_files=csv_files)

@views.route('/upload', methods=['GET','POST'])
def upload():
    if request.method == "POST":
        file = request.files["file"]
        if file and allowed_file(file.filename):
            # Populate the review table
            df = pd.read_csv(request.files.get('file'))
            
            filename = secure_filename(file.filename)
            path = os.path.join(UPLOAD_DIR, filename)
            df.to_csv(path)
            
            # Add the file to the db
            csv_file = File(filename=filename, path=path)
            
            try:
                db.session.add(csv_file)
                db.session.commit()
                
                populate_db(df, csv_file.id)
                flash('File uploaded sucessfully', category='success')
            except:       
                flash("Error while uploading file", category="error")
                return render_template('upload.html')
            
        return render_template('index.html')

    return render_template('upload.html')



@views.route('/label', methods=['GET','POST'])
def label():
    return render_template('label.html')