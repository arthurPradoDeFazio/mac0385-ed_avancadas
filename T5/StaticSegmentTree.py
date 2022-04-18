import math
import LinkedList as ll

class Interval:
    def __init__(self, left, right, open_left=None, open_right=None):
        self.left = left
        self.right = right
        self.open_left = open_left
        self.open_right = open_right

    def __str__(self):
        if self.open_left:
            left_bracket = '('
        else:
            left_bracket = '['

        if self.open_right:
            right_bracket = ')'
        else:
            right_bracket = ']'

        return left_bracket + str(self.left) + ', ' + str(self.right) + right_bracket

    def get_left_endpoint(self):
        return self.left

    def get_right_endpoint(self):
        return self.right

    def is_empty(self):
        return (self.right < self.left
                or (self.left == self.right and (self.open_left or self.open_right)))

    def left_is_open(self):
        return self.open_left

    def right_is_open(self):
        return self.open_right

    def contains_as_member(self, point):
        if self.is_empty():
            return False

        is_greater_than_left = (self.left < point
                                or (not self.open_left and self.left == point))
        is_less_than_right = (point < self.right
                              or (not self.open_right and point == self.right))
        return is_greater_than_left and is_less_than_right

    def contains(self, interval):
        if interval.is_empty():
            return True
        if self.is_empty():
            return False

        left_is_possible = (self.left < interval.left
                            or (self.left == interval.left
                                and ((self.open_left and interval.open_left)
                                     or not self.open_left)))
        right_is_possible = (interval.right < self.right
                              or (interval.right == self.right
                                  and ((self.open_right and interval.open_right)
                                       or not self.open_right)))
        return left_is_possible and right_is_possible

    def is_contained_in(self, interval):
        return interval.contains(self)

    def intersects(self, interval):
        if self.is_empty() or interval.is_empty():
            return False

        intersection_left = max(self.left, interval.left)
        intersection_right = min(self.right, interval.right)
        mid_point = (intersection_left + intersection_right) / 2
        return (self.contains_as_member(mid_point)
                and interval.contains_as_member(mid_point))

class Node:
    def __init__(self):
        self.node_interval = None
        self.interval_list = ll.LinkedList()

    def set_node_interval(self, interval):
        self.node_interval = interval

    def add_interval(self, interval):
        self.interval_list.append(interval)

    def get_node_interval(self):
        return self.node_interval

    def get_interval_list(self):
        return self.interval_list

    def __str__(self):
        if self.interval_list.is_empty():
            return self.node_interval.__str__()

        interval_list_str = [interval.__str__() for interval in self.interval_list]
        interval_list_str[0] = '[' + interval_list_str[0]
        interval_list_str[-1] = interval_list_str[-1] + ']'
        return self.node_interval.__str__() + ", " + ', '.join(interval_list_str)

class AS:
    def __init__(self, interval_collection):
        endpoints = []
        for interval in interval_collection:
            endpoints.append(interval.get_left_endpoint())
            endpoints.append(interval.get_right_endpoint())
        endpoints.append(math.inf)
        endpoints.append(-math.inf)
        endpoints.sort()
        endpoints = AS.remove_duplicates(endpoints)

        elementary_intervals = AS.elementary_intervals(endpoints)

        self.segment_tree = [None] * (16 * len(interval_collection) + 4)
        self.build_tree(0, 0, len(elementary_intervals) - 1, elementary_intervals)
        self.build_interval_lists(interval_collection)

    @staticmethod
    def remove_duplicates(endpoints):
        fixed_list = []
        fixed_list.append(endpoints[0])
        for endpoint in endpoints[1:]:
            if endpoint != fixed_list[-1]:
                fixed_list.append(endpoint)
        return fixed_list

    @staticmethod
    def elementary_intervals(endpoints):
        elementary_intervals = []
        is_two_point_interval = True
        i = 0
        while i <= len(endpoints) - 2:
            if is_two_point_interval:
                elementary_intervals.append(Interval(endpoints[i], endpoints[i + 1],
                                                     True, True))
                i += 1
            else:
                elementary_intervals.append(Interval(endpoints[i], endpoints[i],
                                                     False, False))
            is_two_point_interval = not is_two_point_interval
        return elementary_intervals

    def build_tree(self, i, left, right, elementary_intervals):
        self.segment_tree[i] = Node()
        interval = Interval(elementary_intervals[left].get_left_endpoint(),
                            elementary_intervals[right].get_right_endpoint(),
                            elementary_intervals[left].left_is_open(),
                            elementary_intervals[right].right_is_open())
        self.segment_tree[i].set_node_interval(interval)

        if left == right:
            return

        mid = (left + right) // 2
        self.build_tree(2 * i + 1, left, mid, elementary_intervals)
        self.build_tree(2 * i + 2, mid + 1, right, elementary_intervals)

    def build_interval_lists(self, interval_collection):
        for interval in interval_collection:
            AS.place_interval(self.segment_tree, 0, interval)

    @staticmethod
    def place_interval(segment_tree, i, interval):
        if i >= len(segment_tree) or segment_tree[i] is None:
            return

        if interval.contains(segment_tree[i].get_node_interval()):
            segment_tree[i].add_interval(interval)
            return

        if interval.intersects(segment_tree[2 * i + 1].get_node_interval()):
            AS.place_interval(segment_tree, 2 * i + 1, interval)
        if interval.intersects(segment_tree[2 * i + 2].get_node_interval()):
            AS.place_interval(segment_tree, 2 * i + 2, interval)

    def segments(self, t):
        t_in_intervals = ll.LinkedList()
        self._segments(t, 0, t_in_intervals)
        return t_in_intervals

    def _segments(self, t, i, t_in_intervals):
        t_in_intervals.merge(self.segment_tree[i].get_interval_list())

        if (2 * i + 1 < len(self.segment_tree)
            and self.segment_tree[2 * i + 1] is not None
            and self.segment_tree[2 * i + 1].get_node_interval().contains_as_member(t)):
            self._segments(t, 2 * i + 1, t_in_intervals)
        elif (2 * i + 2 < len(self.segment_tree)
              and self.segment_tree[2 * i + 2] is not None
              and self.segment_tree[2 * i + 2].get_node_interval().contains_as_member(t)):
            self._segments(t, 2 * i + 2, t_in_intervals)

    def print(self):
        self._print("", 0, False)

    # A funão abaixo foi obtida em https://stackoverflow.com/questions/4965335/how-to-print-binary-tree-diagram-in-java/42449385#42449385
    def _print(self, prefix, i, is_left):
        if i < len(self.segment_tree) and self.segment_tree[i] is not None:
            print(prefix, end='')
            if is_left:
                print("|-- ", end='')
            else:
                print("\\-- ", end='')
            print(self.segment_tree[i])
            prefix += "|   " if is_left else "    "
            print(prefix)
            self._print(prefix, 2 * i + 1, True)
            self._print(prefix, 2 * i + 2, False)
