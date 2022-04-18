# Arthur Prado De Fazio
# NUSP: 9298614
# Esta implementação foi fortemente baseada no pseudo-código disponível
# na tese de mestrado de Yan Couto

import PersistentDeque as pd
import sys

def main():
    l = sys.stdin.readline()
    while len(l) > 0:
        if l.find('Deque') != -1:
            part1 = l[:l.find('Deque')]
            part2 = l[l.find('Deque'):]
            l = part1 + 'pd.' + part2
        print(">>>", l, end = '')
        exec(l)
        l = sys.stdin.readline()

def command_finder(l, parentheses_index):
    i = parentheses_index
    while i >= 0:
        if l[i] == '.':
            break
        i -= 1
    if i == -1:
        return l[0:parentheses_index]
    return l[i:parentheses_index]

main()
