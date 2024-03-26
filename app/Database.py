import pymysql
import toml

class Database(type):
    _instance = None
    def __call__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = super().__call__(*args, **kwargs)
        return cls._instance
    

class Connexion(metaclass=Database):
    def __init__(self):
        with open('app/default.toml','r', encoding="utf8") as f:
            config = toml.load(f)
            self.adress = config['database']['adress']
            self.name = config['database']['name']
            self.user = config['database']['user']
            self.password = config['database']['password']
            return pymysql.connect(host=self.adress,user=self.user,password=self.password,database=self.name,cursorclass=pymysql.cursors.DictCursor)
