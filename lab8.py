from flask import Blueprint, url_for, request, redirect, abort, render_template
from werkzeug.security import generate_password_hash
from db import db
from db.models import users, articles
from flask_login import login_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

lab8 = Blueprint('lab8', __name__)

@lab8.route('/lab8/')
def index():
    return render_template('lab8/index.html')

@lab8.route('/lab8/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab8/login.html')

    login_form = request.form.get('login')
    password_form = request.form.get('password')

    if not login_form or not password_form:
        return render_template(
            'lab8/login.html',
            error='Логин и пароль не должны быть пустыми'
        )

    user = users.query.filter_by(login=login_form).first()

    if user and check_password_hash(user.password, password_form):
        login_user(user)   
        return redirect('/lab8/')

    return render_template(
        'lab8/login.html',
        error='Неверный логин или пароль'
    )


@lab8.route('/lab8/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab8/register.html')

    login_form = request.form.get('login')
    password_form = request.form.get('password')

    if not login_form:
        return render_template('lab8/register.html',
                               error='Имя пользователя не должно быть пустым')

    if not password_form:
        return render_template('lab8/register.html',
                               error='Пароль не должен быть пустым')

    login_exists = users.query.filter_by(login = login_form).first()
    if login_exists:
        return render_template('lab8/register.html',
                               error='Такой пользователь уже существует')

    password_hash = generate_password_hash(password_form)
    new_user = users(login = login_form, password = password_hash)
    db.session.add(new_user)
    db.session.commit()
    return redirect('/lab8/')




@lab8.route('/lab8/articles')
@login_required
def articles():
    return render_template('lab8/articles.html')

@lab8.route('/lab8/create')
def create():
    return render_template('lab8/create.html')

@lab8.route('/lab8/logout')
@login_required
def logout():
    logout_user()
    return redirect('/lab8/')


