from math import *
from __misc__.animated_plot import *


class Bar:
    """lattice of n points, values are given by fun"""
    def __init__(self, fun=None, y=None, x_range=None, length=1., n=40):
        self.length = length
        self.x_range = x_range
        if self.x_range:
            self.length = x_range[1] - x_range[0]
        self.n = n
        self.dx = self.length / (self.n-1)
        self.x = np.array([i * self.dx for i in range(n)])

        if y is None:
            self.y = np.ones(len(self.x))
        else:
            self.y = y
        if fun is not None:
            self.y = np.array([fun(i) for i in self.x])
        self.normalize()

    def __len__(self):
        return len(self.y)

    def __mul__(self, other):
        if type(other) == Bar:
            y = np.array([self.y[i] * other.y[i] for i in range(len(self))])
            return Bar(y=y, length=self.length, n=self.n)

    def square_module(self):
        v = [i**2 for i in self.y]
        return (sum(v) - (v[0] + v[-1]) / 2) * self.dx

    def integral(self):
        return (sum(self.y) - (self.y[0] + self.y[-1]) / 2) * self.dx

    def normalize(self):
        area = self.square_module()
        for i in range(len(self)):
            self.y[i] /= area

    def __iter__(self):
        return iter(self.y)

    def plot(self):
        plt.plot(self.x, self.y)
        plt.show()


def coefficients(f):
    """compute the coefficients that allow tou to represent f as a linear combination of eigenstates"""
    psi = Bar(fun=f, x_range=xrange, n=N)

    def c_n(i):
        f_n = Bar(fun=psi_n(i), x_range=xrange, n=N)
        return (f_n * psi).integral()

    return [0] + [c_n(i) for i in range(1, 1 + prec)]


def E_n(n):
    """Energy of the n-th eigenstate"""
    return (n * pi / a) ** 2 / (2 * m)


def psi_n(n):
    """n-th eigenstate"""
    def f(x):
        return (2/a)**.5 * sin(n * pi * x / a)
    return f


def U(n):
    """time evolution operator
    returns real, imaginary part"""
    def f(t):
        return cos(E_n(n) * t / h_), -sin(E_n(n) * t / h_)
    return f


def c_nt(n, t):
    """time-dependent version of coefficients()"""
    u = U(n)(t)
    return c_[n] * u[0], c_[n] * u[1]


def psi_r(x, t):
    """real part of the wave function"""
    return sum(psi_n(i)(x) * c_nt(i, t)[0] for i in range(1, 1 + prec))


def psi_im(x, t):
    """imaginary part of the wave function"""
    return sum(psi_n(i)(x) * c_nt(i, t)[1] for i in range(1, 1 + prec))


def distribution():
    """square module of the wave function"""
    def f(x, t):
        return psi_r(x, t) ** 2 + psi_im(x, t) ** 2
    return f


if __name__ == '__main__':

    m = 1   # particle mass
    h_ = 1  # reduced planck's constant (1 for simplicity)
    xrange = (0, 1)    # initial and final coo of the lattice
    a = xrange[1] - xrange[0]     # length of the lattice
    N = 100     # number of points of the lattice
    prec = 50   # number of degrees of the series expansion


    def f_(x):
        """initial wave function (real)"""
        # return 1-abs(1/2-x)
        return 1. if .25 < x < .5 else 0.


    c_ = coefficients(f_)

    for I in c_:
        print(round(I, 4))

    animated_plot(distribution(), xrange=xrange, dx=1/N, dt=2**-16, yrange=[0, 2])
    plt.show()

    # todo save animation
    # save_animation(ani)
    # ani.save("movie.html")
