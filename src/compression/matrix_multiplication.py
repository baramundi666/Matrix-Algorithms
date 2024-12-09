import numpy as np
from src.calculator import Calculator
from src.compression.compress_tree import CompressTree


class MatrixMultiplication:
    @staticmethod
    def matrix_vector_mult(v, X):
        if not v.children:
            if v.rank == 0:
                return np.zeros(X.shape)
            return v.U @ np.diag(v.S) @ (v.V @ X)

        rows = X.shape[0]
        X1 = X[:rows // 2, :]
        X2 = X[rows // 2:, :]
        Y11 = MatrixMultiplication.matrix_vector_mult(v.children[0], X1)
        Y12 = MatrixMultiplication.matrix_vector_mult(v.children[1], X2)
        Y21 = MatrixMultiplication.matrix_vector_mult(v.children[2], X1)
        Y22 = MatrixMultiplication.matrix_vector_mult(v.children[3], X2)

        return np.vstack((Y11 + Y12, Y21 + Y22))

    @staticmethod
    def rSVDofCompressed(matrix, epsilon=1e-4):
        U, Sigma, VT = np.linalg.svd(matrix, full_matrices=False)
        rank = sum(Sigma >= epsilon)
        U_reduced = U[:, :rank]
        S_reduced = Sigma[:rank]
        V_reduced = VT[:rank, :]
        node = CompressTree(np.zeros(matrix.shape), 0, matrix.shape[0], 0, matrix.shape[1])
        node.set_leaf(U_reduced, S_reduced, V_reduced)
        return node

    @staticmethod
    def svd_and_compress(v, w):
        matrix_v = v.U @ np.diag(v.S) @ v.V.T
        matrix_w = w.U @ np.diag(w.S) @ w.V.T
        added_matrix = matrix_v + matrix_w
        return MatrixMultiplication.rSVDofCompressed(added_matrix)

    @staticmethod
    def matrix_matrix_add(v, w):
        if not v.children and not w.children and v.rank == 0 and w.rank == 0:
            return CompressTree(np.zeros((v.t_max - v.t_min, v.s_max - v.s_min)), v.t_min, v.t_max, v.s_min, v.s_max)
        if not v.children and not w.children and v.rank != 0 and w.rank != 0:
            return MatrixMultiplication.svd_and_compress(v, w)
        if v.children and w.children:
            node = CompressTree(np.zeros((v.t_max - v.t_min, v.s_max - v.s_min)), v.t_min, v.t_max, v.s_min, v.s_max)
            node.children = [MatrixMultiplication.matrix_matrix_add(vc, wc) for vc, wc in zip(v.children, w.children)]
            return node
        if not v.children and w.children:
            v_blocks = MatrixMultiplication.split(v)
            node = CompressTree(np.zeros((v.t_max - v.t_min, v.s_max - v.s_min)), v.t_min, v.t_max, v.s_min, v.s_max)
            node.children = [MatrixMultiplication.matrix_matrix_add(vb, wc) for vb, wc in zip(v_blocks, w.children)]
            return node
        if v.children and not w.children:
            return MatrixMultiplication.matrix_matrix_add(w, v)

    @staticmethod
    def mult_rec(v, w):
        node = CompressTree(np.zeros((v.t_max - v.t_min, w.s_max - w.s_min)), v.t_min, v.t_max, w.s_min, w.s_max)
        node.children = [
            MatrixMultiplication.matrix_matrix_add(
                MatrixMultiplication.matrix_matrix_mult(v.children[0], w.children[0]),
                MatrixMultiplication.matrix_matrix_mult(v.children[1], w.children[2])),
            MatrixMultiplication.matrix_matrix_add(
                MatrixMultiplication.matrix_matrix_mult(v.children[0], w.children[1]),
                MatrixMultiplication.matrix_matrix_mult(v.children[1], w.children[3])),
            MatrixMultiplication.matrix_matrix_add(
                MatrixMultiplication.matrix_matrix_mult(v.children[2], w.children[0]),
                MatrixMultiplication.matrix_matrix_mult(v.children[3], w.children[2])),
            MatrixMultiplication.matrix_matrix_add(
                MatrixMultiplication.matrix_matrix_mult(v.children[2], w.children[1]),
                MatrixMultiplication.matrix_matrix_mult(v.children[3], w.children[3]))]
        return node

    @staticmethod
    def matrix_matrix_mult(v, w):
        if not v.children and not w.children:
            if v.rank == 0 and w.rank == 0:
                return CompressTree(np.zeros((v.t_max - v.t_min, w.s_max - w.s_min)), v.t_min, v.t_max, w.s_min, w.s_max,)
            else:
                if v.rank != 0 and w.rank != 0:
                    new_U, new_Sigma, new_V = v.U, v.S * w.S, (v.V @ w.U) @ w.V
                    node = CompressTree(np.zeros((v.t_max - v.t_min, w.s_max - w.s_min)), v.t_min, v.t_max, w.s_min, w.s_max)
                    node.set_leaf(new_U, new_Sigma, new_V)
                    return node
        if v.children and w.children:
            return MatrixMultiplication.mult_rec(v, w)
        v = MatrixMultiplication.ensure_children(v)
        w = MatrixMultiplication.ensure_children(w)
        return MatrixMultiplication.mult_rec(w, v)

    @staticmethod
    def ensure_children(node):
        if not node.children:
            return MatrixMultiplication.split(node)
        return node

    @staticmethod
    def split(v):
        matrix = v.U @ np.diag(v.S) @ v.V.T
        t_mid = (v.t_min + v.t_max) // 2
        s_mid = (v.s_min + v.s_max) // 2
        A11, A12, A21, A22 = Calculator().split_into_block_matrices(matrix)
        node = CompressTree(np.zeros(matrix.shape), v.t_min, v.t_max, v.s_min, v.s_max)
        node.children = [CompressTree(A11, v.t_min, t_mid, v.s_min, s_mid),
                            CompressTree(A12, v.t_min, t_mid, s_mid, v.s_max),
                            CompressTree(A21, t_mid, v.t_max, v.s_min, s_mid),
                            CompressTree(A22, t_mid, v.t_max, s_mid, v.s_max),]
        return node


