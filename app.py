from flask import Flask, url_for, request, redirect
import datetime
app = Flask(__name__)

@app.route("/")
@app.route("/lab1/web")
def web():
    return """<!doctype html> 
        <html>
            <body>
                <h1>web-сервер на flask</h1>
                <a href="/lab1/author">author</a>
            </body>
        </html>""", 200, {
            "X-Server": "sample",
            'Content-Type': 'text/plain; charset=utf-8'}
        
@app.route("/lab1/author")
def author():
    name = "Трандышева Алина Константиновна"
    group = "ФБИ-34"
    faculty = "ФБ"

    return """<!doctype html>
        <html>
            <body>
                <p>Студент: """ + name + """</p>
                <p>Группа: """ + group + """</p>
                <p>Факультет: """ + faculty + """</p>
                <a href="/lab1/web">web</a>
            </body>
        </html>"""



count = 0

@app.route('/lab1/counter')
def counter():
    global count
    count +=1
    time = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
    url = request.url
    client_ip = request.remote_addr
    reset_url = url_for("reset_counter")

    return f"""
    <!doctype html>
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

@app.route('/reset_counter')
def reset_counter():
    global count
    count = 0
    return f"""
    <!doctype html>
    <html>
        <body>
            Счётчик очищен <br>
            <a href="{url_for("counter")}">Вернуться к счётчику</a>
        </body>
    </html>
    """

@app.route("/lab1/info")
def info():
    return redirect("/lab1/author")


@app.route("/created")
def created():
    return '''
<!doctype html"
<html>
    <body>
        <h1>Создано успешно</h1>
        <div><i>что-то создано...</i></div>
    </body>
</html>
''',201


@app.route("/")
@app.route("/index")
def index():
    return '''<!doctype html> 
<html>
    <head>
        <title>НГТУ, ФБ, Лабораторные работы</title>
    </head>
    <body>
        <h1>НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных</h1>
        <nav>
            <ul>
                <li><a href="/lab1">Первая лабораторная</a></li>
            </ul>
        </nav>
        <footer>
            <p>Трандышева Алина Константиновна, ФБИ-34, 3 курс, 2025</p>
        </footer>
    </body>
</html>'''

@app.route("/lab1")
def lab1():
    return '''<!doctype html>
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
        <a href="/">Корень сайта</a>
    </body>
</html>'''


@app.route("/400")
def bad_request():
    return '''<!doctype html>
<html>
    <head>
        <title>400 Bad Request</title>
    </head>
    <body>
        <h1>400 Bad Request</h1>
        <p>Сервер не может обработать запрос из-за неверного синтаксиса</p>
    </body>
</html>''', 400

@app.route("/401")
def unauthorized():
    return '''<!doctype html>
<html>
    <head>
        <title>401 Unauthorized</title>
    </head>
    <body>
        <h1>401 Unauthorized</h1>
        <p>Требуется аутентификация для доступа к ресурсу</p>
    </body>
</html>''', 401

@app.route("/402")
def payment_required():
    return '''<!doctype html>
<html>
    <head>
        <title>402 Payment Required</title>
    </head>
    <body>
        <h1>402 Payment Required</h1>
        <p>Требуется оплата для доступа к ресурсу</p>
    </body>
</html>''', 402

@app.route("/403")
def forbidden():
    return '''<!doctype html>
<html>
    <head>
        <title>403 Forbidden</title>
    </head>
    <body>
        <h1>403 Forbidden</h1>
        <p>Доступ к ресурсу запрещен</p>
    </body>
</html>''', 403

@app.route("/405")
def method_not_allowed():
    return '''<!doctype html>
<html>
    <head>
        <title>405 Method Not Allowed</title>
    </head>
    <body>
        <h1>405 Method Not Allowed</h1>
        <p>Метод не разрешен для данного ресурса</p>
    </body>
</html>''', 405

@app.route("/418")
def teapot():
    return '''<!doctype html>
<html>
    <head>
        <title>418 I'm a teapot</title>
    </head>
    <body>
        <h1>418 I'm a teapot</h1>
        <p>Я чайник и не могу заваривать кофе</p>
    </body>
</html>''', 418


@app.route("/404")
def not_found():
    image_path = url_for("static", filename="ошибка.webp")
    return f'''<!doctype html>
<html>
    <head>
        <title>404 Not Found</title>
        <style>
            body {{
                background: pink;
                color: #333;
                font-family: Arial;
                text-align: center;
                padding: 50px;
            }}
            h1 {{
                color: #dc3545;
                font-size: 50px;
            }}
            img {{
                width: 200px;
                margin: 20px;
            }}
            a {{
                color: #007bff;
            }}
        </style>
    </head>
    <body>
        <h1>404</h1>
        <p>Страница не найдена</p>
        <img src="{image_path}" alt="Not found">
        <p><a href="/">На главную</a></p>
    </body>
</html>''', 404

@app.route("/server_error")
def server_error():
    result = 10 / 0
    return "Эта строка никогда не будет выполнена"

@app.errorhandler(500)
def internal_server_error(error):
    return '''<!doctype html>
<html>
    <head>
        <title>500 Internal Server Error</title>
    </head>
    <body>
        <h1>500 - Ошибка сервера</h1>
        <p>На сервере произошла внутренняя ошибка</p>
        <p><a href="/">Вернуться на главную страницу</a></p>
    </body>
</html>''', 500

@app.route('/image')
def image():
    path = url_for("static", filename="dog.jpg")
    css_path = url_for("static", filename="lab1.css")
    html_content = f'''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" type="text/css" href="{css_path}">
    </head>
    <body>
        <h1>Шпиц</h1>
        <img src="{path}">
    </body>
</html>
'''
    return html_content, 200, {
        'Content-Language': 'ru',
        'X-Custom-App': 'Flask-Image-Server',
        'X-Image-Filename': 'dog.jpg',
        'Content-Type': 'text/html; charset=utf-8'
    }