from mongo_easy.field import Field
from pymongo import MongoClient
from bson import ObjectId

client = MongoClient()


class Document(dict):

    __collection__ = ''
    __database__ = 'teste'
    __structure__ = {
        's': Field(
            _type=str,
            required=True,
            index=False,
            validate=lambda _value: True
        )
    }

    def __init__(self, **kwargs):
        cls = self.__class__
        if not cls.__collection__:
            cls.__collection__ = cls.__name__
        structure = cls.__structure__
        self.__json = {key: None for key in structure}
        for key in structure:
            self[key] = kwargs.get(key, None)

    def __getitem__(self, key):
        return self.__json.get(key, None)

    def __setitem__(self, key, value):
        # validate key
        if key == '_id' and value is None:
            return KeyError(key)
        cls = self.__class__
        structure = {key: _value for key, _value in cls.__structure__}
        if not structure.get('_id', None):
            structure['_id'] = Field(
                _type=ObjectId,
                validate=ObjectId.is_valid(value)
            )
        if not key in structure and '_id' != key:
            raise KeyError(key)
        # validate value
        field = structure[key]
        is_none = value is None
        print(field['required'])
        if field['required'] and is_none:
            raise Exception("Error value None")
        if not is_none and not isinstance(value, field['type']):
            raise Exception("Error type invalid")
        if not callable(field['validate']):
            raise Exception("Error is not a function")
        if not field['validate'](value):
            raise Exception("Error not valid")
        self.__json[key] = value

    def __delitem__(self, key):
        structure = self.__class__.__structure__
        if key not in structure:
            raise KeyError(key)
        field = structure[key]
        self.__json[key] = field['type']() if field['required'] else None

    def __repr__(self):
        return str(self.__json)
