import sqlite3

conn = sqlite3.connect('game_data.db')
cursor = conn.cursor()

# cursor.execute('CREATE TABLE User(username, id, password)')

cursor.execute("INSERT INTO User (username, id, password) VALUES (?, ?, ?)", ('administor', 'SmartFarm', 'smartfarm208!'))
conn.commit()
conn.close()

