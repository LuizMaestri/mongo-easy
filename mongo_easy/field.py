class Field(dict):
    """docstring for Field."""
    def __init__(
        self,
        _type=object,
        required=True,
        index=False,
        validate=lambda value: True
    ):
        super().__init__()
        self['type'] = _type
        self['index'] = index
        self['validate'] = validate
        self['required'] = required

    def __setitem__(self, key, value):
        if key not in ['type', 'index', 'validate', 'required']:
            raise KeyError(key)
        super().__setitem__(key, value)
