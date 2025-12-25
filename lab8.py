from flask import Blueprint, url_for, request, redirect, abort, render_template
from werkzeug.security import generate_password_hash
from db import db
from db.models import users, articles
from flask_login import login_user, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import and_, or_

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
    remember = request.form.get('remember') == 'on'

    if not login_form or not password_form:
        return render_template(
            'lab8/login.html',
            error='Логин и пароль не должны быть пустыми'
        )

    user = users.query.filter_by(login=login_form).first()

    if user and check_password_hash(user.password, password_form):
        login_user(user, remember=remember)
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
        return render_template('lab8/register.html', error='Логин не должен быть пустым')
    if not password_form:
        return render_template('lab8/register.html', error='Пароль не должен быть пустым')

    login_exists = users.query.filter_by(login=login_form).first()
    if login_exists:
        return render_template('lab8/register.html', error='Такой пользователь уже существует')

    password_hash = generate_password_hash(password_form)
    new_user = users(login=login_form, password=password_hash)

    db.session.add(new_user)
    db.session.commit()

    login_user(new_user)          
    return redirect('/lab8/')



@lab8.route('/lab8/articles')
def list_articles():
    q = request.args.get('q', '').strip()

    query = articles.query

    if current_user.is_authenticated:
        access_filter = or_(
            articles.login_id == current_user.id,
            and_(articles.is_public == True, articles.login_id != current_user.id)
        )
    else:
        access_filter = (articles.is_public == True)

    query = query.filter(access_filter)

    if q:
        query = query.filter(
            or_(
                articles.title.ilike(f'%{q}%'),
                articles.article_text.ilike(f'%{q}%')
            )
        )

    result_articles = query.order_by(articles.id.desc()).all()

    return render_template(
        'lab8/articles.html',
        articles=result_articles,
        q=q
    )

    return render_template('lab8/articles.html', articles=all_articles)
@lab8.route('/lab8/create', methods=['GET', 'POST'])
@login_required
def create_article():
    if request.method == 'GET':
        return render_template('lab8/create.html')

    title = request.form.get('title')
    article_text = request.form.get('article_text')

    is_public = request.form.get('is_public') == 'on'
    is_favorite = request.form.get('is_favorite') == 'on'

    if not title or not article_text:
        return render_template(
            'lab8/create.html',
            error='Заголовок и текст статьи не должны быть пустыми'
        )

    new_article = articles(
        login_id=current_user.id,
        title=title,
        article_text=article_text,
        is_favorite=is_favorite,
        is_public=is_public,
        likes=0
    )

    db.session.add(new_article)
    db.session.commit()
    return redirect('/lab8/articles')

@lab8.route('/lab8/edit/<int:article_id>', methods=['GET', 'POST'])
@login_required
def edit_article(article_id):
    article = articles.query.get_or_404(article_id)

    if article.login_id != current_user.id:
        abort(403)

    if request.method == 'GET':
        return render_template('lab8/edit.html', article=article)

    title = request.form.get('title')
    article_text = request.form.get('article_text')

    is_public = request.form.get('is_public') == 'on'
    is_favorite = request.form.get('is_favorite') == 'on'

    if not title or not article_text:
        return render_template(
            'lab8/edit.html',
            article=article,
            error='Заголовок и текст статьи не должны быть пустыми'
        )

    article.title = title
    article.article_text = article_text
    article.is_public = is_public
    article.is_favorite = is_favorite

    db.session.commit()
    return redirect('/lab8/articles')

@lab8.route('/lab8/delete/<int:article_id>', methods=['POST'])
@login_required
def delete_article(article_id):
    article = articles.query.get_or_404(article_id)

    if article.login_id != current_user.id:
        abort(403)

    db.session.delete(article)
    db.session.commit()
    return redirect('/lab8/articles')

@lab8.route('/lab8/logout')
@login_required
def logout():
    logout_user()
    return redirect('/lab8/')