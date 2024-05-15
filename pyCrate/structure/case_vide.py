from .actor import Actor


class CaseVide(Actor):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)

    def __eq__(self, other: object) -> bool:
        return (self.x == other.x) and (self.y == other.y)

        # if isinstance(other, CaseVide):
        #     return (self.x == other.x) and (self.y == other.y)
        # return False

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)