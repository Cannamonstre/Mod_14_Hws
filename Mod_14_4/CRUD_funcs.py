import sqlite3

connection = sqlite3.connect('Mod_14_4.db')
cursor = connection.cursor()

price_multiplier_num = 4.20


def db_initiator():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products(
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    price INTEGER NOT NULL)
    ''')
    connection.commit()


def get_all_products():
    cursor.execute('SELECT * FROM Products')
    res = cursor.fetchall()
    return res


# db_initiator()
#
# for i in range(1, 5):
#     cursor.execute('INSERT INTO Products(title, description, price) VALUES(?, ?, ?)',
#                    (f'prod{i}', f'desc{i}', 333))
#
# cursor.execute('UPDATE Products SET title = ?, description = ?, price = ? WHERE id = 1',
#                ('№1 Protein',
#                 'High-quality protein powder to support muscle growth and recovery',
#                 f'{round(price_multiplier_num * 4.2, 2)}'))
#
# cursor.execute('UPDATE Products SET title = ?, description = ?, price = ? WHERE id = 2',
#                ('Gold Standard Casein',
#                 'Slow-digesting protein for sustained muscle support during sleep',
#                 f'{round(price_multiplier_num * 5.1, 2)}'))
#
# cursor.execute('UPDATE Products SET title = ?, description = ?, price = ? WHERE id = 3',
#                ('GLS Creatine Monohydrate Powder',
#                 'Boosts muscle strength and power, enhancing workout performance',
#                 f'{round(price_multiplier_num * 3.5, 2)}'))
#
# cursor.execute('UPDATE Products SET title = ?, description = ?, price = ? WHERE id = 4',
#                ('GLS BCAA Powder',
#                 'Branched-chain amino acids for muscle repair and reduced fatigue',
#                 f'{round(price_multiplier_num * 3.2, 2)}'))
#
# connection.commit()
