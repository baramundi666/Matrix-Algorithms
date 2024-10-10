class BaseAlgorithm:
    def __init__(self):
        self.name = self.__class__.__name__

    def run(self, **kwargs):
        pass

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name
