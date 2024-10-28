# Algorytmy Macierzowe

## Sprawozdanie nr 2

## 06.11.2024

## Mateusz Król, Natalia Bratek
## gr. 3

## Spis treści
1. [Polecenie](#polecenie)
2. [Rekurencyjne odwracanie macierzy](#inverse)
   1. [Opis algorytmu](#inversion_opis)
    2. [Pseudokod](#inversion_pseudo)
    3. [Fragment kodu](#inversion_fragment)
3. [Eliminacja Gaussa](#gauss)
    1. [Opis algorytmu](#gauss_opis)
    2. [Pseudokod](#gauss_pseudo)
    3. [Fragment kodu](#gauss_fragment)
4. [LU Faktoryzacja](#lu)
    1. [Opis algorytmu](#lu_opis)
    2. [Pseudokod](#lu_pseudo)
    3. [Fragment kodu](#lu_fragment)
5. [Obliczanie wyznacznika](#det)
    1. [Opis algorytmu](#det_opis)
    2. [Pseudokod](#det_pseudo)
    3. [Fragment kodu](#det_fragment)
6. [Wykresy](#wykresy)
7. [Szacowanie złożoności obliczeniowej](#complexity)
8. [Porównanie wyników z Matlabem](#matlab)
9. [Wnioski](#wnioski)
10. [Bibliografia](#biblio)

## 1. Polecenie <a name="polecenie"></a>

Proszę wybrać ulubiony język programowania, wygenerować macierze losowe o wartościach z przedziału otwartego (0.00000001, 1.0) i zaimplementować:
- Rekurencyjne odwracanie macierzy
- Rekurencyjna eliminacja Gaussa 
- Rekurencyjna LU faktoryzacja 
- Rekurencyjne liczenie wyznacznika

Proszę zliczać liczbę operacji zmiennoprzecinkowych (+-*/ liczb) wykonywanych podczas mnożenia macierzy.


## 2. Rekurencyjne odwracanie macierzy <a name="inverse"></a>

### 2.1 Opis algorytmu  <a name="inversion_opis"></a>
Rekurencyjne odwracanie macierzy polega na podzieleniu macierzy A na 4 podmacierze A11, A12, A21, A22 i wyznaczeniu odwrotności macierzy A11.  Kolejnym krokiem jest obliczenie tzw. macierzy Schura S22. Po wyznaczeniu S22 wywoływana jest rekurencyjnie jej odwrotność. 
Wykorzystując algorytm Strassena z poprzedniego laboratorium, wykonujemy mnożenia na poszczególnych podmacierzach, aby uzyskać ostateczne bloki odwrotności: B11, B12, B2 oraz B22. Na koniec wszystkie bloki są składane w jedną macierz wynikową, która stanowi odwrotność macierzy A.


### 2.2 Pseudokod  <a name="inversion_pseudo"></a>

      inverse(matrix)
	     Jeżeli matrix ma rozmiar 1 
		    zwróć 1/matrix

	     Podziel matrix na bloki:
            - jeśli rozmiar macierzy jest nieparzysty podziel na bloki A11, A12, A21, A22 przy użyciu dynamicznego podziału
            - jeśli rozmiar macierzy jest parzysty podziel na bloki A11, A12, A21, A22 przy użyciu standardowego podziału
      
         Rekurencyjnie wywołaj inverse na A11
                A11_inv = inverse(A11)
         Oblicz pomocniczą macierz  S22
                S22 = A22 - (A21 * A11_inv * A12)
         Jeżeli S22 jest macierzą 1x1:
                Odwróć macierz S22 dla macierzy 1x1
         W przeciwnym przypadku:
                Rekurencyjnie wywołaj inverse na S22
                    S22_inv = inverse(S22)
         Oblicz odwrotne bloki B11, B12, B21, B22
                B11 = A11_inv + (A11_inv * A12 * S22_inv * A21 * A11_inv)
                B12 = -A11_inv * A12 * S22_inv
                B21 = -S22_inv * A21 * A11_inv
                B22 = S22_inv
         Zwróć połączone bloki:
            - Jeżeli n jest nieparzyste zwróć połączone bloki B11, B12, B21, B22 za pomocą dynamicznego łączenia 
            - W przeciwnym razie zwróć połączone 4 bloki B11, B12, B21, B22 



### 2.3 Fragmenty kodu  <a name="inversion_fragment"></a>

```python
    def inverse_rec(self, matrix):
        n = len(matrix)
        if n == 1:
            return self.calculator.inverse_one_by_one_matrix(matrix)

        if n % 2 != 0:
            A11, A12, A21, A22 = self.calculator.split_into_block_matrices_dynamic_peeling(matrix)
        else:
            A11, A12, A21, A22 = self.calculator.split_into_block_matrices(matrix)

        A11_inv = self.inverse_rec(A11)
        S22 = self.calculator.subtract(A22, self.strassen.run(A21, self.strassen.run(A11_inv, A12)))

        if len(S22) == 1 and len(S22[0]) == 1:
            S22_inv = self.calculator.inverse_one_by_one_matrix(S22)
        else:
            S22_inv = self.inverse_rec(S22)

        B11 = self.calculator.add(A11_inv, self.strassen.run(self.strassen.run( self.strassen.run(
                                      self.strassen.run(A11_inv, A12), S22_inv), A21), A11_inv))
        B12 = self.strassen.run(self.strassen.run(self.calculator.negate(A11_inv), A12), S22_inv)
        B21 = self.strassen.run(self.strassen.run(self.calculator.negate(S22_inv), A21), A11_inv)
        B22 = S22_inv

        if n % 2 != 0:
            return self.calculator.connect_block_matrices_dynamic_peeling(B11, B12, B21, B22)
        else:
            return self.calculator.connect_block_matrices(B11, B12, B21, B22)

```

## 3. Eliminacja Gaussa <a name="gauss"></a>

### 3.1 Opis algorytmu  <a name="gauss_opis"></a>

### 3.2 Pseudokod  <a name="gauss_pseudo"></a>

### 3.3 Fragmenty kodu  <a name="gauss_fragment"></a>


## 4. LU Faktoryzacja  <a name="lu"></a>

### 4.1 Opis algorytmu  <a name="lu_opis"></a>
Rekurencyjny algorytm LU faktoryzacji dzieli macierz A na mniejsze bloki i rekursywnie oblicza macierze dolną L i górną U, tak aby A=LU.
Wykorzystamy algorytm Strassena do mnożenia macierzy oraz rekurencyjne odwracanie macierzy.

### 4.2 Pseudokod  <a name="lu_pseudo"></a>

      LU(matrix)
	     Jeżeli matrix ma rozmiar 1 
		    zwróć macierz jednostkową oraz matrix
	     Podziel matrix na bloki:
            - jeśli rozmiar macierzy jest nieparzysty podziel na bloki A11, A12, A21, A22 przy użyciu dynamicznego podziału
            - jeśli rozmiar macierzy jest parzysty podziel na bloki A11, A12, A21, A22 przy użyciu standardowego podziału
         Oblicz L11 i U11 przez rekurencyjne wywołanie LU(A11)
            L11, U11 = LU(A11)
         Oblicz odwrotność U11 i L11
            U11_inv = inverse(U11)
            L11_inv = inverse (L11)
         Oblicz L21 oraz U12
            L21 = A21* U11_inv
            U12 = L11_inv * A12
         Oblicz pomocniczą macierz
            S = A22 -  L21 * U12
         Wykonaj rekurencyjną faktoryzację LU dla S
            Ls, Us = LU(S)
         Połącz bloki:
            -Jeżeli n jest nieparzyste połącz bloki za pomocą dynamicznego łączenia
               L = (L11, macierz zerowa o rozmiarze U12xL11, L21, Ls)
               U = (U11, U12, macierz zerowa o rozmiarze L21xU11, Us)
            - W przeciwnym razie zwróć połączone bloki za pomocą standardowego łączenia
               L = (L11, macierz zerowa o rozmiarze U12xL11, L21, Ls)
               U = (U11, U12,  macierz zerowa o rozmiarze L21xU11, Us)
      Zwróć L, U


### 4.3 Fragmenty kodu  <a name="lu_fragment"></a>

```python
    def lu_recursive(self, matrix):
        n = len(matrix)

        if n == 1:
            return [[1]], [[matrix[0][0]]]

        if n % 2 == 0:
            A11, A12, A21, A22 = self.calculator.split_into_block_matrices(matrix)
        else:
            A11, A12, A21, A22 = self.calculator.split_into_block_matrices_dynamic_peeling(matrix)

        L11, U11 = self.lu_recursive(A11)

        U11_inv = self.inversion.inverse(U11)
        L11_inv = self.inversion.inverse(L11)

        L21 = self.strassen.run(A21, U11_inv)
        U12 = self.strassen.run(L11_inv, A12)
        S = self.calculator.subtract(A22, self.strassen.run(L21, U12))

        Ls, Us = self.lu_recursive(S)

        if n % 2 == 0:
            L = self.calculator.connect_block_matrices(L11, [[0] * len(U12[0])] * len(L11), L21, Ls)
            U = self.calculator.connect_block_matrices(U11, U12, [[0] * len(L21[0])] * len(U11), Us)
        else:
            L = self.calculator.connect_block_matrices_dynamic_peeling(L11, [[0] * len(U12[0])] * len(L11), L21, Ls)
            U = self.calculator.connect_block_matrices_dynamic_peeling(U11, U12, [[0] * len(L21[0])] * len(U11), Us)

        return L, U
```


## 5. Obliczanie wyznacznika <a name="det"></a>

### 5.1 Opis algorytmu  <a name="det_opis"></a>

### 5.2 Pseudokod  <a name="det_pseudo"></a>

### 5.3 Fragmenty kodu  <a name="det_fragment"></a>

## 6. Wykresy <a name="wykresy"></a>

## 7. Szacowanie złożoności obliczeniowej  <a name="complexity"></a>


## 8. Porównanie wyników z Matlabem <a name="matlab"></a>

	
## 9. Wnioski  <a name="wnioski"></a>

## 10. Bibliografia  <a name="biblio"></a>
- Wykłady prof. dr hab. Macieja Paszyńskiego (https://home.agh.edu.pl/~paszynsk/RM/RachunekMacierzowy1.pdf)