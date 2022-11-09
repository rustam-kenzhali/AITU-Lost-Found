from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Post
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/')
def home():
    if current_user.is_authenticated:
        flash('You already logged in!', category='error')
        return redirect(url_for('views.oldhome'))
    return render_template("home.html", user=current_user)


@views.route("/oldhome")
def oldhome():
    return render_template("old_home.html", user=current_user)

