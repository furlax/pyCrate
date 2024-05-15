from .actor import Actor


class Personnage(Actor):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)

    def __eq__(self, other: object) -> bool:
        return (self.x == other.x) and (self.y == other.y)

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)
