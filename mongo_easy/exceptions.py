class InvalidTypeException(Exception):

    def __init__(self, value, _type):
        super().__init__('Value "%s" isn\'t a instance of %s' %
                         (str(value), str(_type)))


class InvalidValueException(Exception):

    def __init__(self, value):
        super().__init__('Value "%s" isn\'t valid' % str(value))


class InvalidDefaultValueException(Exception):

    def __init__(self, value):
        super().__init__('Default Value isn\'t valid: %s' % str(value))
