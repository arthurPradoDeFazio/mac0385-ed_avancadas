import SuffixArray as sa
import sys

def main():
    l = sys.stdin.readline()
    while len(l) > 0:
        print(">>>", l)
        index_stack = l.find("VS")
        if index_stack != -1:
            exec(l[:index_stack] + 'sa.' + l[index_stack:])
        else:
            exec(l)
        l = sys.stdin.readline()

main()
