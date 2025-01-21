import numpy as np
from src.algorithms.compression.compress_tree import CompressTree

def matrix_vector_mult(v, X):
    if not v.children:
        if v.rank == 0:
            return np.zeros(X.shape)
        return v.U @ np.diag(v.S) @ (v.V @ X)
    rows = X.shape[0]
    X1 = X[:rows // 2, :]
    X2 = X[rows // 2:, :]
    Y11 = matrix_vector_mult(v.children[0], X1)
    Y12 = matrix_vector_mult(v.children[1], X2)
    Y21 = matrix_vector_mult(v.children[2], X1)
    Y22 = matrix_vector_mult(v.children[3], X2)

    return np.vstack((Y11 + Y12, Y21 + Y22))

def rSVDofCompressed(v, w, epsilon=1e-7):
    n, k = v.U.shape[0], v.V.shape[1]
    original_rank = v.rank
    U_stacked = np.hstack((v.U, w.U))
    V_stacked = np.vstack((v.V, w.V))
    S_stacked = np.concatenate((v.S, w.S))
    node = CompressTree(None, 0, n, 0, k)
    node.set_leaf(U_stacked, S_stacked, V_stacked)
    node.matrix = node.decompress()
    node.compress(original_rank, epsilon)
    return node

def add_rec(v, w):
    node = CompressTree(None, v.t_min, v.t_max, v.s_min, v.s_max)
    node.rank = v.rank
    node.children = [matrix_matrix_add(vc, wc) for vc, wc in zip(v.children, w.children)]
    return node

def matrix_matrix_add(v, w):
    if v.zeros:
        return w
    if w.zeros:
        return v
    if not v.children and not w.children and v.rank == 0 and w.rank == 0:
        node = CompressTree(None, v.t_min, v.t_max, v.s_min, v.s_max)
        node.zeros = True
        return node
    if not v.children and not w.children and v.rank != 0 and w.rank != 0:
        return rSVDofCompressed(v, w)
    if v.children and w.children:
        return add_rec(v, w)
    if not v.children:
        return matrix_matrix_add(split_compressed_matrix(v), w)
    if not w.children:
        return matrix_matrix_add(v, split_compressed_matrix(w))
    return add_rec(v, w)

def mult_rec(v, w):
    node = CompressTree(None, v.t_min, v.t_max, w.s_min, w.s_max)
    node.rank = v.rank
    node.children = [
        matrix_matrix_add(
            matrix_matrix_mult(v.children[0], w.children[0]),
            matrix_matrix_mult(v.children[1], w.children[2])),
        matrix_matrix_add(
            matrix_matrix_mult(v.children[0], w.children[1]),
            matrix_matrix_mult(v.children[1], w.children[3])),
        matrix_matrix_add(
            matrix_matrix_mult(v.children[2], w.children[0]),
            matrix_matrix_mult(v.children[3], w.children[2])),
        matrix_matrix_add(
            matrix_matrix_mult(v.children[2], w.children[1]),
            matrix_matrix_mult(v.children[3], w.children[3]))]
    return node

def matrix_matrix_mult(v, w):
    if v.zeros or w.zeros:
        node = CompressTree(None, v.t_min, v.t_max, w.s_min, w.s_max)
        node.zeros = True
        return node
    if not v.children and not w.children:
        if v.rank == 0 or w.rank == 0:
            node = CompressTree(None, v.t_min, v.t_max, w.s_min, w.s_max)
            node.zeros = True
            return node
        new_U = v.U
        new_S = v.S * w.S
        new_V = (v.V @ w.U) @ w.V
        node = CompressTree(None, v.t_min, v.t_max, w.s_min, w.s_max)
        node.set_leaf(new_U, new_S, new_V)
        node.rank = v.rank
        return node
    if v.children and w.children:
        return mult_rec(v, w)
    if not v.children:
        return matrix_matrix_mult(split_compressed_matrix(v), w)
    if not w.children:
        return matrix_matrix_mult(v, split_compressed_matrix(w))
    return matrix_matrix_mult(w, v)

def split_compressed_matrix(v) -> CompressTree:
    if v.rank == 1:
        S_1 = v.S
        S_2 = v.S
    else:
        S_1 = v.S[:v.S.shape[0] // 2]
        S_2 = v.S[v.S.shape[0] // 2:]
    U_upper = v.U[:v.U.shape[0] // 2, :]
    U_lower = v.U[v.U.shape[0] // 2:, :]
    V_left = v.V[:, :v.V.shape[1] // 2]
    V_right = v.V[:, v.V.shape[1] // 2:]
    node = CompressTree(None, v.t_min, v.t_max, v.s_min, v.s_max)
    node.rank = v.rank
    node.children = [None for _ in range(4)]
    node.children[0] = CompressTree(None, v.t_min, v.t_min + U_upper.shape[0], v.s_min,
                        v.s_min + V_left.shape[1])
    node.children[0].rank = v.rank
    node.children[0].set_leaf(U_upper, S_1, V_left)
    node.children[1] = CompressTree(None, v.t_min, v.t_min + U_upper.shape[0],
                        v.s_min + V_left.shape[1], v.s_max)
    node.children[1].rank = v.rank
    node.children[1].set_leaf(U_upper, S_2, V_right)
    node.children[2] = CompressTree(None, v.t_min + U_upper.shape[0], v.t_max, v.s_min,
                        v.s_min + V_left.shape[1])
    node.children[2].rank = v.rank
    node.children[2].set_leaf(U_lower, S_1, V_left)
    node.children[3] = CompressTree(None, v.t_min + U_upper.shape[0], v.t_max,
                        v.s_min + V_left.shape[1], v.s_max)
    node.children[3].rank = v.rank
    node.children[3].set_leaf(U_lower, S_2, V_right)
    return node


