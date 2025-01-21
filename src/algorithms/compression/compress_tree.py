import numpy as np
from sklearn.utils.extmath import randomized_svd


class CompressTree:
    def __init__(self, matrix, t_min, t_max, s_min, s_max):
        self.matrix = matrix
        self.t_min = t_min
        self.t_max = t_max
        self.s_min = s_min
        self.s_max = s_max
        self.rank = 0
        self.U = None
        self.S = None
        self.V = None
        self.is_leaf = False
        self.zeros = False
        self.children = []


    def is_admissible(self, S, r, epsilon):
        return self.t_min + r == self.t_max or S[r] <= epsilon

    def set_leaf(self, U, S, V):
        self.is_leaf = True
        self.U = U
        self.S = S
        self.V = V

    def compress(self, r, epsilon):
        matrix_block = self.matrix[self.t_min:self.t_max, self.s_min:self.s_max]

        if np.allclose(matrix_block, np.zeros(matrix_block.shape)):
            self.rank = 0
            self.is_leaf = True
            self.zeros = True
            return self

        U, Sigma, V = randomized_svd(matrix_block,n_components=r+1, random_state=0)
        if self.is_admissible(Sigma, r, epsilon):
            self.rank = r
            self.set_leaf(U[:, :r], Sigma[:r], V[:r, :])
            return self
        else:
            self.children = []
            new_t_max = (self.t_min + self.t_max) // 2
            new_s_max = (self.s_min + self.s_max) // 2
            row_splits = [(self.t_min, new_t_max), (new_t_max, self.t_max)]
            col_splits = [(self.s_min, new_s_max), (new_s_max, self.s_max)]

            for t_min, t_max in row_splits:
                for s_min, s_max in col_splits:
                    child = CompressTree(self.matrix, t_min, t_max, s_min, s_max)
                    self.children.append(child)

            for child in self.children:
                child.compress(r, epsilon)

    def decompress(self):
        if self.is_leaf:
            if self.zeros:
                return np.zeros((self.t_max - self.t_min, self.s_max - self.s_min))
            return (self.U @ np.diag(self.S) @ self.V).reshape(self.t_max - self.t_min, self.s_max - self.s_min)


        nrows = self.t_max - self.t_min
        ncols = self.s_max - self.s_min
        decompressed_matrix = np.zeros((nrows, ncols))

        half_row = (self.t_max + self.t_min) // 2
        half_col = (self.s_max + self.s_min) // 2
        for i, child in enumerate(self.children):
            if i == 0:
                decompressed_matrix[:half_row - self.t_min, :half_col - self.s_min] = child.decompress()
            elif i == 1:
                decompressed_matrix[:half_row - self.t_min, half_col - self.s_min:] = child.decompress()
            elif i == 2:
                decompressed_matrix[half_row - self.t_min:, :half_col - self.s_min] = child.decompress()
            elif i == 3:
                decompressed_matrix[half_row - self.t_min:, half_col - self.s_min:] = child.decompress()

        return decompressed_matrix



def analyze(i, r=2, eps=1e-5):
    red_channel = i[:, :, 0]
    green_channel = i[:, :, 1]
    blue_channel = i[:, :, 2]

    def analyze_tree(node, channel_name):
        if node.is_leaf:
            print(f"[{channel_name}] Węzeł liściowy - zakres wierszy: {node.t_min}-{node.t_max}, zakres kolumn: {node.s_min}-{node.s_max}")
            print(f"[{channel_name}] Ranga węzła: {node.rank}")
            if node.rank > 0:
                print(f"[{channel_name}] Macierze SVD dostępne:\n  U: {node.U.shape}\n  S: {len(node.S)}\n  V: {node.V.shape}")
            else:
                print(f"[{channel_name}] Macierz jest pusta lub ma rangę 0")
        else:
            print(f"[{channel_name}] Węzeł wewnętrzny - zakres wierszy: {node.t_min}-{node.t_max}, zakres kolumn: {node.s_min}-{node.s_max}")
            for child in node.children:
                analyze_tree(child, channel_name)

    for channel, name in zip([red_channel, green_channel, blue_channel], ["Red", "Green", "Blue"]):
        tree = CompressTree(channel, 0, channel.shape[0], 0, channel.shape[1])
        tree.compress(r, eps)
        print(f"\nWyniki kompresji dla kanału {name}:")
        analyze_tree(tree, name)

np.random.seed(42)
i = np.random.randint(0, 256, (8, 8, 3))
# analyze(i)





def test_compression(matrix, r=2, eps=1e-5, tolerance=1e-3):
    matrix_tree = CompressTree(matrix, 0, matrix.shape[0], 0, matrix.shape[1])
    matrix_tree.compress(r, eps)

    decompressed_matrix = matrix_tree.decompress()

    print("Oryginalna macierz:")
    print(matrix)
    print("\nZdekompresowana macierz:")
    print(decompressed_matrix)

    difference = np.linalg.norm(matrix - decompressed_matrix)
    print("\nNorma różnicy między oryginalną a zdekompresowaną macierzą:", difference)

    if difference < tolerance:
        print("Zdekompresowana macierz jest bliska oryginalnej.")
    else:
        print("Zdekompresowana macierz różni się od oryginalnej.")


original_matrix = np.random.rand(4, 4)
# test_compression(original_matrix)



