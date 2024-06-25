import sqlite3

class Database:
    def __init__(self, db_name='emertech_community.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            first_name TEXT,
            last_name TEXT,
            age INTEGER,
            country TEXT,
            skills TEXT,
            occupation TEXT,
            interests TEXT,
            share_knowledge BOOLEAN,
            contribute_meetups BOOLEAN
        )
        ''')
        self.conn.commit()

    def add_user(self, user_data):
        self.cursor.execute('''
        INSERT OR REPLACE INTO users 
        (user_id, first_name, last_name, age, country, skills, occupation, interests, share_knowledge, contribute_meetups) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            user_data['user_id'],
            user_data['first_name'],
            user_data['last_name'],
            user_data['age'],
            user_data['country'],
            user_data['skills'],
            user_data['occupation'],
            user_data['interests'],
            user_data['share_knowledge'],
            user_data['contribute_meetups']
        ))
        self.conn.commit()

    def get_user(self, user_id):
        self.cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        return self.cursor.fetchone()

    def close(self):
        self.conn.close()
