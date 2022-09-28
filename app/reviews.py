from fileinput import filename
from flask import Blueprint, request, flash, render_template
from werkzeug.utils import secure_filename
import pandas as pd
from . import db
from .models import populate_db, Review, File
import os
from .utils.config import INPUT_DIR, OUTPUT_DIR

reviews = Blueprint('reviews', __name__)

show_only_labeled = True
file_id = None


@reviews.route('/reviews', methods=['GET', 'POST'])
def review():
    global show_only_labeled, file_id
    
    reviews = []
    
    if request.method == 'POST':
        show_only_labeled = request.form.get("show_only_labeled")
        file_id = request.form.get("file_id")
        reviews = Review.query.filter_by(file_id=file_id).order_by(Review.id).all()
    
    csv_files = File.query.order_by(File.id).all()
    return render_template('reviews.html', reviews=reviews, show_only_labeled=show_only_labeled, csv_files=csv_files)


@reviews.route('/reviews-output', methods=['POST'])
def review_output():
    global show_only_labeled, file_id
    
    try:
        filename = db.session.query(File.filename).filter_by(id=file_id).first()[0]
        reviews = Review.query.filter_by(file_id=file_id).order_by(Review.id).all()
        
        out_df = pd.read_sql(db.session.query(Review).filter(Review.file_id == file_id).statement, db.session.bind)
        out_df.to_csv(os.path.join(OUTPUT_DIR, filename), index=False)
        flash(f"{filename} saved succesfully", category="sucess")
    except:
        flash("Something went wrong when saving the output CSV file", category="error")
      
    csv_files = File.query.order_by(File.id).all()
    return render_template('reviews.html', reviews=reviews, show_only_labeled=show_only_labeled, csv_files=csv_files)
