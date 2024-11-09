import sqlite3

connection = sqlite3.connect('not_telegram.db')
cursor = connection.cursor()

# cursor.execute('''
# CREATE TABLE IF NOT EXISTS Users(
# id INTEGER PRIMARY KEY,
# username TEXT NOT NULL,
# email TEXT NOT NULL,
# age INTEGER,
# balance INTEGER NOT NULL)
# ''')
#
# for i in range(1, 11):
#     cursor.execute('INSERT INTO Users(username, email, age, balance) VALUES(?, ?, ?, ?)',
#                    (f'User{i}', f'example{i}@gmail.com', f'{i * 10}', '1000'))
#
# for i in range(1, 11, 2):
#     cursor.execute('UPDATE Users SET balance = ? WHERE id = ?', (500, f'{i}'))
#
# for i in range(1, 11, 3):
#     cursor.execute('DELETE FROM Users WHERE id = ?', (f'{i}',))
#
# cursor.execute('SELECT username, email, age, balance FROM Users WHERE age != 60')
# result = cursor.fetchall()
# for row in result:
#     username, email, age, balance = row
#     print(f'Name: {username} | E-mail: {email} | Age: {age} | Balance: {balance}')

cursor.execute('DELETE FROM Users WHERE id = 6')  # Removing user from table whose id equals 6

cursor.execute('SELECT COUNT(*) FROM Users')
result_amount = cursor.fetchall()[0][0]
print(f'Records amount: {result_amount}')

cursor.execute('SELECT SUM(balance) FROM Users')
result_sum_balance = cursor.fetchone()[0]
print(f'Total balance of users: {result_sum_balance}')

cursor.execute('SELECT AVG(balance) FROM Users')
result_avg_balance = cursor.fetchone()[0]
print(f"Average users' balance: {result_avg_balance}")

connection.commit()
connection.close()
