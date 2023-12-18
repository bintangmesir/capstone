import os
import pymongo
from ... import db
from ... import app, render_template, roles_required, request, redirect, url_for, bcrypt, flash, current_user
from flask_login import login_required
from bson import ObjectId
from datetime import datetime
from werkzeug.utils import secure_filename
current_time = datetime.utcnow()


APP_ROOT = os.path.dirname(os.path.abspath(__file__))
IMG_AKTIVITAS = os.getenv("IMG_AKTIVITAS")
IMG_ARTIKEL = os.getenv("IMG_ARTIKEL")
IMG_DONATUR = os.getenv("IMG_DONATUR")
IMG_QR = os.getenv("IMG_QR")


app.config['IMG_AKTIVITAS'] = IMG_AKTIVITAS
app.config['IMG_ARTIKEL'] = IMG_ARTIKEL
app.config['IMG_DONATUR'] = IMG_DONATUR
app.config['IMG_QR'] = IMG_QR
