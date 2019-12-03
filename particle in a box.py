"""
Particle in a box with Quantum Mechanics
This program computes the first energy levels of an n-dimensional box
"""

def recursive_iter(depth=1, *args):
    """
    iterate recursively (nested "for" loops)
    :param depth: number of nested loops
    :param args: args that go in range()
    :return:
    """
    if depth <= 1:
        for i in range(*args):
            yield (i,)
    else:
        for i in range(*args):
            for j in recursive_iter(depth - 1, *args):
                yield (i,) + j


def gen(n_max=7, dim=3):
    """:returns list of [n energy level, energy, degeneracy]"""
    d = {}  # store {energy: degeneracy}
    for indices in recursive_iter(dim, 1, n_max+1):
        # print(indices)
        n = sum([i**2 for i in indices])
        if n <= n_max ** 2 + 2:  # correct only up to 1**2 + 1**2 + n_max**2
            if n in d:
                d[n] += 1
            else:
                d.update({n:1})

    out = []    # store [n energy level, energy, degeneracy]
    for i in sorted(d.keys()):
        out += [[len(out)+1, i, d[i]]]

    return out


def pprint(n_max=7, dim=3):
    """pretty-print gen()"""
    print(f'\n{"n":>4} \t{"E":>4} \t{"deg":>4}\n')
    for i in gen(n_max=n_max, dim=dim):
        print(f'{i[0]:4} \t{i[1]:4} \t{i[2]:4}')


if __name__ == '__main__':
    pprint(n_max=7, dim=3)
