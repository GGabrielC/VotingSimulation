class DefaultedDict(dict):
    def __init__(self, defaultValue=None, **kwargs):
        super().__init__(**kwargs)
        self.defaultValue = defaultValue

    def __getitem__(self, key):
        if key in self.keys():
            return super().__getitem__(key)
        super().__setitem__(key, self.defaultValue)
        return super().__getitem__(key)