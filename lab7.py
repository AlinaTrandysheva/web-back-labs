from flask import Blueprint, render_template, request, abort


lab7 = Blueprint('lab7', __name__)

@lab7.route('/lab7/')
def main():
    return render_template('lab7/index.html')

films = [
    {
        "title": "Inception",
        "title_ru": "Начало",
        "year": 2010,
        "description": "Вор, который крадёт секреты из подсознания, получает шанс очистить имя, внедрив идею в чужой сон."
    },
    {
        "title": "Interstellar",
        "title_ru": "Интерстеллар",
        "year": 2014,
        "description": "Группа учёных отправляется через червоточину, чтобы найти новый дом для человечества."
    },
    {
        "title": "The Matrix",
        "title_ru": "Матрица",
        "year": 1999,
        "description": "Хакер узнаёт, что его мир — это иллюзия, созданная машинами, и присоединяется к сопротивлению."
    },
    {
        "title": "Titanic",
        "title_ru": "Титаник",
        "year": 1997,
        "description": "Роман молодых людей разворачивается на борту обречённого лайнера «Титаник»."
    },
    {
        "title": "The Lion King",
        "title_ru": "Король Лев",
        "year": 1994,
        "description": "Юный львёнок Симба проходит путь взросления, чтобы принять своё место короля саванны."
    }
]

@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    return films

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def get_film(id):
    if id < 0 or id >= len(films):
        abort(404)   

    return films[id]

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def del_film(id):
    if id < 0 or id >= len(films):
        abort(404)

    del films[id]
    return '', 204

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])
def put_film(id):
    if id < 0 or id >= len(films):
        abort(404)

    film = request.get_json()
    films[id] = film
    return '', 204

@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
    film = request.get_json()    
    films.append(film)              
    new_id = len(films) - 1        
    return str(new_id), 201          
