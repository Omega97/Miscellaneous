import numpy as np
from omar_utils import *
import matplotlib.pyplot as plt
from math import pi


# ----------------------------------------------------------------


# E = eV
# L = nm
# T = ns

m_e = 9.109 * 10 ** -31    # electron mass eV/c^2
c = 2.998 * 10 ** 8  # speed of light nm/ns
h = 6.626 * 10 ** -34    # Panck's constant ns eV
h_ = h / (2 * pi)   # reduced Panck's constant ns eV


J__eV = 6.242 * 10 ** 18
# m = 9.109383632 * 10**-31


# ----------------------------------------------------------------


def solve_H(V_, interval, N=10):

    length_ = interval[1] - interval[0]
    delta = length_ / (N + 1)
    lam = h_**2 / (2 * m_e * delta**2)

    # hamiltonian operator
    H = np.zeros((N, N))
    for i in range(N):
        x = interval[0] + delta * (i + 1)   # todo test
        H[i, i] = 2 + V_(x) / lam
    for i in range(N-1):
        H[i, i + 1] = -1
        H[i + 1, i] = -1


    # eigenvalues, eigenvectors
    e_val, e_vec = np.linalg.eig(H)
    e_val.sort()
    e_val = [i * lam for i in e_val]

    # print(lam)
    # k = (h_/length)**2 / (2 + m_e)
    # print(k)

    return e_val, e_vec


def wavelength_of_energy(E):
    return h * c / E


def plot_eigen_vals(v, colors='b', **kwargs):
    plt.title('Energy levels [eV]')
    plt.xticks([])
    plt.hlines(np.array(v) * J__eV, 0, 1, colors=colors,**kwargs)
    plt.show()


def plot_eigen_states(v, first_n=3, **kwargs):
    for f in gen_first_n_items(v, n=first_n):
        plt.plot(f, **kwargs)
        plt.show()


def calc_wavelengths(eigen_val):
    wavelengths = []
    for i in eigen_val:
        for j in eigen_val:
            nrg = abs(i - j)
            if nrg > 0:
                wl = wavelength_of_energy(nrg) * 10 ** 9
                wl = round(wl, 5)
                wavelengths.append(wl)

    wavelengths = list(set(wavelengths))    # remove duplicates
    wavelengths.sort()

    print('\nWavelengths [nm]\n')
    for i in wavelengths:
        print(f'{i:.1f}')

    return wavelengths


def plot_wavelengths(wl, x_max=None, linewidth=1., **kwargs):
    plt.axes().set_facecolor("black")
    plt.title('Emission spectrum [nm]')
    plt.yticks([])
    plt.vlines(wl, 0, 1, colors=[color_of_wavelength(i) for i in wl], linewidth=linewidth, **kwargs)
    if x_max:
        plt.xlim(0, x_max)
    else:
        plt.xlim(0, plt.xlim()[1])

    plt.show()


def color_of_wavelength(wl, gamma=0.8):
    red = 750
    violet = 380
    if wl <= violet:    # UV
        A = (wl / violet) / 2
    elif wl >= red:     # Infra-red
        A = 2/3
    else:
        A = 1.
    if wl < violet:
        wl = violet
    if wl > red:
        wl = red
    if violet <= wl <= 440:
        attenuation = 0.3 + 0.7 * (wl - violet) / (440 - 380)
        R = ((-(wl - 440) / (440 - violet)) * attenuation) ** gamma
        G = 0.0
        B = (1.0 * attenuation) ** gamma
    elif 440 <= wl <= 490:
        R = 0.0
        G = ((wl - 440) / (490 - 440)) ** gamma
        B = 1.0
    elif 490 <= wl <= 510:
        R = 0.0
        G = 1.0
        B = (-(wl - 510) / (510 - 490)) ** gamma
    elif 510 <= wl <= 580:
        R = ((wl - 510) / (580 - 510)) ** gamma
        G = 1.0
        B = 0.0
    elif 580 <= wl <= 645:
        R = 1.0
        G = (-(wl - 645) / (645 - 580)) ** gamma
        B = 0.0
    elif 645 <= wl <= red:
        attenuation = 0.3 + 0.7 * (red - wl) / (red - 645)
        R = (1.0 * attenuation) ** gamma
        G = 0.0
        B = 0.0
    else:
        R = 0.0
        G = 0.0
        B = 0.0
    return R, G, B, A


# ----------------------------------------------------------------

def infinite_well(length=2*10**-9):

    def V(_):
        return 0

    eig_val, eig_vec = solve_H(V, [0, length], N=50)
    wl = calc_wavelengths(eig_val)
    # plot_eigen_vals(eig_val)
    # plot_eigen_states(eig_vec)
    plot_wavelengths(wl)



def finite_well(length=2*10**-9):

    def V(x):
        return -.1 if abs(x) < length / 4 else 0

    eig_val, eig_vec = solve_H(V, [-length, +length], N=50)
    wave_len = calc_wavelengths(eig_val)
    plot_wavelengths(wave_len)



if __name__ == '__main__':
    finite_well()
