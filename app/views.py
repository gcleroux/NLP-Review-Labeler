import csv
from flask import Blueprint, request, flash, redirect, render_template
from werkzeug.utils import secure_filename
import pandas as pd
from . import db
from .models import populate_db, Review, File
import os
from .utils.config import UPLOAD_DIR

views = Blueprint('views', __name__)

show_only_labeled = True

labeling_classes = [
    "bike",
    "shoes",
    "delivery",
    "bag",
    "stock",
    "store"
]
labeling_reviews = []
current_review = None

ALLOWED_EXTENSIONS = set(["csv"])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@views.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@views.route('/reviews', methods=['GET', 'POST'])
def reviews():
    global show_only_labeled
    
    reviews = []
    
    if request.method == 'POST':
        show_only_labeled = request.form.get("show_only_labeled")
        file_id = request.form.get("file_id")
        reviews = Review.query.filter_by(file_id=file_id).order_by(Review.id).all()
    
    csv_files = File.query.order_by(File.id).all()
    return render_template('reviews.html', reviews=reviews, show_only_labeled=show_only_labeled, csv_files=csv_files)

@views.route('/upload', methods=['GET','POST'])
def upload():
    if request.method == "POST":
        file = request.files["file"]
        if file and allowed_file(file.filename):
            try:
                df = pd.read_csv(request.files.get('file'))
                filename = secure_filename(file.filename)
                path = os.path.join(UPLOAD_DIR, filename)
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



@views.route('/label', methods=['GET','POST'])
def label():
    global labeling_classes, labeling_reviews, current_review
    
    if request.method == 'POST':       
        # Get all the reviews
        file_id = request.form.get("file_id")
        labeling_reviews = Review.query.filter_by(file_id=file_id).order_by(Review.id).all()
        try:
            current_review = labeling_reviews[0]
        except IndexError:
            flash("No review in this CSV file", category="error")
    
    csv_files = File.query.order_by(File.filename).all()
    return render_template('label.html', csv_files=csv_files, current_review=current_review, labeling_classes=labeling_classes)