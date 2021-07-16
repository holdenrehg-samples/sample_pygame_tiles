from dataclasses import dataclass


@dataclass
class Point:
    x: int = 0
    y: int = 0

    def __hash__(self):
        return hash((self.x, self.y))

    @staticmethod
    def parse(self, data):
        if type(data) == Point:
            return data
        if len(data) == 2:
            return self(x=data[0], y=data[1])
