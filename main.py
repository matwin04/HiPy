import os.path
import serial
from bottle import request, route, run, static_file, template, redirect
from bottle_pymysql import pymysql
import socket
import sqlite3
import logging


logging.basicConfig(level=logging.DEBUG)
hostname = socket.gethostname()
IPAddr = "192.168.10.110"
DATABASE = 'hipy.db'
SQL_SCRIPT = 'createdb.sql'
avr_status = "STANDBY"
avr_source = "NA"
def connectDB():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn
def initDB():
    if not os.path.exists(DATABASE):
        with sqlite3.connect(DATABASE) as conn:
            with open(SQL_SCRIPT,'r') as f:
                conn.executescript(f.read())

def getSources():
    conn = connectDB()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sources")
    result = cursor.fetchall()
    conn.close()
    return result
@route('/')
def index():
    avr_sources = getSources()
    return template('./pages/index.html',
                    rows=avr_sources,
                    status=avr_status,
                    )
@route('/pw', method='POST')
def toggle():
    global avr_status
    try:
        ser = serial.Serial('/dev/ttyUSB0',baudrate=9600)
        if avr_status == "STANDBY":
            ser.write(b'PWON\r')
            avr_status="ON"
        else:
            ser.write(b'PWSTANDBY\r')
            avr_status="STANDBY"
        ser.close()
    except Exception as e:
        avr_status = "ERROR:" + str(e)
    return redirect('/')
@route('/si/<source>', method='GET')
def switch_source(source):
    try:
        ser = serial.Serial('/dev/ttyUSB0', 9600)
        command = f'SI{source.upper()}\r'.encode()
        logging.debug(f'Sending command: {command}')
        ser.write(command)
        ser.close()
    except Exception as e:
        return "Error: " + str(e)
    return redirect('/')
initDB()
run(host=IPAddr, port=5159, reloader=True, debug=True)