from flask import Blueprint, request, flash, redirect, render_template
from werkzeug.utils import secure_filename
import pandas as pd
from . import db
from .models import populate_db, Review, File
import os
from .utils.config import INPUT_DIR

labels = Blueprint('labels', __name__)

TOPICS_DICT = {
    "bag": "Product",
    "bike": "Product",
    "boots": "Product",
    "camping": "Product",
    "checkout": "Customer_service",
    "delivery": "Customer_service",
    "glasses": "Product",
    "helmet": "Product",
    "negative": "Negative",
    "none": "Other",
    "other": "Other",
    "pants": "Product",
    "positive": "Positive",
    "quality": "Quality",
    "scooter": "Product",
    "shoes": "Product",
    "size": "Size",
    "skates": "Product",
    "ski": "Product",
    "staff": "Customer_service",
    "stock": "Stock",
    "store": "Store",
    "swimsuit": "Product",
    "website": "Tech"
}

labeling_reviews = []
current_review = None

@labels.route('/label', methods=['GET','POST'])
def label():
    global TOPICS_DICT, labeling_reviews, current_review
    
    if request.method == 'POST':       
        # Get all the reviews
        file_id = request.form.get("file_id")
        labeling_reviews = Review.query.filter_by(file_id=file_id).order_by(Review.id).all()
        get_next_review()
    
    csv_files = File.query.order_by(File.filename).all()
    return render_template('label.html', csv_files=csv_files, current_review=current_review, labeling_classes=list(TOPICS_DICT.keys()))


@labels.route('/label-next', methods=['POST'])
def label_next():
    global TOPICS_DICT, labeling_reviews, current_review
    
    # Get all the topics
    topic_1 = request.form.get("topic-1")
    topic_2 = request.form.get("topic-2")
    topic_3 = request.form.get("topic-3")
    
    try:
        # Update the review
        Review.query.filter_by(
            id=current_review.id,
            file_id=current_review.file_id
        ).update(
            dict(
                primary_topic=topic_1,
                primary_metatopic=TOPICS_DICT[topic_1],
                secondary_topic=topic_2,
                secondary_metatopic=TOPICS_DICT[topic_2],
                tertiary_topic=topic_3,
                tertiary_metatopic=TOPICS_DICT[topic_3],
                is_labeled=True
            )
        )
        db.session.commit()
    except:
        flash("Error when updating the review in the database", category='error')
    
    get_next_review()
    
    csv_files = File.query.order_by(File.filename).all()
    return render_template('label.html', csv_files=csv_files, current_review=current_review, labeling_classes=list(TOPICS_DICT.keys()))

def get_next_review():
    global labeling_reviews, current_review
    try:
        while True:
            current_review = labeling_reviews.pop(0)
            if not current_review.is_labeled:
                break
    except IndexError:
        flash("No review left to label in this CSV file", category="error")
