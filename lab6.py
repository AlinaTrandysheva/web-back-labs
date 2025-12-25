from flask import Blueprint, render_template, request, session
from lab5 import db_connect, db_close

lab6 = Blueprint('lab6', __name__)


@lab6.route('/lab6/')
def main():
    return render_template('lab6/lab6.html')

@lab6.route('/lab6/json-rpc-api/', methods = ['POST'])
def api():
    data = request.json
    id = data['id']
    
    conn, cur = db_connect()
    cur.execute("SELECT number, tenant, price FROM offices ORDER BY number;")
    rows = cur.fetchall()

    offices = []
    for row in rows:
        offices.append({
            'number': row['number'],
            'tenant': row['tenant'] or '',
            'price': row['price']
        })
    
    if data['method'] == 'info':
        db_close(conn, cur)
        return {
            'jsonrpc': '2.0',
            'result': offices,
            'id': id
        }

    login = session.get('login')
    if not login:
        db_close(conn, cur)
        return {
            'jsonrpc': '2.0',
            'error': {
                'code': 1,
                'message': 'Вы не авторизованы'
            },
            'id': id
        }

    if data['method'] == 'booking':
        office_number = data['params']
        for office in offices:
            if office['number'] == office_number:

                if office['tenant']:
                    db_close(conn, cur)
                    return {
                        'jsonrpc': '2.0',
                        'error': {
                            'code': 2,
                            'message': 'Офис уже арендуется'
                        },
                        'id': id
                    }

                office['tenant'] = login
                cur.execute(
                    "UPDATE offices SET tenant = %s WHERE number = %s;",
                    (login, office_number)
                )
                db_close(conn, cur)
                return {
                    'jsonrpc': '2.0',
                    'result': 'success',
                    'id': id
                }
    
    
    if data['method'] == 'cancellation':
        office_number = data['params']
        for office in offices:
            if office['number'] == office_number:

                if not office['tenant']:
                    db_close(conn, cur)
                    return {
                        'jsonrpc': '2.0',
                        'error': {
                            'code': 3,
                            'message': 'Офис не арендуется'
                        },
                        'id': id
                    }
            
                if office['tenant'] != login:
                    db_close(conn, cur)
                    return {
                        'jsonrpc': '2.0',
                        'error': {
                            'code': 4,
                            'message': 'Нельзя снять чужую аренду'
                        },
                        'id': id
                    }
            
                office['tenant'] = ''
                cur.execute(
                    "UPDATE offices SET tenant = '' WHERE number = %s;",
                    (office_number,)
                )
                db_close(conn, cur)
                return {
                    'jsonrpc': '2.0',
                    'result': 'success',
                    'id': id
                }    

    db_close(conn, cur)
    return {
        'jsonrpc': '2.0',
        'error': {
            'code': -32601,
            'message': 'Метод не найден'
        },
        'id': id
    }
