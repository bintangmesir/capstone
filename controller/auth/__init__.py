import os
import datetime
from ... import app, User, bcrypt, flash
from ... import db
from datetime import datetime
from bson.objectid import ObjectId
from flask import Flask, request, render_template, redirect, url_for
from flask_login import current_user, login_user, logout_user

users = db['users']
