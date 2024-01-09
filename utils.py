import sqlite3
from decouple import config


class Database:

    def __init__(self):
        self._conn = sqlite3.connect('db')
        self._cur = self._conn.cursor()
        try:
            self._cur.execute('CREATE TABLE admins (id)')
            self._conn.execute('CREATE TABLE words (title)')
            self.add_admin(config('DEFAULT_ADMIN', cast=int))
        except:
            pass

    def commit(self) -> None:
        self._conn.commit()

    def admins(self):
        result = self._cur.execute(f'SELECT * FROM admins')
        return [res[0] for res in result.fetchall()]

    def add_admin(self, id) -> None:
        self._cur.execute(f'INSERT INTO admins VALUES ({id})')
        self.commit()

    def remove_admin(self, id) -> None:
        self._cur.execute(f'DELETE FROM admins WHERE id={id};')
        self.commit()

    def admin_exists(self, id):
        result = self._cur.execute(f'SELECT * FROM admins WHERE id={id}')
        if result.fetchone():
            return True
        else:
            return False

    def words(self):
        result = self._cur.execute(f'SELECT * FROM words')
        return [res[0] for res in result.fetchall()]

    def add_word(self, word) -> None:
        self._cur.execute(f'INSERT INTO words VALUES ("{word}")')
        self.commit()

    def remove_word(self, word) -> None:
        self._cur.execute(f'DELETE FROM words WHERE title="{word}";')
        self.commit()

    def word_exists(self, word):
        result = self._cur.execute(f'SELECT * FROM words WHERE title="{word}"')
        if result.fetchone():
            return True
        else:
            return False

    def __str__(self):
        return f"Admins : {len(self.admins())}\nWords : {len(self.words())}"


db = Database()
