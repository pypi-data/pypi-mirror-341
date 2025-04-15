from tketool.ml.modelbase import Model_Base


class TreeNode:
    def __init__(self, key=None, value=None, base_node=None):
        self.key = key
        self.value = value
        self._children = {}
        self._base_node = base_node
        self._root_node = self if base_node is None else base_node.root_node

    @property
    def Value(self):
        return self.value

    @Value.setter
    def Value(self, value):
        self.value = value

    @property
    def children(self):
        return self._children

    @property
    def base_node(self):
        return self._base_node

    @property
    def root_node(self):
        return self._root_node

    @property
    def distance_to_root(self):
        """获取当前节点到根节点的距离"""
        distance = 0
        node = self
        while node.base_node is not None:
            distance += 1
            node = node.base_node
        return distance

    def add_child(self, key, value):
        child_node = TreeNode(key, value, self)
        self._children[key] = child_node
        return child_node

    def path_to_root(self):
        path = []
        node = self
        while node is not None:
            path.append(node)
            node = node.base_node
        return path[::-1]  # Reverse the path to start from the root

    def iter_depth(self):
        yield self
        for child in self._children.values():
            yield from child.iter_depth()

    def iter_extensive(self):
        queue = [self]
        while queue:
            node = queue.pop(0)
            yield node
            queue.extend(node._children.values())

    def __setitem__(self, key, value):
        """Allow setting a child node using dictionary-like syntax."""
        self.add_child(key, value)

    def __contains__(self, key):
        """Check if a child node with the given key exists."""
        return key in self._children

    def __getitem__(self, key):
        """通过键获取下级节点"""
        return self._children.get(key)



