from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Post
from . import db, app
import json
import os
from werkzeug.utils import secure_filename

views = Blueprint('views', __name__)

@views.route('/')
def home():
    if current_user.is_authenticated:
        # flash('You already logged in!', category='error')
        return redirect(url_for('views.main_page'))
    return render_template("home.html")


@login_required   # you haven't acsess to home page if you are not login
@views.route("/main_page")
def main_page():
    return render_template("main_page.html", main_page="active")

@login_required   # you haven't acsess to home page if you are not login
@views.route("/lost")
def lost():
    posts = Post.query.filter_by(lostfound='lost').all()
    # print(posts)
    return render_template("posts.html", lost_page="active", posts=posts)


@login_required   # you haven't acsess to home page if you are not login
@views.route("/found")
def found():
    posts = Post.query.filter_by(lostfound='found').all()

    return render_template("posts.html", found_page="active", posts=posts)

@login_required   # you haven't acsess to home page if you are not login
@views.route("/profile")
def profile():
    return render_template("profile.html", profile_page="active", email=current_user.email, full_name=current_user.full_name,
                           phone=current_user.phone_number, group=current_user.group)

@login_required
@views.route("/profile/add_post", methods=['GET', 'POST'])
def add_post():
    if request.method == 'POST':

        title = request.form.get('title')
        content = request.form.get('content')
        method = request.form.get('method')
        image = request.files['img']

        if len(title) < 5:
            flash('Title too short')
        elif not image:
            flash('Upload image!')
        else:
            new_post = Post(title=title, content=content, lostfound=method, image=image.filename,
                        author=current_user.full_name,user_id=current_user.id)
            db.session.add(new_post)
            db.session.commit()
            image.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'],
                                    secure_filename(image.filename)))

        return redirect(url_for('views.profile'))

    return render_template("add_post.html", profile_page="active")

