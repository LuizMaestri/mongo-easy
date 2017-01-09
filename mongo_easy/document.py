from mongo_easy.field import DictField, Field


class Document(dict):

    __database__ = ''
    __structure__ = DictField()

    def __init__(self, **kwargs):
        super().__init__()
        for key in [k for k, v in self.__structure__.items() if v.not_none]:
            value = kwargs.get(key, None)
            if value is None:
                
            if key in kwargs:
                del kwargs[key]
        for k, v in kwargs.items():
            self[k] = v

        def __setitem__(self, key, value):
            self.__structure__[key] = value
            super().__setitem__(key, value)


class User(Document):

    __structure__ = DictField(
        name=Field(str, default=''),
        username=Field(str, not_none=False),
        password=Field(str, not_none=False),
        son=Field(Document, not_none=False)
    )

print(User(name='ká', son=User(name='luiz')))
