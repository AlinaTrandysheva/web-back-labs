from flask import Flask, url_for, request, redirect, abort, render_template
from lab1 import lab1
from lab2 import lab2
from lab3 import lab3
import datetime

app = Flask(__name__)
app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)

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
                <li><a href="/lab2">Вторая лабораторная</a></li>
                <li><a href="/lab3/">Третья лабораторная</a></li>
            </ul>
        </nav>
        <footer>
            <p>Трандышева Алина Константиновна, ФБИ-34, 3 курс, 2025</p>
        </footer>
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





not_found_log = []

@app.route("/404")
def not_found():
    client_ip = request.remote_addr
    access_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    requested_url = request.url
    
    log_entry = f"{access_time} - {client_ip} - {requested_url}"
    not_found_log.append(log_entry)
    
    image_path = url_for("static", filename="lab1/ошибка.webp")
    
    log_html = "<h3>Журнал:</h3>"
    for entry in not_found_log[-5:]:  
        log_html += f"<p>{entry}</p>"
    
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
        <p><strong>Ваш IP:</strong> {client_ip}</p>
        <p><strong>Время доступа:</strong> {access_time}</p>
        <img src="{image_path}" alt="Not found">
        <p><a href="/">Вернуться на главную страницу</a></p>
        
        {log_html}
        
        <p><small>Всего обращений: {len(not_found_log)}</small></p>
    </body>
</html>''', 404


