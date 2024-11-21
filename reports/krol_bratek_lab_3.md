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

4. [Wnioski](#wnioski)
5. [Bibliografia](#biblio)


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
	
## 4. Wnioski  <a name="wnioski"></a>


## 5. Bibliografia  <a name="biblio"></a>
- Wykłady prof. dr hab. Macieja Paszyńskiego (https://home.agh.edu.pl/~paszynsk/RM/RachunekMacierzowy1.pdf)




