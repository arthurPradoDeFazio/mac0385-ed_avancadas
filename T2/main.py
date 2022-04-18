import ABB as abb
import sys

def main():
    l = sys.stdin.readline()
    while len(l) > 0:
        print(">>>", l, end = '')
        index_abb = l.find("BST")
        if index_abb != -1:
            exec(l[:index_abb] + "abb." + l[index_abb:])
        else:
            exec(l)
        l = sys.stdin.readline()

main()
