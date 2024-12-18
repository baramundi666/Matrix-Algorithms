import numpy as np
import matplotlib.pyplot as plt


def reconstruct_block(node):
    if node.is_leaf:
        if node.zeros:
            return np.zeros((node.t_max - node.t_min, node.s_max - node.s_min))
        else:
            return node.U @ np.diag(node.S) @ node.V
    else:
        raise ValueError("Node is not a leaf.")


class CompressTreeBitmapVisualizer:
    def __init__(self, compress_tree):
        self.compress_tree = compress_tree

    def reconstruct_matrix(self):
        matrix = np.zeros_like(self.compress_tree.matrix)
        stack = [self.compress_tree]

        while stack:
            node = stack.pop()
            if node.is_leaf:
                block = reconstruct_block(node)
                matrix[node.t_min:node.t_max, node.s_min:node.s_max] = block
            else:
                stack.extend(node.children)

        return matrix

    def draw_bitmap(self):
        matrix = self.reconstruct_matrix()
        return matrix


class CompressTreeStructureVisualizer:
    def __init__(self, compress_tree):
        self.compress_tree = compress_tree

    def visualize_tree_structure(self):
        rows, cols = self.compress_tree.matrix.shape
        structure = np.ones((rows, cols))

        def mark_blocks(node):
            if node.is_leaf:
                if not node.zeros:
                    structure[node.t_min:node.t_min + node.rank,
                              node.s_min:node.s_max] = 0

                    structure[node.t_min :node.t_max,
                              node.s_min:node.s_min + node.rank] = 0
            else:

                for child in node.children:
                    mark_blocks(child)

        mark_blocks(self.compress_tree)

        plt.figure(figsize=(10, 10))
        plt.imshow(structure, cmap="gray", interpolation="nearest")
        plt.title("Tree Structure Visualization (U, S, V blocks)")
        plt.axis("off")
        plt.show()

