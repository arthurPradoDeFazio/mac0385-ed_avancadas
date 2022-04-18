import DynamicForest as df
import sys

def main():
    l = sys.stdin.readline()
    while len(l) > 0:
        print(">>>", l, end='')
        index_stack = l.find("DynamicForest")
        if index_stack != -1:
            exec(l[:index_stack] + 'df.' + l[index_stack:])
        else:
            exec(l)
        l = sys.stdin.readline()

main()
