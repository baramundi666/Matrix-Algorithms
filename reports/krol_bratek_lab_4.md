# Algorytmy Macierzowe

## Sprawozdanie nr 4

## 08.01.2025

## Mateusz Król, Natalia Bratek
## gr. 3

## Spis treści
1. [Polecenie](#polecenie)
2. [Generowanie_macierzy](#matrix)
	1. [Opis algorytmu](#matrix_opis)
    2. [Pseudokod](#matrix_pseudo)
    3. [Fragment kodu](#matrix_fragment)
    4. [Rysunki](#matrix_rysunki)
3. [Mnożenie_macierzy_skompresowanej_przez_wektor](#vector)
    1. [Opis algorytmu](#vector_opis)
    2. [Pseudokod](#vector_pseudo)
    3. [Fragment kodu](#vector_fragment)
    4. [Wykres](#vector_wykres)
    5. [Norma Frobeniusa](#vector_norma)
4. [Mnożenie_macierzy_skompresowanej_przez_samą siebie](#mulmatrix)
    1. [Opis algorytmu](#mulmatrix_opis)
    2. [Pseudokod](#mulmatrix_pseudo)
    3. [Fragment kodu](#mulmatrix_fragment)
    4. [Wykres](#mulmatrix_wykres)
    5. [Norma Frobeniusa](#mulmatrix_norma)
5. [Wnioski](#wnioski)


## 1. Polecenie <a name="polecenie"></a>
- Proszę wybrać ulubiony język programowania.
- Proszę wygenerować macierz o rozmiarze 2<sup>3k</sup> dla k = 2, 3, 4
o strukturze opisującej topologię trójwymiarowej
siatki zbudowanej z elementów sześciennych (wiersz =
wierzchołek, niezerowe losowe wartości w kolumnach –
sąsiadujące wierzchołki siatki)
- Proszę użyć rekurencyjną procedurę kompresji macierzy z zadania 3.
- Proszę narysować macierz skompresowaną używając rysowacza z zadania 3
- Proszę przemnożyć macierz skompresowaną przez wektor
- Proszę przemnożyć macierz skompresowaną przez samą siebie

## 2. Generowanie macierzy <a name="matrix"></a>

### 2.1 Opis algorytmu  <a name="matrix_opis"></a>




### 2.2 Pseudokod  <a name="matrix_pseudo"></a>



### 2.3 Fragment kodu  <a name="matrix_fragment"></a>
```python
import numpy as np

def generate_matrix(k):
    grid_size = 2 ** k
    total_size = grid_size ** 3
    matrix = np.zeros((total_size, total_size), dtype=float)
    for z in range(grid_size):
        for y in range(grid_size):
            for x in range(grid_size):
                current_idx = z * grid_size * grid_size + y * grid_size + x
                neighbors = [(x - 1, y, z), (x + 1, y, z),
                    (x, y - 1, z), (x, y + 1, z),
                    (x, y, z - 1), (x, y, z + 1)]
                for nx, ny, nz in neighbors:
                    if 0 <= nx < grid_size and 0 <= ny < grid_size and 0 <= nz < grid_size:
                        neighbor_idx = nz * grid_size * grid_size + ny * grid_size + nx
                        matrix[current_idx, neighbor_idx] = np.random.random()
    return matrix
```
### 2.4 Rysunki <a name="matrix_rysunki"></a>
Rysunki przedstawiają reprezentację skompresowanych macierzy
- r = 1
- epsilon = 1e-7

k = 2
![tree_net_2.png](figures/compression/tree_net_2.png)

k = 3
![tree_net_3.png](figures/compression/tree_net_3.png)

k = 4
![tree_net_4.png](figures/compression/tree_net_4.png)


## 3. Mnożenie macierzy skompresowanej przez wektor <a name="vector"></a>

### 3.1 Opis algorytmu <a name="vector_opis"></a>


### 3.2 Pseudokod <a name="vector_pseudo"></a>
		

### 3.3 Fragment kodu <a name="vector_fragment"></a>
```python
import numpy as np

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
```

### 3.4 Wykres <a name="vector_wykres"></a>
![matrix_vector_mult_time.png](figures/compression/matrix_vector_mult_time.png)

![matrix_vector_mult_time_fit.png](figures/compression/matrix_vector_mult_time_fit.png)

### 3.5 Norma Frobeniusa <a name="vector_norma"></a>
Norma została obliczona na podstawie macierzy gęstej i wektora o wartościach z przedziału (0.00000001, 1.0)

| matrix size | Frobenius norm |
|-------------|:--------------:|
| 2           |      0.0       |
| 4           |      0.0       |
| 8           |   1.602e-31    |
| 16          |   3.944e-30    |
| 32          |   2.682e-29    |
| 64          |   3.282e-28    |
| 128         |   1.578e-27    |
| 256         |   1.217e-26    |
| 512         |   1.349e-25    |
	
## 4. Mnożenie macierzy skompresowanej przez samą siebie <a name="mulmatrix"></a>

### 4.1 Opis algorytmu <a name="mulmatrix_opis"></a>


### 4.2 Pseudokod <a name="mulmatrix_pseudo"></a>
	

### 4.3 Fragmenty kodu <a name="mulmatrix_fragment"></a>
```python
import numpy as np
from src.compression.compress_tree import CompressTree

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
```

### 3.4 Wykres <a name="mulmatrix_wykres"></a>
![matrix_matrix_mult_time.png](figures/compression/matrix_matrix_mult_time.png)

![matrix_matrix_mult_time_fit.png](figures/compression/matrix_matrix_mult_time_fit.png)


### 3.5 Norma Frobeniusa <a name="mulmatrix_norma"></a>
Norma została obliczona na podstawie macierzy gęstych o wartościach z przedziału (0.00000001, 1.0)

| matrix size | Frobenius norm |
|-------------|:--------------:|
| 2           |   4.930e-32    |
| 4           |   6.163e-32    |
| 8           |   2.798e-30    |
| 16          |   8.761e-29    |
| 32          |   2.029e-27    |
| 64          |   5.119e-26    |
| 128         |   1.593e-24    |
| 256         |   4.656e-23    |
## 5. Wnioski  <a name="wnioski"></a>





