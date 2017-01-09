from mongo_easy.field import DictField, Field


class Document(dict):

    STRUCTURE = DictField()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        struct = self.STRUCTURE
        print(struct)

class User(Document):

    STRUCTURE = DictField(
        name=Field(str),
        username=Field(str),
        password=Field(str),
        son=Field(Document)
    )

print(User(son=User(name='luiz')))
