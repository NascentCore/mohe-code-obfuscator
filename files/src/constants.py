class Constant:
    # Enforce immutability by overriding __setattr__
    def __setattr__(self, name, value):
        raise AttributeError("Cannot modify constants.")


class StringLength(Constant):
    FILE_FILENAME: int = 255
    FILE_EXTENSION: int = 10
