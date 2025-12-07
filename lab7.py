from flask import Blueprint, render_template, request, abort, jsonify, g
from datetime import datetime
import sqlite3

lab7 = Blueprint('lab7', __name__)

DATABASE = 'films.db'

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    db = get_db()
    db.execute('''
        CREATE TABLE IF NOT EXISTS films (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            title_ru TEXT NOT NULL,
            year INTEGER NOT NULL,
            description TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    db.execute('CREATE INDEX IF NOT EXISTS idx_films_year ON films(year)')
    db.execute('CREATE INDEX IF NOT EXISTS idx_films_title ON films(title)')
    db.execute('CREATE INDEX IF NOT EXISTS idx_films_title_ru ON films(title_ru)')
    db.commit()

def add_initial_data():
    db = get_db()
    count = db.execute('SELECT COUNT(*) as cnt FROM films').fetchone()['cnt']
    
    if count == 0:
        initial_films = [
            ("Inception", "Начало", 2010, "Вор, который крадёт секреты из подсознания, получает шанс очистить имя, внедрив идею в чужой сон."),
            ("Interstellar", "Интерстеллар", 2014, "Группа учёных отправляется через червоточину, чтобы найти новый дом для человечества."),
            ("The Matrix", "Матрица", 1999, "Хакер узнаёт, что его мир — это иллюзия, созданная машинами, и присоединяется к сопротивлению.")
        ]
        
        for film in initial_films:
            db.execute('INSERT INTO films (title, title_ru, year, description) VALUES (?, ?, ?, ?)', film)
        
        db.commit()

@lab7.before_app_request
def before_request():
    g.db = get_db()

@lab7.teardown_app_request
def teardown_request(exception=None):
    close_db()

@lab7.route('/lab7/')
def main():
    try:
        init_db()
        add_initial_data()
    except:
        pass
    return render_template('lab7/index.html')

def film_to_dict(row):
    return {
        'id': row['id'],
        'title': row['title'],
        'title_ru': row['title_ru'],
        'year': row['year'],
        'description': row['description']
    }

def validate_film(film):
    errors = {}
    
    title_ru = film.get('title_ru', '').strip()
    if not title_ru:
        errors['title_ru'] = 'Заполните русское название'
    else:
        film['title_ru'] = title_ru
    
    title = film.get('title', '').strip()
    
    if not title and not title_ru:
        errors['title'] = 'Заполните хотя бы одно название'
    elif not title:
        film['title'] = title_ru
    else:
        film['title'] = title
    
    year_str = film.get('year')
    current_year = datetime.now().year
    
    if not year_str and year_str != 0:
        errors['year'] = 'Заполните год выпуска'
    else:
        try:
            year_int = int(year_str)
            if year_int < 1895:
                errors['year'] = 'Год должен быть не раньше 1895'
            elif year_int > current_year:
                errors['year'] = f'Год не может быть больше {current_year}'
            film['year'] = year_int
        except (ValueError, TypeError):
            errors['year'] = 'Год должен быть числом'
    
    description = film.get('description', '').strip()
    if not description:
        errors['description'] = 'Заполните описание'
    elif len(description) > 2000:
        errors['description'] = 'Описание не должно превышать 2000 символов'
    else:
        film['description'] = description
    
    return errors

@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    db = get_db()
    films = db.execute('SELECT * FROM films ORDER BY year DESC').fetchall()
    return jsonify([film_to_dict(film) for film in films])

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def get_film(id):
    db = get_db()
    film = db.execute('SELECT * FROM films WHERE id = ?', (id,)).fetchone()
    
    if film is None:
        abort(404)
    
    return jsonify(film_to_dict(film))

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def del_film(id):
    db = get_db()
    film = db.execute('SELECT * FROM films WHERE id = ?', (id,)).fetchone()
    if film is None:
        abort(404)
    
    db.execute('DELETE FROM films WHERE id = ?', (id,))
    db.commit()
    
    return '', 204

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])
def put_film(id):
    db = get_db()
    film_exists = db.execute('SELECT id FROM films WHERE id = ?', (id,)).fetchone()
    if film_exists is None:
        abort(404)
    
    film = request.get_json()
    errors = validate_film(film)
    
    if errors:
        return jsonify(errors), 400
    
    db.execute('UPDATE films SET title = ?, title_ru = ?, year = ?, description = ? WHERE id = ?', 
               (film['title'], film['title_ru'], film['year'], film['description'], id))
    db.commit()
    
    return '', 204

@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
    film = request.get_json()
    errors = validate_film(film)
    
    if errors:
        return jsonify(errors), 400
    
    db = get_db()
    cursor = db.execute('INSERT INTO films (title, title_ru, year, description) VALUES (?, ?, ?, ?)', 
                       (film['title'], film['title_ru'], film['year'], film['description']))
    db.commit()
    
    new_id = cursor.lastrowid
    return jsonify({'id': new_id}), 201