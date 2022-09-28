from curses import flash
from unicodedata import category
from . import db
from datetime import datetime

class File(db.Model):
    __tablename__ = "files"
    
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    filename = db.Column(db.String(100))
    path = db.Column(db.String(100))
    
    def __init__(self, filename, path):
        self.filename = filename
        self.path = path
        
    def __repr__(self):
        return f"<id {self.id}>"
    


class Review(db.Model):
    """
    Table for customer reviews.
    
    Having a database for this application is somewhat overkill for it's
    purpose, but it's nice to have a saving feature that garantees we are not
    going to lose progress when labeling the data.
    """

    __tablename__ = "reviews"

    id = db.Column(db.BigInteger, autoincrement=False, primary_key=True)
    file_id = db.Column(db.ForeignKey('files.id'), primary_key=True)
    review_type = db.Column(db.String(100))
    store_num = db.Column(db.Integer)
    store_name = db.Column(db.String(100))
    country_reference = db.Column(db.String(2))
    language_reference = db.Column(db.String(2))
    title = db.Column(db.String(100))
    body = db.Column(db.Text)
    rating = db.Column(db.Integer)
    firstname = db.Column(db.String(100))
      
    review_topic_1 = db.Column(db.String(100))
    review_topic_2 = db.Column(db.String(100))
    review_topic_3 = db.Column(db.String(100))
    
    review_metatopic_1 = db.Column(db.String(100))
    review_metatopic_2 = db.Column(db.String(100))
    review_metatopic_3 = db.Column(db.String(100))
    
    review_source = db.Column(db.String(100))
    is_labeled = db.Column(db.Boolean)

    def __init__(
        self,
        id,
        file_id,
        review_type,
        store_num,
        store_name,
        country_reference,
        language_reference,
        title,
        body,
        rating,
        firstname,
        review_topic_1,
        review_topic_2,
        review_topic_3,
        review_metatopic_1,
        review_metatopic_2,
        review_metatopic_3,
        review_source,
        is_labeled = False
    ):  

        self.id = id
        self.file_id = file_id
        self.review_type = review_type
        self.store_num = store_num
        self.store_name = store_name
        self.country_reference = country_reference
        self.language_reference = language_reference
        self.title = title
        self.body = body
        self.rating = rating
        self.firstname = firstname
        
        self.review_topic_1 = review_topic_1    
        self.review_topic_2 = review_topic_2    
        self.review_topic_3 = review_topic_3   
         
        self.review_metatopic_1 = review_metatopic_1    
        self.review_metatopic_2 = review_metatopic_2    
        self.review_metatopic_3 = review_metatopic_3
        
        self.review_source = review_source
        self.is_labeled = is_labeled

    def __repr__(self):
        return f"<id {self.id}, file_id {self.file_id}>"


def populate_db(df, file_id):
    count = 0
    # Iterate over the rows of the dataframe
    for _, row in df.iterrows():
        review = Review.query.filter_by(id=row["id"], file_id=file_id).first()
        if review is None:
            new_review = Review(row["id"],
                                file_id,
                                row["review_type"], 
                                row["store_num"], 
                                row["store_name"], 
                                row["country_reference"], 
                                row["language_reference"], 
                                row["title"], 
                                row["body"], 
                                row["rating"], 
                                row["firstname"], 
                                row["review_topic_1"], 
                                row["review_topic_2"], 
                                row["review_topic_3"], 
                                row["review_metatopic_1"], 
                                row["review_metatopic_2"], 
                                row["review_metatopic_3"], 
                                row["review_source"]
            )
            
            try:
                db.session.add(new_review)
                db.session.commit()
                count += 1
            except Exception as e:
                raise e
        else:
            pass
    return count
