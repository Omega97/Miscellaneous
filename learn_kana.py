from omar_utils.data.files import File
from random import random
import pandas as pd
import msvcrt
from time import time
from copy import deepcopy


def keyboard_input(threshold=20):
    """ input from keyboard (without print, works only in an external console)
    :param threshold:
    :return: word (str), time taken
    """
    t = time()
    v = []
    while True:
        try:
            key = msvcrt.getch()
        except UnicodeDecodeError:
            key = b' '
        if key == b'\r' or key == b' ':     # end the input
            break
        elif key == b'\x08':     # Backspace deletes the last char
            if len(v) > 0:
                v = v[:-1]
        else:
            v += [key]

    t = min(time() - t, threshold)
    s = ''.join([str(i)[2:-1] for i in v])

    return s, t


def keyboard_input_():
    return input('>'), .1


def normalize(v):
    s = sum(v)
    if s == 0:
        return normalize([1 for _ in v])
    return [i/s for i in v]


def pick(v):
    v = normalize(v)
    r = random()
    for i in range(len(v)):
        r -= v[i]
        if r < 0:
            return i


def load_alphabet(url, path):
    """return alphabet as dicts of char: name"""
    f = File(url=url, path=path, separator=' ')
    f.save()
    chars = [i for i in f[0]]
    names = [i for i in f[1]]
    names = [i.replace('Katakana/', '').replace('Hiragana/', '').replace('.mp3', '') for i in names]
    names = [i if i != 'o_2' else 'o2' for i in names]
    return {chars[i]: names[i] for i in range(len(chars))}


def load_data(path):
    """ list of lists: [char, attempts, correct] """
    def empty_data(alpha):
        ind = [i for i in alpha]
        d = {'attempts': [0 for _ in ind],
             'correct': [0 for _ in ind],
             'time': [0. for _ in ind]}
        return pd.DataFrame(d, index=ind)
    try:
        f = File(path=path)
        return f()
    except FileNotFoundError:
        return empty_data(alpha=load_alphabet(URL, PATH))


def save_data(path, data):
    f = File()
    f.load_var(data)
    f.save(path=path)


def probability(tries, correct, t):
    """non-normalized probability"""
    score = (1 - correct / (1 + tries) + 1/(tries + 1)) ** 2 / 4
    if tries:
        score += t / tries / 4
    return  score


def update(problem, solution, data):
    out = deepcopy(data)

    print('\n\t ', problem)
    answer, t = keyboard_input()
    out.loc[problem, 'attempts'] += 1  # attempt
    out.loc[problem, 'time'] += t  # time

    if answer == solution and t is not None:
        out.loc[problem, 'correct'] += 1  # correct
    else:
        print('\t\t ', solution)    # wrong
        msvcrt.getch()     # todo ?
    return out


def quiz(alphabet):
    """quiz"""
    data = load_data(DATA)

    while True:
        chars = ''.join(i for i in alphabet)
        prob = [probability(data['attempts'][i], data['correct'][i], data['time'][i]) for i in chars]
        n = pick(prob)
        problem = chars[n]
        solution = alphabet[problem]
        data = update(problem, solution, data)
        save_data(DATA, data)


def test_1():
    pd.options.display.max_rows = 100
    print(File(DATA))
    input()


def show_times():
    data = File(DATA)()

    att = list(data['attempts'])
    t = list(data['time'])
    avg = [round(t[i]/att[i], 3) if att[i] > 0 else None for i in range(len(t))]

    pd.options.display.max_rows = 100
    df = pd.DataFrame(avg, index=data.index, columns=['AVG time'])
    print(df)

    s = sum([i if i else 0 for i in avg])
    n = sum([i is not None for i in avg])
    if n:
        print('AVG =', round(s / n, 3))
    input()


if __name__ == '__main__':

    URL = 'https://raw.githubusercontent.com/Ensiss/hiragana-katakana-zshprompt/master/files/hk_symbols.txt'
    PATH = 'hiragana_katakana.txt'
    DATA = 'kana_data.txt'

    # test_1()
    # show_times()

    Alphabet = load_alphabet(URL, PATH)

    print('Works on Windows console only! '
          'Write the romanji characters corresponding to the char that appears on screen. '
          'A timer takes track of your progress.'
          'Your accuracy is stored in a file.')
    input('\n' * 3 + '\t' * 2 + ' Learn Kana' + '\n' * 2)
    quiz(Alphabet)
