import pymysql
import csv


val1 = []
val2 = []

f1 = open('C:\\Users\\Kosmo\\Desktop\\RKR\\PyDjango\\pj_team1\\room_escape\\지점.csv', encoding='cp949')
rd1 = csv.reader(f1)
for line in rd1:
    list = tuple(line)
    val1.append(list)
f1.close()

f2 = open('C:\\Users\\Kosmo\\Desktop\\RKR\\PyDjango\\pj_team1\\room_escape\\테마.csv', encoding='cp949')
rd2 = csv.reader(f2)
for line in rd2:
    list = tuple(line)
    val2.append(list)
f2.close()

conn = pymysql.connect(host='localhost',
                       user='team1',
                       password='team1',
                       db='escape',
                       charset='utf8mb4')

sql_1 = "INSERT INTO room_escape_room (room, loc, url, tel, img_path, theme_number, star) VALUES (%s, %s, %s, %s, %s, 0, 0)"
sql_2 = "INSERT INTO room_escape_theme (theme, room, img_path, genre, people, info, difficulty, horror, activity, star, recommend) VALUES (%s, (SELECT room FROM room_escape_room WHERE room = %s), %s, %s, %s, %s, 0, 0, 0, 0, 0)"


with conn:
    with conn.cursor() as cur:
        cur.executemany(sql_1, val1)
        cur.executemany(sql_2, val2)
        conn.commit()

