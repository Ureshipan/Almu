"""INSERT INTO tra (text, title, url)
VALUES (?, ?, ?);"""
import sqlite3
import re
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
sql_request = 'SELECT * FROM tra WHERE text LIKE "%тыконечно%"'
cursor.execute(sql_request)
print(*cursor.fetchall())
cursor.close()
con.close()