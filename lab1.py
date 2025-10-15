from flask import Blueprint, url_for, request, redirect, abort, render_template
import datetime

lab1 = Blueprint('lab1', __name__, url_prefix='/lab1')


@lab1.route('/web')
def web():
    return f"""<!doctype html> 
<html>
  <body>
    <h1>web-сервер на flask</h1>
    <a href="{ url_for('lab1.author') }">author</a>
  </body>
</html>""", 200, {
        "X-Server": "sample",
        'Content-Type': 'text/html; charset=utf-8'
    }


@lab1.route('/author')
def author():
    name = "Трандышева Алина Константиновна"
    group = "ФБИ-34"
    faculty = "ФБ"
    return f"""<!doctype html>
<html>
  <body>
    <p>Студент: {name}</p>
    <p>Группа: {group}</p>
    <p>Факультет: {faculty}</p>
    <a href="{ url_for('lab1.web') }">web</a>
  </body>
</html>"""


count = 0

@lab1.route('/counter')
def counter():
    global count
    count += 1
    time = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
    url = request.url
    client_ip = request.remote_addr
    reset_url = url_for('lab1.reset_counter')
    return f"""<!doctype html>
<html>
  <body>
    Сколько раз вы сюда заходили: {count} <br>
    Дата и время: {time} <br>
    Запрошенный адрес: {url} <br>
    Ваш IP-адрес: {client_ip} <br>
    <a href="{reset_url}">Сбросить счётчик</a>
  </body>
</html>
"""


@lab1.route('/info')
def info():
    return redirect(url_for('lab1.author'))


@lab1.route('/created')
def created():
    return """<!doctype html>
<html>
  <body>
    <h1>Создано успешно</h1>
    <div><i>что-то создано...</i></div>
  </body>
</html>
""", 201


@lab1.route('/')
def labflask():
    return f'''<!doctype html>
<html>
  <head>
    <title>Лабораторная 1</title>
  </head>
  <body>
    <p>Flask — фреймворк для создания веб-приложений на языке
    программирования Python, использующий набор инструментов
    Werkzeug, а также шаблонизатор Jinja2. Относится к категории так
    называемых микрофреймворков — минималистичных каркасов
    веб-приложений, сознательно предоставляющих лишь самые базовые возможности.</p>

    <h2>Список роутов</h2>
    <ul>
      <li><a href="{ url_for('index') }">Главная страница</a></li>
      <li><a href="{ url_for('lab1.web') }">/lab1/web</a></li>
      <li><a href="{ url_for('lab1.author') }">/lab1/author</a></li>
      <li><a href="{ url_for('lab1.counter') }">/lab1/counter</a></li>
      <li><a href="{ url_for('lab1.info') }">/lab1/info</a></li>
      <li><a href="{ url_for('lab1.created') }">/lab1/created</a></li>
      <li><a href="{ url_for('lab1.image') }">/lab1/image</a></li>
      <li><a href="/400">/400 Bad Request</a></li>
      <li><a href="/401">/401 Unauthorized</a></li>
      <li><a href="/402">/402 Payment Required</a></li>
      <li><a href="/403">/403 Forbidden</a></li>
      <li><a href="/404">/404 Not Found</a></li>
      <li><a href="/405">/405 Method Not Allowed</a></li>
      <li><a href="/418">/418 I'm a teapot</a></li>
      <li><a href="/server_error">/server_error (500)</a></li>
    </ul>

    <a href="{ url_for('index') }">Корень сайта</a>
  </body>
</html>'''


@lab1.route('/image')
def image():
    img_path = url_for('static', filename='lab1/dog.jpg')
    css_path = url_for('static', filename='lab1/main.css')
    html_content = f'''<!doctype html>
<html>
  <head>
    <link rel="stylesheet" type="text/css" href="{css_path}">
  </head>
  <body>
    <h1>Шпиц</h1>
    <img src="{img_path}">
  </body>
</html>
'''
    return html_content, 200, {
        'Content-Language': 'ru',
        'X-Custom-App': 'Flask-Image-Server',
        'X-Image-Filename': 'dog.jpg',
        'Content-Type': 'text/html; charset=utf-8'
    }


@lab1.route('/reset_counter')
def reset_counter():
    global count
    count = 0
    return f"""<!doctype html>
<html>
  <body>
    Счётчик очищен <br>
    <a href="{ url_for('lab1.counter') }">Вернуться к счётчику</a>
  </body>
</html>
"""
