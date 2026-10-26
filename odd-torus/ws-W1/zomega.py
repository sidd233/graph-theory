"""Exact arithmetic in Q(omega), omega = e^(2 pi i/3), omega^2 = -1 - omega.
An element is a + b*omega with a, b Fractions."""
from fractions import Fraction as F


class Z:
    __slots__ = ("a", "b")

    def __init__(self, a=0, b=0):
        self.a = F(a)
        self.b = F(b)

    def __add__(self, o):
        o = _c(o)
        return Z(self.a + o.a, self.b + o.b)

    __radd__ = __add__

    def __sub__(self, o):
        o = _c(o)
        return Z(self.a - o.a, self.b - o.b)

    def __rsub__(self, o):
        return _c(o) - self

    def __neg__(self):
        return Z(-self.a, -self.b)

    def __mul__(self, o):
        o = _c(o)
        # (a + b w)(c + d w) = ac + (ad + bc) w + bd w^2,  w^2 = -1 - w
        a, b, c, d = self.a, self.b, o.a, o.b
        return Z(a * c - b * d, a * d + b * c - b * d)

    __rmul__ = __mul__

    def conj(self):
        # complex conjugation: w -> w^2 = -1 - w
        return Z(self.a - self.b, -self.b)

    def norm(self):
        # |z|^2 = a^2 - ab + b^2 (rational)
        return self.a * self.a - self.a * self.b + self.b * self.b

    def inv(self):
        n = self.norm()
        if n == 0:
            raise ZeroDivisionError
        c = self.conj()
        return Z(c.a / n, c.b / n)

    def __truediv__(self, o):
        return self * _c(o).inv()

    def __eq__(self, o):
        o = _c(o)
        return self.a == o.a and self.b == o.b

    def __hash__(self):
        return hash((self.a, self.b))

    def iszero(self):
        return self.a == 0 and self.b == 0

    def is_rational(self):
        return self.b == 0

    def __pow__(self, n):
        r = Z(1)
        x = self
        if n < 0:
            x = x.inv()
            n = -n
        while n:
            if n & 1:
                r = r * x
            x = x * x
            n >>= 1
        return r

    def __repr__(self):
        if self.b == 0:
            return f"{self.a}"
        return f"({self.a} + {self.b}w)"


def _c(o):
    return o if isinstance(o, Z) else Z(o)


W = [Z(1, 0), Z(0, 1), Z(-1, -1)]  # omega^0, omega^1, omega^2


def wpow(j):
    return W[j % 3]


ISQ3 = Z(1, 2)  # i*sqrt(3) = omega - omega^2 = 1 + 2 omega

if __name__ == "__main__":
    assert ISQ3 * ISQ3 == Z(-3)
    assert W[1] * W[1] == W[2] and W[1] * W[2] == W[0]
    assert (W[1] - W[2]) == ISQ3
    x = Z(F(2, 3), -5)
    assert x * x.inv() == Z(1)
    print("zomega self-test ok")
