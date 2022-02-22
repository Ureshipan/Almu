import socket
import json
import sqlite3
import re

sock = socket.socket()
sock.bind(('', 5000))
sock.listen(1000)
con = sqlite3.connect('tracks.db')
cursor = con.cursor()
sql_request1 = 'SELECT text, title, url FROM tracks;'
sql_request2 = 'SELECT text, title, url FROM tra;'
cursor.execute(sql_request1)
rows = cursor.fetchall()
cursor.execute(sql_request2)
new_rows = cursor.fetchall()
for row in rows:
    dna = False
    text = ''.join(re.split('|…|«|»|!|-|:|—|\?| |\.|;|,|\*|\n', row[0])).lower()
    print(text)
    for r in range(len(new_rows)):
        if new_rows[r][2] == row[2]:
            new_rows.pop(r)
            dna = True
            break
    if not dna:
        new_rows.append((text, row[1], row[2]))
ap_req = """INSERT INTO tra (text, title, url)
            VALUES (?, ?, ?);"""
for row in new_rows:
    cursor.execute(ap_req, row)
while True:
    conn, addr = sock.accept()
    print('connected:', addr)
    data = conn.recv(1024)
    if data:
        mes = json.loads(data.decode("utf-8"))['text']
        print(mes)
        if mes.split()[0].lower() == 'найти':
            string = ''.join(re.split('|найти|Найти|…|«|»|!|-|:|—|\?| |\.|;|,|\*|\n', mes)).lower()
            sql_request = 'SELECT * FROM tra WHERE text LIKE "%{}%"'.format(string)
            cursor.execute(sql_request)
            print(*cursor.fetchall())
            cursor.close()
            con.close()
            req = {'title': [], 'url': []}
            for song in rows:
                req['title'].append(song[1])
                req['url'].append(song[2])
            print(req)
            req = json.dumps(req)
            conn.sendall(bytes(req, encoding="utf-8"))
    conn.close()
