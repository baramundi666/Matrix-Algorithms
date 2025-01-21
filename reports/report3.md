# Algorytmy Macierzowe

## Sprawozdanie nr 3

## 4.12.2024

## Mateusz Król, Natalia Bratek
## gr. 3

## Spis treści
1. [Polecenie](#polecenie)
2. [Rekurencyjna kompresja macierzy](#compress)
	1. [Opis algorytmu](#compress)
    2. [Pseudokod](#compress_pseudo)
    3. [Fragment kodu](#compress_fragment)
3. [Rekurencyjna dekompresja macierzy](#decompress)
	1. [Opis algorytmu](#decompress)
    2. [Pseudokod](#decompress_pseudo)
    3. [Fragment kodu](#decompress_fragment)
4. [Wizualizacja](#wizualizacja)
5. [Wykresy i bitmapy](#5-wykresy-i-bitmapy)
    1. [Wartości osobliwe](#51-wartości-osobliwe)
    2. [Nieskompresowana bitmapa](#52-nieskompresowana-bitmapa)
    3. [Kompresja](#53-kompresja)
        1. [Wariant 1](#531-wariant-1)
        2. [Wariant 2](#532-wariant-2)
        3. [Wariant 3](#533-wariant-3)
        4. [Wariant 4](#534-wariant-4)
        5. [Wariant 5](#535-wariant-5)
        6. [Wariant 6](#536-wariant-6)
6. [Bibliografia](#biblio)


## 1. Polecenie <a name="polecenie"></a>

- Proszę wybrać ulubiony język programowania.
- Proszę wybrać ulubioną kolorową bitmapę np. 500 × 500
- Prosze zamienić bitmapę na 3 macierze Red Green Blue
(wartości z przedziału [0,255])
- Proszę napisać rekurencyjną kompresje macierzy z
wykorzystaniem częściowego SVD dla wybranych
parametrów δ=najmniejsza wartość osobliwa (wyrzucamy
mniejsze) i b= maksymalny rank (liczba wartości osobliwych)
- Proszę zaimplementować rysowacz skompresowanej macierzy
- Proszę zaimplementować rysowacz skompresowanej bitmapy


## 2. Rekurencyjna kompresja macierzy <a name="compress"></a>

### 2.1 Opis algorytmu  <a name="compress_opis"></a>

Algorytm polega na hierarchicznej kompresji macierzy z wykorzystaniem częściowego SVD. Dzieli macierz na coraz mniejsze bloki, aż każdy blok będzie można przybliżyć macierzą o niskim ranku i z wymaganą dokładnością.
Najpierw, dla danego bloku macierzy, algorytm oblicza SVD przy użyciu metody randomized_svd. Jeśli blok spełnia warunek dopuszczalności, algorytm oznacza go jako liść w drzewie, zapisując wynikowe macierze U, S, i V. Jeśli nie, blok zostaje podzielony na cztery mniejsze części, które są następnie przetwarzane w ten sam sposób. 
Proces jest powtarzany rekurencyjnie, aż każdy blok spełni kryterium przybliżenia lub osiągnie minimalny rozmiar.




### 2.2 Pseudokod  <a name="compress_pseudo"></a>


    compress(r, epsilon):

        Wyodrębnij bieżący blok macierzy 
        matrix_block =  matrix[t_min:t_max, s_min:s_max]

        if blok jest zerowy:
	        oznacz blok jako liść 
	        ustaw rank na 0
	        zwróć blok

        oblicz dekompozyzję SVD
        (U, Sigma, V) = RandomizedSVD(matrix_block,r + 1)

        if blok spełnia warunek dopuszczalności
	        zapisz U[:, :r], Sigma[:r], V[:r, :]
	        oznacz blok jako liść 
            zwróć blok
	    else:

		    Stwórz listę children
            Dodaj do children: CompressTree(matrix, t_min, new_t_max, s_min, new_s_max, r, epsilon)
            Dodaj do children: CompressTree(matrix, t_min, new_t_max, new_s_max, s_max, r, epsilon)
            Dodaj do children: CompressTree(matrix, new_t_max, t_max, s_min, new_s_max, r, epsilon)
            Dodaj do children: CompressTree(matrix, new_t_max, t_max, new_s_max, s_max, r, epsilon)

            Rekurencyjnie przetwórz dzieci
            dla child w children: 
                wywołaj compress dla child z parametrami (r, epsilon)


        zwróć blok z children



### 2.3 Fragment kodu  <a name="compress_fragment"></a>
 
```python
    def is_admissible(self,  U, S, V, r, epsilon):
        if self.t_min + r == self.t_max or S[r] <= epsilon:
            self.rank = r
            self.set_leaf(U[:, :r], S[:r], V[:r, :])
            return True
        return False

    def set_leaf(self, U, S, V):
        self.is_leaf = True
        self.U = U
        self.S = S
        self.V = V

    def compress(self, r, epsilon):
        matrix_block = self.matrix[self.t_min:self.t_max, self.s_min:self.s_max]

        if np.sum(matrix_block) == 0:
            self.rank = 0
            self.is_leaf = True
            self.zeros = True
            return self

        U, Sigma, V = randomized_svd(matrix_block, n_components=r + 1, random_state=0)
        sigma = np.diag(Sigma)
        if self.is_admissible( U,Sigma,V, r, epsilon):
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

```

## 3. Rekurencyjna dekompresja macierzy <a name="decompress"></a>

### 3.1 Opis algorytmu  <a name="decompress_opis"></a>

Decompress rekonstruuje oryginalną macierz z jej skompresowanej reprezentacji w drzewie. Jeśli węzeł drzewa jest liściem, funkcja sprawdza czy reprezentuje blok zerowy. 
Jeśli tak, zwraca blok wypełniony zerami, a w przeciwnym razie odtwarza blok macierzy z zapisanych macierzy U, S i V przy użyciu operacji macierzowych.
Dla węzłów wewnętrznych, które mają dzieci, funkcja inicjalizuje pustą macierz o odpowiednich wymiarach, a następnie wypełnia jej części poprzez wywołanie funkcji decompress rekurencyjnie dla każdego dziecka. 
Każde dziecko odpowiada jednemu z czterech podbloków macierzy, które są umieszczane w odpowiednich miejscach macierzy wynikowej.



### 3.2 Pseudokod  <a name="decompress_pseudo"></a>

    decompress():

        if węzeł jest liściem:
            if blok jest zerowy:
                return macierz zerowa o wymiarach (t_max - t_min, s_max - s_min)
            else:
                odtwórz macierz 
                macierz = U * diag(S) * V 
                zwróć macierz o wymiarach (t_max - t_min, s_max - s_min)

	    zinicjalizuj macierz decompressed_matrix o wymiarach (t_max - t_min, s_max - s_min) 
        oblicz połowę zakresów:
	        half_row  = (t_max + t_min) // 2
            half_col = (s_max + s_min) // 2
	
	    dla każdego dziecka (child) w children:
		
		    if indeks dziecka == 0:
			    Wypełnij górny lewy kwadrant: 
                decompressed_matrix[:half_row - t_min, :half_col - s_min] = child.DEOMPRESS()

		    if indeks dziecka == 1:
                Wypełnij górny prawy kwadrant:
                decompressed_matrix[:half_row - t_min, half_col - s_min:] = child.DECOMPRESS(

            if indeks dziecka == 2: 
                Wypełnij dolny lewy kwadrant: 
                decompressed_matrix[half_row - t_min:, :half_col - s_min] = child.DECOMPRESS()


            if indeks dziecka == 3: 
                Wypełnij dolny prawy kwadrant: 
                decompressed_matrix[half_row - t_min:, half_col - s_min:] = child.DECOMPRESS()


	    zwróć decompressed_matrix



### 3.3 Fragment kodu  <a name="decompress_fragment"></a>

```python

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
```

## 4. Wizualizacja <a name="wizualizacja"></a>
### 4.1 Rysowacz skompresowanej macierzy <a name="wizualizacja"></a>
```python
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
```

### 4.2 Rysowacz skompresowanej bitmapy <a name="wizualizacja"></a>
```python
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
```

## 5. Wykresy i bitmapy 
### 5.1 Wartości osobliwe 
![alt text](figures/compression/singular_values.png)
### 5.2 Nieskompresowana bitmapa 
Wymiary: 512x512
![alt text](figures/compression/original.png)
![alt text](figures/compression/rgb_original.png)
### 5.3 Kompresja 
#### 5.3.1 Wariant 1 
- r = 1
- epsilon = sigma_1

Macierze kompresji są identyczne dla R, G, B:
![alt text](figures/compression/tree_var1.png)
Wynikowe bitmapy R, G, B:
![alt text](figures/compression/rgb_var1.png)
Połączona bitmapa:

![alt text](figures/compression/compr_var1.png)
#### 5.3.2 Wariant 2
- r = 1
- epsilon = sigma_512

Macierze kompresji dla R, G, B:
![alt text](figures/compression/tree1_var2.png)
![alt text](figures/compression/tree2_var2.png)
![alt text](figures/compression/tree3_var2.png)
Wynikowe bitmapy R, G, B:
![alt text](figures/compression/rgb_var2.png)
Połączona bitmapa:

![alt text](figures/compression/compr_var2.png)
#### 5.3.3 Wariant 3
- r = 1
- epsilon = sigma_256

Macierze kompresji dla R, G, B:
![alt text](figures/compression/tree1_var3.png)
![alt text](figures/compression/tree2_var3.png)
![alt text](figures/compression/tree3_var3.png)
Wynikowe bitmapy R, G, B:
![alt text](figures/compression/rgb_var3.png)
Połączona bitmapa:

![alt text](figures/compression/compr_var3.png)

#### 5.3.4 Wariant 4
- r = 4
- epsilon = sigma_1

Macierze kompresji są identyczne dla R, G, B:
![alt text](figures/compression/tree_var4.png)
Wynikowe bitmapy R, G, B:
![alt text](figures/compression/rgb_var4.png)
Połączona bitmapa:

![alt text](figures/compression/compr_var4.png)
#### 5.3.5 Wariant 5 
- r = 4
- epsilon = sigma_512

Macierze kompresji dla R, G, B:
![alt text](figures/compression/tree1_var5.png)
![alt text](figures/compression/tree2_var5.png)
![alt text](figures/compression/tree3_var5.png)
Wynikowe bitmapy R, G, B:
![alt text](figures/compression/rgb_var5.png)
Połączona bitmapa:

![alt text](figures/compression/compr_var5.png)
#### 5.3.6 Wariant 6 
- r = 4
- epsilon = sigma_256

Macierze kompresji dla R, G, B:
![alt text](figures/compression/tree1_var6.png)
![alt text](figures/compression/tree2_var6.png)
![alt text](figures/compression/tree3_var6.png)
Wynikowe bitmapy R, G, B:
![alt text](figures/compression/rgb_var6.png)
Połączona bitmapa:

![alt text](figures/compression/compr_var6.png)


## 6. Bibliografia  <a name="biblio"></a>
- Wykłady prof. dr hab. Macieja Paszyńskiego (https://home.agh.edu.pl/~paszynsk/RM/RachunekMacierzowy1.pdf)




