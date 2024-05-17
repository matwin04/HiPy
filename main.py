import os.path

from bottle import request, route, run, static_file, template, redirect
from bottle_pymysql import pymysql
import socket
import sqlite3

hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)
DATABASE = 'hipy.db'
SQL_SCRIPT = 'createdb.sql'
def connectDB():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn
def initDB():
    if not os.path.exists(DATABASE):
        with sqlite3.connect(DATABASE) as conn:
            with open(SQL_SCRIPT,'r') as f:
                conn.executescript(f.read())
@route('/')
def index():
    conn = connectDB()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    result = cursor.fetchall()
    cursor.close()
    return template('./pages/index.html',rows=result)
@route('/music')
def music():
    conn = connectDB()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM music")
    result = cursor.fetchall()
    cursor.close()
    return template('./pages/music/music.html',rows=result)

@route('/music/<artist>')
def artist_details(artist):
    conn = connectDB()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM music WHERE artist = ?',(artist,))
    result = cursor.fetchone()
    cursor.close()
    return template('./pages/music/artist.html',artist=result['artist'])
@route('/photos')
def photos():
    conn = connectDB()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM photos")
    result = cursor.fetchall()
    cursor.close()
    return template('./pages/photos/photos.html',rows=result)
if __name__ == '__main__':
    initDB()
    run(host=IPAddr, port=5159, reloader=True, debug=True)