import csv
from flask import Blueprint, request, flash, redirect, render_template
from werkzeug.utils import secure_filename
import pandas as pd
from . import db
from .models import populate_db, Review, File
import os
from .utils.config import INPUT_DIR

views = Blueprint('views', __name__)


@views.route('/', methods=['GET'])
def index():
    return render_template('index.html')

