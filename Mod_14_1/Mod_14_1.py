import sqlite3

connection = sqlite3.connect('not_telegram.db')
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Users(
id INTEGER PRIMARY KEY,
username TEXT NOT NULL,
email TEXT NOT NULL,
age INTEGER,
balance INTEGER NOT NULL)
''')

for i in range(1, 11):
    cursor.execute('INSERT INTO Users(username, email, age, balance) VALUES(?, ?, ?, ?)',
                   (f'User{i}', f'example{i}@gmail.com', f'{i * 10}', '1000'))

for i in range(1, 11, 2):
    cursor.execute('UPDATE Users SET balance = ? WHERE id = ?', (500, f'{i}'))

for i in range(1, 11, 3):
    cursor.execute('DELETE FROM Users WHERE id = ?', (f'{i}',))

cursor.execute('SELECT username, email, age, balance FROM Users WHERE age != 60')
result = cursor.fetchall()
for row in result:
    username, email, age, balance = row
    print(f'Name: {username} | E-mail: {email} | Age: {age} | Balance: {balance}')

connection.commit()
connection.close()
