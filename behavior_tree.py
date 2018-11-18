

class Node:
    def add_child(self, child):
        self.children.append(child)

    def add_children(self, *children):
        for o in children:
            self.children.append(o)


class BehaviorTree:
    SUCCESS, RUNNING, FAIL = 1, 0, -1

    def __init__(self, node_name):
        self.root = node_name

    def run(self):
        self.root.run()


class LeafNode(Node):
    def __init__(self, node_name, func_name):
        self.name = node_name
        self.func = func_name

    def run(self):
        return self.func()


class SequenceNode(Node):
    def __init__(self, node_name):
        self.name = node_name
        self.children = []
        self.prev_running_pos = 0

    def run(self):
        for o in range(self.prev_running_pos, len(self.children)):
            result = self.children[o].run()

            if result == BehaviorTree.RUNNING:
                self.prev_running_pos = o
                return BehaviorTree.RUNNING

            elif result == BehaviorTree.FAIL:
                self.prev_running_pos = 0
                return BehaviorTree.FAIL

        self.prev_running_pos = 0
        return BehaviorTree.SUCCESS


class SelectorNode(Node):

    def __init__(self, node_name):
        self.name = node_name
        self.children = []
        self.prev_running_pos = 0

    def run(self):
        for o in range(self.prev_running_pos, len(self.children)):

            result = self.children[o].run()

            if result == BehaviorTree.RUNNING:
                self.prev_running_pos = o
                return BehaviorTree.RUNNING

            elif result == BehaviorTree.SUCCESS:
                self.prev_running_pos = 0
                return BehaviorTree.SUCCESS

        self.prev_running_pos = 0
        return BehaviorTree.FAIL





