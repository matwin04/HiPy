from bottle import request, route, run, static_file, template, redirect
from bottle_pymysql import pymysql
import socket

hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)

conn = pymysql.connect(host='localhost',
                       user='root',
                       database='HiPy',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor
                       )
@route('/')
def index():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    result = cursor.fetchall()
    cursor.close()
    return template('./pages/index.html',rows=result)
@route('/music')
def music():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM music")
    result = cursor.fetchall()
    cursor.close()
    return template('./pages/music/music.html',rows=result)


if __name__ == '__main__':
    run(host=IPAddr, port=5159, reloader=True, debug=True)