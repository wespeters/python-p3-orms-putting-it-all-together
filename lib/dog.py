import sqlite3

CONN = sqlite3.connect('lib/dogs.db')
CURSOR = CONN.cursor()

class Dog:

    def __init__(self, name, breed, id=None):
        self.name = name
        self.breed = breed
        self.id = id

    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS dogs
                (id INTEGER PRIMARY KEY,
                name TEXT,
                breed TEXT)
        """
        CURSOR.execute(sql)

    @classmethod
    def drop_table(cls):
        sql = "DROP TABLE IF EXISTS dogs"
        CURSOR.execute(sql)

    def save(self):
        if self.id is None:
            sql = """
                INSERT INTO dogs (name, breed)
                VALUES (?, ?)
            """
            CURSOR.execute(sql, (self.name, self.breed))
            self.id = CURSOR.lastrowid
        else:
            self.update()
        
        return self

    @classmethod
    def create(cls, name, breed):
        dog = cls(name, breed)
        return dog.save()

    @classmethod
    def new_from_db(cls, row):
        return cls(row[1], row[2], row[0])

    @classmethod
    def get_all(cls):
        sql = "SELECT * FROM dogs"
        rows = CURSOR.execute(sql).fetchall()
        return [cls.new_from_db(row) for row in rows]

    @classmethod
    def find_by_name(cls, name):
        sql = """
            SELECT * FROM dogs
            WHERE name=?
            LIMIT 1
        """
        row = CURSOR.execute(sql, (name,)).fetchone()
        return cls.new_from_db(row) if row else None

    @classmethod
    def find_by_id(cls, id):
        sql = """
            SELECT * FROM dogs
            WHERE id=?
            LIMIT 1
        """
        row = CURSOR.execute(sql, (id,)).fetchone()
        return cls.new_from_db(row) if row else None

    @classmethod
    def find_or_create_by(cls, name, breed):
        dog = cls.find_by_name(name)
        if dog and dog.breed == breed:
            return dog
        else:
            return cls.create(name, breed)

    def update(self):
        sql = """
            UPDATE dogs
            SET name=?, breed=?
            WHERE id=?
        """
        CURSOR.execute(sql, (self.name, self.breed, self.id))
