from flask import Blueprint, request, flash, redirect, render_template
from werkzeug.utils import secure_filename
import pandas as pd
from . import db
from .models import populate_db, Review, File
import os
from .utils.config import INPUT_DIR

labels = Blueprint('labels', __name__)


# New topics dict for insatisfaction
TOPICS_DICT = {
    "bag": "Product",
    "bike": "Product",
    "boots": "Product",
    "camping": "Product",
    "checkout": "Customer_service",
    "coats": "Product",
    "delivery": "Customer_service",
    "fishing": "Product",
    "food": "Product",
    "glasses": "Product",
    "gloves": "Product",
    "helmet": "Product",
    "kayaks": "Product",
    "none": "Other",
    "other": "Other",
    "pants": "Product",
    "pick-up": "Customer_service",
    "positive": "Positive",
    "pricing": "Price",
    "quality": "Quality",
    "scooter": "Product",
    "shirts": "Product",
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

# Old topics dict
# TOPICS_DICT = {
#     "bag": "Product",
#     "bike": "Product",
#     "boots": "Product",
#     "camping": "Product",
#     "checkout": "Customer_service",
#     "delivery": "Customer_service",
#     "fishing": "Product",
#     "glasses": "Product",
#     "helmet": "Product",
#     "irrelevant": "Other",
#     "kayaking": "Product",
#     "mixed": "Mixed",
#     "negative": "Negative",
#     "none": "Other",
#     "other": "Other",
#     "pants": "Product",
#     "pick-up": "Customer_service",
#     "positive": "Positive",
#     "pricing": "Pricing",
#     "quality": "Quality",
#     "scooter": "Product",
#     "shirts": "Product",
#     "shoes": "Product",
#     "size": "Size",
#     "skates": "Product",
#     "ski": "Product",
#     "staff": "Customer_service",
#     "stock": "Stock",
#     "store": "Store",
#     "swimsuit": "Product",
#     "website": "Tech"
# }

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
                review_topic_1=topic_1,
                review_topic_2=topic_2,
                review_topic_3=topic_3,
                review_metatopic_1=TOPICS_DICT[topic_1],
                review_metatopic_2=TOPICS_DICT[topic_2],
                review_metatopic_3=TOPICS_DICT[topic_3],
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
