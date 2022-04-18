import StaticSegmentTree as sst
import LinkedList as ll

class ADS:
    def __init__(self):
        self.trees = [None] * 50 # 2 ^ 50 - 1 > 10 ^ 15
        self.interval_lists = [None] * 50

    def insert(self, interval):
        new_interval_list = ll.LinkedList()
        new_interval_list.append(interval)
        i = 0
        while self.trees[i] is not None:
            new_interval_list.merge(self.interval_lists[i])
            self.trees[i] = None
            self.interval_lists[i] = None
            i += 1

        self.interval_lists[i] = new_interval_list
        self.trees[i] = sst.AS(self.interval_lists[i])

    def segments(self, t):
        t_in_intervals = ll.LinkedList()
        for i in range(0, 50):
            if self.trees[i] is not None:
                t_in_intervals.merge(self.trees[i].segments(t))
        return t_in_intervals
