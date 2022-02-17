import socket
import json
import sqlite3


sock = socket.socket()
sock.bind(('', 5000))
sock.listen(1000)
while True:
    conn, addr = sock.accept()
    print('connected:', addr)
    data = conn.recv(1024)
    if data:
        mes = json.loads(data.decode("utf-8"))['text']
        if mes.split()[0].lower() == 'найти':
            string = ' '.join(mes.split()[1:])
            conn = sqlite3.connect('tracks.db')
            cursor = conn.cursor()
            sql_request = '''
            SELECT
                title,
                url
            FROM tracks
            WHERE MATCH(text) AGAINST (?);'''
            cursor.execute(sql_request, string)
            rows = cursor.fetchall()
            cursor.close()
            conn.close()
