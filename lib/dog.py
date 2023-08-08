import sqlite3
from config import CONN, CURSOR

# CONN = sqlite3.connect('lib/dogs.db')
# CURSOR = CONN.cursor()

class Dog:

    all = []
    
    def __init__(self, name, breed):
        self.id = None
        self.name = name
        self.breed = breed
    
    @classmethod
    def create_table(cls):
        sql = '''
                create table if not exists dogs (
                    id integer primary key,
                    name text,
                    breed text
                )
        '''
        CURSOR.execute(sql)
    
    @classmethod
    def drop_table(cls):
        sql = '''
                drop table if exists dogs
        '''
        CURSOR.execute(sql)
    
    def save(self):
        sql = '''
                insert into dogs (name, breed)
                values (?, ?)
        '''
        CURSOR.execute(sql, (self.name, self.breed))
        self.id = CURSOR.execute('select last_insert_rowid() from dogs').fetchone()[0]

    @classmethod
    def create(cls, name, breed):
        dog = Dog(name, breed)
        dog.save()
        return dog
    
    @classmethod
    def new_from_db(cls, row):
        dog = cls(row[1], row[2])
        dog.id = row[0]
        return dog
    
    @classmethod
    def get_all(cls):
        sql = '''
                select * from dogs
        '''
        data = CURSOR.execute(sql).fetchall()
        cls.all = [cls.new_from_db(row) for row in data]
        return cls.all

    @classmethod
    def find_by_name(cls, name):
        sql = '''
                select * from dogs
                where name = ?
                limit 1
        '''
        dog = CURSOR.execute(sql, (name,)).fetchone()
        return cls.new_from_db(dog)
    
    @classmethod
    def find_by_id(cls, id):
        sql = '''
                select * from dogs
                where id = ?
                limit 1
        '''
        dog = CURSOR.execute(sql, (id, )).fetchone()
        return cls.new_from_db(dog)





