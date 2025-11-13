from flask import Blueprint, render_template,request, session, redirect, current_app
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
from os import path

lab5 = Blueprint('lab5', __name__)

@lab5.route('/lab5/')
def lab():
    return render_template('lab5/lab5.html', login=session.get('login'))

@lab5.route('/lab5/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab5/register.html')

    login = request.form.get('login')
    password = request.form.get('password')
    full_name = request.form.get('full_name', '').strip()

    if not login or not password or not full_name:
        return render_template(
            'lab5/register.html',
            error='Заполните логин, пароль и имя',
            login=login,
            full_name=full_name
        )

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT login FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT login FROM users WHERE login=?;", (login,))

    
    if cur.fetchone():
        db_close(conn, cur)
        return render_template(
            'lab5/register.html',
            error="Такой пользователь уже существует",
            login=login,
            full_name=full_name
        )

    password_hash = generate_password_hash(password)
    
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute(
            "INSERT INTO users (login, password, full_name) VALUES (%s, %s, %s);",
            (login, password_hash, full_name)
        )
    else:
        cur.execute(
            "INSERT INTO users (login, password, full_name) VALUES (?, ?, ?);",
            (login, password_hash, full_name)
        )

    db_close(conn, cur)
    return render_template('lab5/success.html', login=login)


@lab5.route('/lab5/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab5/login.html')

    login = request.form.get('login')
    password = request.form.get('password')

    if not login or not password:
        return render_template('lab5/login.html', error="Заполните поля")

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres': cur.execute("SELECT * FROM users WHERE login=%s;", (login,))
    else:  
        cur.execute("SELECT * FROM users WHERE login=?;", (login,))

    user = cur.fetchone()

    if not user:
        db_close(conn, cur)
        return render_template('lab5/login.html',
                               error='Логин и/или пароль неверны')
    
    if not check_password_hash(user['password'], password):
        db_close(conn, cur)
        return render_template('lab5/login.html',
                            error='Логин и/или пароль неверны')

    
    session['login'] = login

    db_close(conn, cur)

    return render_template('lab5/success_login.html', login=login)


def db_connect():
    if current_app.config['DB_TYPE'] == 'postgres':
        conn = psycopg2.connect(
            host = '127.0.0.1',
            database = 'alina_trandysheva_knowledge_base',
            user = 'alina_trandysheva_knowledge_base',
            password = '123'
        )
        cur = conn.cursor(cursor_factory = RealDictCursor)
    else:
        dir_path = path.dirname(path.realpath(__file__))
        db_path = path.join(dir_path, "database.db")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

    return conn, cur


def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()

@lab5.route('/lab5/create', methods = ['GET', 'POST'])
def create():
    login=session.get('login')
    if not login:
        return redirect('/lab5/login')

    if request.method == 'GET':
        return render_template('lab5/create_article.html')
    
    title = request.form.get('title')
    article_text = request.form.get('article_text')
    is_favorite = bool(request.form.get('is_favorite'))
    is_public = bool(request.form.get('is_public'))


    if not title or not article_text:
        return render_template(
            'lab5/create_article.html',
            error='Заполните и заголовок, и текст статьи',
            title=title,
            article_text=article_text
        )

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT id FROM users WHERE login=?;", (login,))
    
    user_id = cur.fetchone()["id"]

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute(
            "INSERT INTO articles(user_id, title, article_text, is_favorite, is_public) "
            "VALUES (%s, %s, %s, %s, %s);",
            (user_id, title, article_text, is_favorite, is_public)
        )
    else:
        cur.execute(
        "INSERT INTO articles(user_id, title, article_text, is_favorite, is_public) "
        "VALUES (?, ?, ?, ?, ?);",
        (user_id, title, article_text, is_favorite, is_public)
    )

    db_close(conn, cur)
    return redirect('/lab5')


@lab5.route("/lab5/list")
def list():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT id FROM users WHERE login=?;", (login,))

    user_id = cur.fetchone()["id"]

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute(
            "SELECT * FROM articles "
            "WHERE user_id=%s "
            "ORDER BY is_favorite DESC, id;",
            (user_id,)
        )
    else:
        cur.execute(
            "SELECT * FROM articles "
            "WHERE user_id=? "
            "ORDER BY is_favorite DESC, id;",
            (user_id,)
        )

   
    articles = cur.fetchall()
    db_close(conn, cur)
    return render_template('lab5/articles.html', articles=articles)


@lab5.route('/lab5/logout')
def logout():
    session.pop('login', None)
    return redirect('/lab5/')


@lab5.route('/lab5/edit/<int:article_id>', methods=['GET', 'POST'])
def edit_article(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT id FROM users WHERE login=?;", (login,))

    user_id = cur.fetchone()['id']

    if request.method == 'GET':
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute(
                "SELECT * FROM articles WHERE id=%s AND user_id=%s;",
                (article_id, user_id)
            )
        else:
            cur.execute(
                "SELECT * FROM articles WHERE id=? AND user_id=?;",
                (article_id, user_id)
            )
        article = cur.fetchone()
        db_close(conn, cur)

        if not article:
            return redirect('/lab5/list')

        return render_template('lab5/edit_article.html', article=article)

    title = request.form.get('title', '').strip()
    article_text = request.form.get('article_text', '').strip()

    if not title or not article_text:
        db_close(conn, cur)
        return render_template(
            'lab5/edit_article.html',
            article={'id': article_id, 'title': title, 'article_text': article_text},
            error='Заполните и заголовок, и текст статьи'
        )

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute(
            "UPDATE articles SET title=%s, article_text=%s WHERE id=%s AND user_id=%s;",
            (title, article_text, article_id, user_id)
        )
    else:
        cur.execute(
            "UPDATE articles SET title=?, article_text=? WHERE id=? AND user_id=?;",
            (title, article_text, article_id, user_id)
        )

    db_close(conn, cur)
    return redirect('/lab5/list')

@lab5.route('/lab5/delete/<int:article_id>', methods=['POST'])
def delete_article(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT id FROM users WHERE login=?;", (login,))

    user_id = cur.fetchone()['id']

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute(
            "DELETE FROM articles WHERE id=%s AND user_id=%s;",
            (article_id, user_id)
        )
    else:
        cur.execute(
            "DELETE FROM articles WHERE id=? AND user_id=?;",
            (article_id, user_id)
        )

    db_close(conn, cur)
    return redirect('/lab5/list')


@lab5.route('/lab5/profile', methods=['GET', 'POST'])
def profile():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT * FROM users WHERE login=?;", (login,))

    user = cur.fetchone()

    if request.method == 'GET':
        db_close(conn, cur)
        return render_template('lab5/profile.html', user=user)

    full_name = request.form.get('full_name', '').strip()
    password = request.form.get('password', '').strip()
    password2 = request.form.get('password2', '').strip()

    if not full_name:
        db_close(conn, cur)
        return render_template(
            'lab5/profile.html',
            user=user,
            error="Имя не может быть пустым"
        )

    if password or password2:
        if password != password2:
            db_close(conn, cur)
            return render_template(
                'lab5/profile.html',
                user=user,
                error="Пароль и подтверждение не совпадают"
            )
        password_hash = generate_password_hash(password)
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute(
                "UPDATE users SET full_name=%s, password=%s WHERE login=%s;",
                (full_name, password_hash, login)
            )
        else:
            cur.execute(
                "UPDATE users SET full_name=?, password=? WHERE login=?;",
                (full_name, password_hash, login)
            )
    else:
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute(
                "UPDATE users SET full_name=%s WHERE login=%s;",
                (full_name, login)
            )
        else:
            cur.execute(
                "UPDATE users SET full_name=? WHERE login=?;",
                (full_name, login)
            )

    db_close(conn, cur)
    return redirect('/lab5/')

@lab5.route('/lab5/users')
def users():
    conn, cur = db_connect()

    cur.execute("SELECT login, full_name FROM users ORDER BY login;")
    users_list = cur.fetchall()

    db_close(conn, cur)
    return render_template('lab5/users.html', users=users_list)

@lab5.route('/lab5/public')
def public_articles():
    conn, cur = db_connect()

    cur.execute(
        "SELECT a.*, u.login, u.full_name "
        "FROM articles a "
        "JOIN users u ON a.user_id = u.id "
        "WHERE a.is_public "
        "ORDER BY a.is_favorite DESC, a.id;"
    )

    articles = cur.fetchall()
    db_close(conn, cur)
    return render_template('lab5/public_articles.html', articles=articles)