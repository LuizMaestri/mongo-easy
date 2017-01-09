from mongo_easy.exceptions import ValidTypeException, ValidException


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
        value = default if not callable(default) else default()
        super().__init__(value=value)

        def is_valid(_value):
            if not_none and _value is None:
                raise ValidException(_value)
            if not isinstance(_value, _type):
                raise ValidTypeException(_value, _type)
            if not validator(_value):
                raise ValidException(_value)
        self.validator = is_valid
        if index:
            print(index)

    def set_value(self, value):
        self.validator(value)
        super().__setitem__('value', value)

    def __setitem__(self, key, value):
        if key != 'value':
            raise KeyError(key)
        self.set_value(value)


class DictField(dict):

    def __setitem__(self, key, value):
        if not isinstance(value, Field):
            raise ValidTypeException(value, Field)
        super().__setitem__(key, value)
