import sqlite3


price_multiplier_num = 4.20

# conn = sqlite3.connect('Mod_14_4_products.db')
# cursor = conn.cursor()


def db_initiator_products():
    conn = sqlite3.connect('Mod_14_5_products.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products(
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    price INTEGER NOT NULL)
    ''')

    conn.commit()
    conn.close()


def db_initiator_users():
    conn = sqlite3.connect('Mod_14_5_users.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users(
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    age INTEGER NOT NULL,
    balance INTEGER NOT NULL)
    ''')

    conn.commit()
    conn.close()


def get_all_products():
    conn = sqlite3.connect('Mod_14_5_products.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM Products')
    res = cursor.fetchall()

    conn.close()
    return res


def user_insertion(username, email, age):
    conn = sqlite3.connect('Mod_14_5_users.db')
    cursor = conn.cursor()

    if is_existing:
        cursor.execute('''
        INSERT INTO USERS (username, email, age, balance)
        VALUES (?, ?, ?, 1000)
        ''', (username, email, age))
    else:
        print('The user already exists')

    conn.commit()
    conn.close()


def user_remover(username):
    conn = sqlite3.connect('Mod_14_5_users.db')
    cursor = conn.cursor()

    cursor.execute('DELETE FROM Users WHERE username = ?', (username, ))

    conn.commit()
    conn.close()


def is_existing(username):
    conn = sqlite3.connect('Mod_14_5_users.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT EXISTS(SELECT 1 FROM Users WHERE username = ?)
        ''', (username,))
    result = cursor.fetchone()[0]

    conn.close()
    return result == 1


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
# conn.commit()
# conn.close()
