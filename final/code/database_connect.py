import sqlite3

conn = sqlite3.connect('game_data.db')
cursor = conn.cursor()

# cursor.execute('CREATE TABLE User(username, id, password)')

cursor.execute("INSERT INTO User (username, id, password) VALUES (?, ?, ?)",
               ('administor', 'SmartFarm', 'smartfarm208!'))
# cursor.execute("INSERT INTO User (username, id, password) VALUES (?, ?, ?)", ('admin', 'smartfarm', 'smartfarm208!'))

# cursor.execute('DELETE FROM User WHERE username = "admin"')

result = cursor.execute("SELECT * FROM User;")
for row in result:
    print(row)

conn.commit()
conn.close()

