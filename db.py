import sqlite3

def create_table():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE Transferencias
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  cellphone TEXT(10),
                  amount REAL,
                  description TEXT(255))''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_table()