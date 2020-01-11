"""     Particle in a box

Simulates a quantum particle's distribution over time in a 1D box
The system is approximated by a lattice

Takes the initial wave function,  energy eigenvalues and eigenstates as input

Computes the coefficients of the series expansion of the initial wave function
Computes the time-dependent coefficients
Uses those to build the final time-dependent wave-function
"""
from __misc__.animated_plot import *
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from numpy import pi, exp, sin


i_ = np.complex(0, 1)


def animated_plot(x, y, dt=.01, yrange=None):

    def init():
        # only required for blitting to give a clean slate.
        line.set_ydata([np.nan] * len(x))
        return line,

    def animate(i):
        line.set_ydata(y(i*dt))
        return line,

    fig, ax = plt.subplots()
    if yrange:
        plt.ylim(bottom=yrange[0], top=yrange[1])

    line, = ax.plot(x, y(0))

    return animation.FuncAnimation(fig, animate, init_func=init, interval=2, blit=True, save_count=50)


class WaveFunction:
    """lattice of n points, values are given by fun"""
    def __init__(self, fun=None, y=None, x_range=None, length=1., n=None):
        if y is not None:
            n = len(y)
        if not n:
            n = 40
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

    def __len__(self):
        return len(self.y)

    def __mul__(self, other):
        if type(other) == WaveFunction:
            y = np.array([self.y[i] * other.y[i] for i in range(len(self))])
            return WaveFunction(y=y, length=self.length, n=self.n)
        if type(other) in [float, int, np.complex, np.complex128]:
            y = np.array([self.y[i] * other for i in range(len(self))])
            return WaveFunction(y=y, length=self.length, n=self.n)

    def __rmul__(self, other):
        return self * other

    def __add__(self, other):
        if type(other) == WaveFunction:
            y = np.array([self.y[i] + other.y[i] for i in range(len(self))])
            return WaveFunction(y=y, length=self.length, n=self.n)

    def square_module(self):
        v = [abs(i)**2 for i in self.y]
        return (sum(v) - (v[0] + v[-1]) / 2) * self.dx

    def distribution(self):
        return [abs(i)**2 for i in self.y]

    def integral(self):
        return (sum(self.y) - (self.y[0] + self.y[-1]) / 2) * self.dx

    def normalize(self):
        area = self.square_module()
        if area:
            for i in range(len(self)):
                self.y[i] /= area
        return self

    def real(self):
        return [i.real for i in self.y]

    def imag(self):
        return [i.imag for i in self.y]

    def __iter__(self):
        return iter(self.y)

    def __repr__(self):
        plt.plot(self.x, self.real())
        plt.plot(self.x, self.imag())
        plt.show()
        return ''


def gen_animation(psi_0, eigenvalues, eigenstates, dt=2**-16, order=10, N=100, m=1.):
    """
    :param psi_0: initial wave function
    :param eigenvalues: energy eigenvalues
    :param eigenstates: energy eigenvalues
    :param dt: time interval
    :param order: series expansion order
    :param N: number of points of the lattice
    :param m: particle mass
    :return:
    """

    xrange = (0, 1)  # initial and final coo of the lattice
    h_ = 1  # reduced planck's constant (1 for simplicity)
    a = xrange[1] - xrange[0]  # length of the lattice

    kw = {'x_range': xrange, 'length': a, 'n': N}

    # eigenvalues
    energy_n = {i: eigenvalues(i, a=a, m=m) for i in range(1, 1 + order)}

    # eigenstates
    Psi_n = {i: WaveFunction(fun=eigenstates(i, a=a), **kw).normalize() for i in range(1, 1 + order)}

    # initial state
    Psi = WaveFunction(fun=psi_0, **kw)

    # expanxion
    coeff = {i: (Psi_n[i] * Psi).integral() for i in range(1, 1 + order)}

    print('coefficients:')
    epsilon = 10 ** -5
    for i in coeff:
        print(f'{i:<8}', end='')
        if abs(coeff[i].real) <= epsilon and abs(coeff[i].imag) <= epsilon:
            print(' 0', end='')
        if abs(coeff[i].real) > epsilon:
            print(f' {coeff[i].real:+.4f}', end='')
        if abs(coeff[i].imag) > epsilon:
            print(f' {coeff[i].imag:+.4f} i', end='')
        print()

    def U(n, t):
        """time evolution operator"""
        return np.exp(- i_ * energy_n[n] * t / h_)

    def c_nt(n, t):
        """time-dependent version of coefficients()"""
        return coeff[n] * U(n, t)

    def psi(t):
        """imaginary part of the wave function"""
        out = WaveFunction(y=[0 for _ in range(N)], **kw)

        for i in range(1, 1 + order):
            out += Psi_n[i] * c_nt(i, t)

        return out

    def distribution(t):
        """square module of the wave function"""
        return psi(t).distribution()

    animated_plot(x=[i * a / (N-1) for i in range(N)], y=distribution,
                  dt=dt, yrange=[0, max(distribution(0))*1.6])
    plt.show()


if __name__ == '__main__':

    def initial_wave_function(x):
        """initial wave function (real)"""
        # return 1-abs(1/2-x)
        # return 1. if .25 < x < .5 else 0.
        # return np.exp(i_ * pi * 4) if .25 < x < .5 else 0.
        # return sin(x * pi) + sin(x * pi * 2)
        x0 = 0.5
        v = 10
        w = 1/15
        return exp(v * i_ * 2 * pi * x) * exp(-((x-x0)/w)**2)


    def E_n(n, a=1, m=1):
        """Energy of the n-th eigenstate"""
        return (n * pi / a) ** 2 / (2 * m)


    def psi_n(n, a=1):
        """n-th eigenstate"""

        def f_(x):
            return sin(n * pi * x / a)

        return f_

    gen_animation(initial_wave_function, E_n, psi_n, dt=2**-14, order=40, N=200)
