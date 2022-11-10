from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from jinja2 import Template

# FLOOR PROF DATA
from .data_floorproof import phone_num_floorproof, code_confirm

auth = Blueprint('auth', __name__)


@auth.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if current_user.is_authenticated:
        flash('You already logged in!', category='error')
        return redirect(url_for('views.main_page'))

    if request.method == 'POST':
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        full_name = request.form.get('full_name')
        group = request.form.get('group')
        phone_number = request.form.get('phone_number')

        # foolproof
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exist!', category='error')
        elif len(email) < 15 or '@astanait.edu.kz' not in email:
            flash('Use only university corporate mail', category='error')
        elif len(full_name) < 2:
            flash('Full name must be greater than 1 character', category='error')
        elif password1 != password2:
            flash('Password don\'t match', category='error')
        elif group[0:2].upper() not in ['CS', 'IT', 'SE'] and group[0:3] not in ['BDA', 'MIT']:
           flash('This group does not exist', category='error')
        elif not phone_num_floorproof(phone_number):
           flash('This phone does not exist', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters', category='error')
        else:
            # Password confirm
            session['user'] = [email, password1, full_name, group, phone_number]
            subject = 'Confirm your Email on AITU Lost&Found'
            body = Template('''AITU Lost&Found
            Thank you for using our development
            Your verification code: {{ code }}
            
            The project was developed by CS2114 students
            Rustam Kenzhali,
            Dariya Aidarkyzy,
            Ussenbekova Togzhan
            ''')
            code_confirm(email, subject, body)

            session['open_code_confirm'] = True

            return redirect(url_for("auth.email_confirm"))

    return render_template("sign_up.html", user=current_user)


@auth.route('sign_up/email_comfirm', methods=['GET', 'POST'])
def email_confirm():
    print(session['send_code'])
    if current_user.is_authenticated:
        flash('You already logged in!', category='error')
        return redirect(url_for('views.main_page'))

    try:
        if not session['open_code_confirm']:
            # flash('You are logged or have not filled in the registration field!')
            print(1)
            return redirect(url_for('views.home'))
    except:
        # flash('You have not filled in the registration field!')
        print(2)
        return redirect(url_for('views.home'))

    if request.method == 'POST':
        input_code = request.form.get('code')
        if session['send_code'] == input_code:

            # add user to database
            new_user = User(email=session['user'][0], password=generate_password_hash(session['user'][1], method='sha256'),
                            full_name=session['user'][2],
                            group=session['user'][3], phone_number=session['user'][4])
            db.session.add(new_user)
            db.session.commit()

            user = User.query.filter_by(email=session['user'][0]).first()
            login_user(user, remember=True)  # remember login user session
            # flash('Account created!', category='success')
            session['open_code_confirm'] = False
            return redirect(url_for('views.main_page'))
        else:
            flash('Incorect code')

    return render_template("check_code.html", user=current_user)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('You already logged in!', category='error')
        return redirect(url_for('views.main_page'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                # flash('Logged in successfully!', category='success')
                login_user(user, remember=True)  # remember login user session
                # session['userLogged'] = email
                return redirect(url_for('views.main_page'))
            else:
                flash('Incorrect password, try agaun.', category='error')
        else:
            flash('Email does not exist.', category='error')
    return render_template("login.html", user=current_user)

# You already logged in!
@auth.route('/login/forgot', methods=['GET', 'POST'])
def forgot_password():
    if current_user.is_authenticated:
        flash('You already logged in!', category='error')
        return redirect(url_for('views.main_page'))

    if request.method == 'POST':
        email = request.form.get('email')

        user = User.query.filter_by(email=email).first()
        if not user:
            flash("This account does't exist")
        elif len(email) < 15 or '@astanait.edu.kz' not in email:
            flash('Use only university corporate mail', category='error')
        else:
            # print(email)
            session['email'] = email

            subject = 'Password Reset on AITU Lost&Found'
            body = Template('''AITU Lost&Found
            Password Reset
            Your confirmation code: {{ code }}

            The project was developed by CS2114 students
            Rustam Kenzhali,
            Dariya Aidarkyzy,
            Ussenbekova Togzhan
            ''')
            code_confirm(email, subject, body)

            session['open_code_confirm'] = True

            return redirect(url_for("auth.forgot_password_code_confirm"))



    return render_template('forgot_password.html')


@auth.route('/login/forgot/code', methods=['GET', 'POST'])
def forgot_password_code_confirm():
    if current_user.is_authenticated:
        flash('You already logged in!', category='error')
        return redirect(url_for('views.main_page'))

    try:
        if not session['open_code_confirm']:
            # flash('You are logged or have not filled in the registration field!')
            print(1)
            return redirect(url_for('views.home'))
    except:
        # flash('You have not filled in the registration field!')
        print(2)
        return redirect(url_for('views.home'))

    if request.method == 'POST':
        input_code = request.form.get('code')
        if session['send_code'] == input_code:
            # print(session['send_code'])
            # print(input_code)
            session['open_code_confirm'] = False
            session['new_password_confirm'] = True
            return redirect(url_for('auth.new_password'))
        else:
            flash('Incorect code')
    return render_template('check_code.html')


@auth.route('/login/forgot/new_password', methods=['GET', 'POST'])
def new_password():
    if current_user.is_authenticated:
        flash('You already logged in!', category='error')
        return redirect(url_for('views.main_page'))

    try:
        if not session['new_password_confirm']:
            # flash('You are logged or have not filled in the registration field!')
            print(1)
            return redirect(url_for('views.home'))
    except:
        # flash('You have not filled in the registration field!')
        print(2)
        return redirect(url_for('views.home'))

    if request.method == 'POST':
        password = request.form.get('password')
        if len(password) < 7:
            flash('Password must be at least 7 characters', category='error')
            return render_template('new_password.html')

        update_user = User.query.filter_by(email=session['email']).first()
        update_user.password = generate_password_hash(password, method='sha256')
        db.session.commit()

        session['new_password_confirm'] = False

        return redirect(url_for('views.home'))
        # print(session['email'])
        # print(password)


    return render_template('new_password.html')

@auth.route('/logout')
@login_required   # you can't log out if you not log in
def logout():
    session['open_code_confirm'] = False
    session['new_password_confirm'] = False
    logout_user()
    return redirect(url_for('views.home'))
