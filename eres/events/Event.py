

class Event:

    def __init__(self, name):

        super().__init__()
        self.name = name

    def __str__(self):

        return self.name

    @property
    def name(self):

        return self._name

    @name.setter
    def name(self, name):

        if not isinstance(name, str):
            raise TypeError('name must be a str')

        self._name = name
