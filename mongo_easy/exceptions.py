class ValidTypeException(Exception):

    def __init__(self, value, _type):
        super().__init__('value "%s" isn\'t a instance of %s' %
                         (str(value), str(_type)))


class ValidException(Exception):

    def __init__(self, value):
        super().__init__('value "%s" isn\'t valid' % (str(value)))
