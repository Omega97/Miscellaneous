"""     Generalized groups

1) create an item
A = item('A')

2) define a multiplication rule
add_mul_rule('A', 'A', -1)

3) use the item to perform calculations!
1 / (1 + A)     #
"""
# item() creates mul rules
# todo sort elements
from copy import deepcopy
import numpy as np


class Group:

    Unit = '1'
    elements = set(Unit)    # record of all elements
    mul_table = {Unit + ' ' + Unit: 1}

    def __init__(self, items: dict):
        self.items = items  # deepcopy?
        self.index_ = 0
        self.update()
        self.clean()

    def __call__(self, name=None):
        if name is None:
            return self.items
        else:
            # return value of "name"
            return self()[name] if name in self() else 0

    def __repr__(self):
        """ultra-fancy print"""
        if len(self):
            s = ['+' if self.items[i] >= 0 else '-' for i in self.items]
            v = [self.items[i] for i in self.items]
            n = [str(round(abs(i), 15)) for i in v]
            n = [str(round(float(i))) if round(float(i)) == float(i) else i for i in n]
            n = [i + ' ' for i in n]
            for i in range(len(n)):
                f = float(n[i])
                if f == 1:
                    n[i] = ''
            e = [i for i in self.items]
            e = ['' if e[i] == '1' and abs(v[i]) != 1 else e[i] for i in range(len(e))]
            out = [s[i] + ' ' + n[i] + e[i] for i in range(len(n))]
            return ' '.join(out)
        else:
            return '0'

    def __len__(self):
        return len(self())

    def __iter__(self):
        self.index_ = 0
        return self

    def __next__(self):
        if self.index_ < len(self):
            name = self.keys()[self.index_]
            value = self()[name]
            self.index_ += 1
            return item(name=name, value=value)
        else:
            raise StopIteration

    def update(self):
        """record new elements & add mul rules (A * 1 = A, 1 * A = A)"""
        for i in self.items:
            if i not in Group.elements:
                Group.elements.update(i)
                add_mul_rule(Group.Unit, i, Group({i: 1}))

    def clean(self):
        """remove null elements"""
        new = {}
        items = self()
        for i in items:
            if items[i] != 0:
                new.update({i: items[i]})
        self.items = new

    def keys(self):
        return list(self().keys())

    def values(self):
        return [self()[i] for i in self()]

    def value(self):
        """value if there is only 1 element"""
        if len(self) == 1:
            return self.values()[0]

    def name(self):     # todo
        """name if there is only 1 element"""
        if len(self) == 1:
            return self.keys()[0]

    def __abs__(self):
        y = 0
        for i in self():
            y += self()[i] ** 2
        return y ** (1 / 2)

    def __add__(self, other):   # todo simplify
        if type(other) == Group:
            # join self.items + other.items
            items = deepcopy(self())
            for i in other():
                if i in items:
                    items.update({i: other()[i] + self()[i]})
                else:
                    items.update({i: other()[i]})
            self.clean()
            return Group(items)
        elif type(other) == int or type(other) == float:
            return self + item(name=Group.Unit, value=other)
        else:
            return self + item(name=other.__name__, value=other)    # todo ?

    def __radd__(self, other):
        return self + other

    def __neg__(self):
        items = self()
        return Group({i: -items[i] for i in items})

    def __rsub__(self, other):
        return -self + other

    def __sub__(self, other):
        return self + (-other)

    def __mul__(self, other):
        if type(other) == Group:
            out = Group({})

            for i in self:
                for j in deepcopy(other):
                    mul_tag = i.name() + ' ' + j.name()     # find def in mul_table
                    try:
                        result = Group.mul_table[mul_tag]   # find result   deepcopy?
                    except KeyError:
                        print('Missing product: ', mul_tag)    # todo
                    else:
                        out += result * i.value() * j.value()
            return out

        elif type(other) == int or type(other) == float:
            items = self()
            return Group({i: items[i] * other for i in items})

    def __rmul__(self, other):
        return self * other

    def __truediv__(self, other):   # todo check
        return self * (1 / other)

    def __rtruediv__(self, other):  # todo check Group.elements changes order
        if other == 1:
            # 1 / Group

            x = [item(i) for i in Group.elements]
            d = self

            v = [i * d for i in x]

            m = [[j(i) for j in v] for i in Group.elements]
            u = [1 if i == Group.Unit else 0 for i in Group.elements]

            m = np.array(m)     # todo check
            u = np.array(u).T

            try:
                sol = np.linalg.solve(m, u)
            except np.linalg.LinAlgError:
                return None     # Singular matrix
            else:
                return sum([sol[i] * x[i] for i in range(len(sol))])

        else:
            return other * (1 / self)

    def __eq__(self, other):    # todo
        if type(other) == Group:
            return self() == other()
        else:
            return False

    def __pow__(self, power, modulo=None):    # todo check
        if power >= 0:
            out = 1
            for i in range(power):
                out *= self
            return out
        else:
            out = 1
            for i in range(-power):
                out /= self
            return out


def add_mul_rule(item1: str, item2: str, result):
    """add multiplication rule (by default items commute)"""
    new = item1 + ' ' + item2
    Group.mul_table.update({new: result})
    # try to add commuted to mul_table
    commuted = item2 + ' ' + item1
    if commuted not in Group.mul_table:
        Group.mul_table.update({commuted: result})


def item(name: str, value=1.) -> Group:
    """creates a group with a single item"""
    name_ = name.replace(' ', '')
    return Group({name_: value})


if __name__ == '__main__':

    from math import factorial as fact

    A = item('A')
    add_mul_rule('A', 'A', -1)
    G = 1 + A

    assert G + 1 == Group({'A': 1, '1': 2})
    assert G + 1 == Group({'A': 1, '1': 2})
    assert G * G == Group({'A': 2})
    assert G * G * G == Group({'1': -2, 'A': 2})
    assert G * 2 == Group({'1': 2, 'A': 2})
    assert Group({'1': 2}) * Group({'1': 3}) == Group({'1': 6})

    def sin(x, prec=10):
        return sum([(-1)**i * x ** (2 * i + 1) / fact(2 * i + 1) for i in range(prec)])

    def cos(x, prec=10):
        return sum([(-1)**i * x ** (2 * i) / fact(2 * i) for i in range(prec)])

    assert cos(A) ** 2 + sin(A) ** 2

    # print(2 + 2 * A)
    # print(1 + 1.2 * A)
    # print(0 + A)
    # print(-1 + A)

    # print((5 + 2 * A)/(3 + 4 * A))

    # A = item('A')
    # B = item('B')
    # add_mul_rule('A', 'A', B)
    # add_mul_rule('A', 'B', -1)
    # add_mul_rule('B', 'B', -A)
    #
    # print(A / (A + B + 1))
