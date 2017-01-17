from mongo_easy import Connection
from mongo_easy import Field
from bson import ObjectId
from json import loads


@Connection.register('teste')
class Document(dict):

    __structure__ = {
        's': Field(
            _type=str,
            required=True,
            index=False,
            validate=lambda _value: True
        )
    }

    def __init__(self, **kwargs):
        structure = self.__class__.__structure__
        self.__json = {key: None for key in structure}
        for key in structure:
            self[key] = kwargs.get(key, None)

    def __getitem__(self, key):
        if key not in self.__class__.__structure__ and key != '_id':
            raise KeyError(key)
        return self.__json[key]

    def __setitem__(self, key, value):
        # validate key
        if key == '_id' and value is None:
            return KeyError(key)
        cls = self.__class__
        structure = {key: _value for key, _value in cls.__structure__.items()}
        if not structure.get('_id', None):
            structure['_id'] = Field(
                _type=ObjectId,
                validate=ObjectId.is_valid
            )
        if not key in structure:
            raise KeyError(key)
        # validate value
        field = structure[key]
        is_none = value is None
        if field['required'] and is_none:
            raise Exception("Error Value not accepted None")
        if not is_none and not isinstance(value, field['type']):
            raise Exception("Error: Value type is invalid - " + type(value))
        if not callable(field['validate']):
            raise Exception("Error: Validate property in field isn't a function")
        if not field['validate'](value):
            raise Exception("Error: Value is invalid")
        self.__json[key] = value

    def __delitem__(self, key):
        structure = self.__class__.__structure__
        if key not in structure:
            raise KeyError(key)
        field = structure[key]
        self.__json[key] = field['type']() if field['required'] else None

    def __repr__(self):
        return str(self.__json)

    def save(self):
        cls = self.__class__
        collection = Connection.get_database(cls.__database__)[cls.__name__]
        result = collection.update_one(
            {
                '_id': self.get('_id', None)
            }, {
                '$set': loads(str(self).repalce('\'', '"'))
            }
        )
        if result.modified_count == 0:
            collection.insert(self)
