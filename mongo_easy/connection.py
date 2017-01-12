from pymongo import MongoClient


class __Connection(type):
    def __getitem__(cls, key):
        return cls.__connections__[key]



class Connection(object, metaclass=__Connection):

    __connections__ = {}


    def __new__(cls, database, host, port):
        if not cls.__connections__.get(database, None):
            cls.__connections__[database] = MongoClient(host, port)
        return cls.__connections__[database]

    @staticmethod
    def register(database, host='localhost', port=27017):
        Connection(database, host, port)
        def __register(cls):
            cls.__database__ = database
            return cls
        return __register

    def __getitem__(self, database):
        return Connection.__connections__.get(database, None)

    @classmethod
    def get_database(cls, database):
        return cls[database][database]
