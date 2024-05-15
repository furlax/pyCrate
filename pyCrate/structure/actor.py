class Actor:
    def __init__(self, x: int, y: int):
        self.x: int = x
        self.y: int = y

    def get_x(self) -> int:
        return self.x

    def get_y(self) -> int:
        return self.y
