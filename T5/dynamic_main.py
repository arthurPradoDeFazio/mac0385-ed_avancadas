import StaticSegmentTree as sst
import DynamicSegmentTree as dst
import sys

def main():
    l = sys.stdin.readline()
    while len(l) > 0:
        print(">>>", l, end='')
        index_stack = l.find("ADS")
        if index_stack != -1:
            exec(l[:index_stack] + 'dst.' + l[index_stack:])
        else:
            exec(l)
        l = sys.stdin.readline()

main()
