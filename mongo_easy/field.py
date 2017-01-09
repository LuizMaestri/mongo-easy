from mongo_easy.exceptions import (InvalidTypeException,
                                   InvalidValueException,
                                   InvalidDefaultValueException)
from bson import ObjectId


def valid(value):
    return value is None or value is not None


class Field(dict):

    def __init__(
            self,
            _type,
            not_none=True,
            default=None,
            validator=valid,
            index=None
    ):
        super().__init__()
        value = default if not callable(default) else default()
        self.not_none = not_none

        def is_valid(_value):
            if not_none and _value is None:
                raise InvalidValueException(_value)
            if not isinstance(_value, (_type, type(None))):
                raise InvalidTypeException(_value, _type)
            if not validator(_value):
                raise InvalidValueException(_value)
        self.validator = is_valid
        if index:
            print(index)
        try:
            print(type(value))
            self['value'] = value
        except Exception as e:
            raise InvalidDefaultValueException(value)

        def not_none():
            doc = "The not_none property."

            def fget(self):
                return self._not_none

            def fset(self, value):
                if self._not_none is None:
                    self._not_none = value

            def fdel(self):
                del self._not_none
            return locals()
        not_none = property(**not_none())

    def set_value(self, value):
        self.validator(value)
        super().__setitem__('value', value)

    def __setitem__(self, key, value):
        if key != 'value':
            raise KeyError(key)
        self.set_value(value)


class DictField(dict):

    class IdField(Field):

        def __init__(self):
            super().__init__(
                ObjectId,
                default=ObjectId,
                validator=ObjectId.is_valid
            )

    def __init__(self, **kwargs):
        super().__init__()
        if '_id' not in kwargs:
            self['_id'] = DictField.IdField()


    def __setitem__(self, key, value):
        if not isinstance(value, Field):
            raise InvalidTypeException(value, Field)
        super().__setitem__(key, value)
