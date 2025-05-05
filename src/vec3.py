from typing import Union
from math import sqrt


class Vector3d:
    def __init__(
        self, x: Union[int, float], y: Union[int, float], z: Union[int, float]
    ):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        return Vector3d(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vector3d(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other: Union[int, float]):
        if not (isinstance(other, int) or isinstance(other, float)):
            raise TypeError(
                f"unsupported operand type(s) for *: '{type(other).__name__}' "
                "and 'Vector3d'"
            )

        return Vector3d(self.x * other, self.y * other, self.z * other)

    def __rmul__(self, other: Union[int, float]):
        if not (isinstance(other, int) or isinstance(other, float)):
            raise TypeError(
                "unsupported operand type(s) for *: 'Vector3d' and "
                f"'{type(other).__name__}'"
            )

        return Vector3d(self.x * other, self.y * other, self.z * other)

    def __truediv__(self, other: Union[int, float]):
        if not (isinstance(other, int) or isinstance(other, float)):
            raise TypeError(
                "unsupported operand type(s) for /: 'Vector3d' and "
                f"'{type(other).__name__}'"
            )

        return Vector3d(self.x / other, self.y / other, self.z / other)

    def __repr__(self):
        return "Vector3d({}, {}, {})".format(self.x, self.y, self.z)

    def mag2(self) -> float:
        return self.x ** 2 + self.y ** 2 + self.z ** 2

    def mag(self) -> float:
        return sqrt(self.mag2())

    def norm(self):
        return self / self.mag()


if __name__ == "__main__":
    v = Vector3d(0, 0, 0)
    v = v + Vector3d(10, 0, 0)
    v = v * 3

    mag2 = v.mag2()

    # now, v equals Vector3d(30, 0, 0) and mag2 = 900
    print("v={} and mag2={}".format(v, mag2))
