from math import *

class matrix:
    # basic operations of a matrix

    # [ [10.], [10.] ] -> vertical vector
    # | 10.0 |
    # | 10.0 |
    def __init__(self, value):
        self.value = value
        self.rows = len(value)
        self.cols = len(value[0])
        if value == [[]]:
            self.rows = 0

    def zero(self, rows, cols):
        if rows < 1 or cols < 1:
            raise ValueError("Invalid size of matrix")
        else:
            self.rows = rows
            self.cols = cols
            self.value = [[0]*cols for _ in range(rows)]

    def identity(self, dim):
        if dim < 1:
            raise ValueError("Invalid size of matrix")
        else:
            self.rows = dim
            self.cols = dim
            self.value = [[0]*dim for _ in range(dim)]
        for i in range(dim):
            self.value[i][i] = 1

    def show(self):
        for r in range(self.rows):
            print(self.value[r])
        print(' ')

    # overload operations
    def __add__(self, other):
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrices must be of equal dimension to add")
        else:
            res = matrix([[]])
            res.zero(self.rows, self.cols)
            for r in range(self.rows):
                for c in range(self.cols):
                    res.value[r][c] = self.value[r][c] + other.value[r][c]
            return res

    def __sub__(self, other):
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrices must be of equal dimension to subtract")
        else:
            res = matrix([[]])
            res.zero(self.rows, self.cols)
            for r in range(self.rows):
                for c in range(self.cols):
                    res.value[r][c] = self.value[r][c] - other.value[r][c]
            return res    

    def __mul__(self, other):
        if self.cols != other.rows:
            raise ValueError("Matrices must be m*n and n*p to multiply")
        else:
            res = matrix([[]])
            res.zero(self.rows, other.cols)
            for r in range(self.rows):
                for oc in range(other.cols):
                    for c in range(self.cols):
                        res.value[r][oc] += self.value[r][c] * other.value[c][oc]
            return res
        
    def transpose(self):
        res = matrix([[]])
        res.zero(self.cols, self.rows)
        for r in range(self.rows):
            for c in range(self.cols):
                res.value[c][r] = self.value[r][c]
        return res
    
    # Ernest P. Adorio for use of Cholesky & CholeskyInverse function
    def Cholesky(self, ztol=1.0e-5):
        # computes the upper triangular Cholesky factorization of 
        # a positive definite matrix
        res = matrix([[]])
        res.zero(self.rows, self.cols)

        for i in range(self.rows):
            S = sum([(res.value[k][i])**2 for k in range(i)])
            d = self.value[i][i] - S
            if abs(d) < ztol:
                res.value[i][i] = 0.0
            else:
                if d < 0.0:
                    raise ValueError("Matrix not positive-definite")
                res.value[i][i] = sqrt(d)
            for j in range(i+1, self.rows):
                S = sum([res.value[k][i] * res.value[k][j] for k in range(i)])
                if abs(S) < ztol:
                    S = 0.0
                try:
                    res.value[i][j] = (self.value[i][j] - S) / res.value[i][i]
                except:
                    raise ValueError("Zero diagonal")
        return res
    
    def CholeskyInverse(self):
        # compute inverse of matric given its Cholesky upper Triangular
        # decomposition of matrix
        res = matrix([[]])
        res.zero(self.rows, self.cols)
        
        # backward step for inverse
        for j in range(self.rows-1, -1, -1):
            tjj = 1.0 / self.value[j][j]
            S = sum([self.value[j][k] * res.value[j][k] for k in range(j+1, self.rows)])
            res.value[j][j] = 1.0/tjj**2 - S/tjj
            for i in reversed(range(j)):
                res.value[j][i] = res.value[i][j] = -sum([self.value[i][k] * res.value[j][k] for k in range(i+1, j+1)]) / self.value[i][i]
        return res
    
    def inverse(self):
        aux = self.Cholesky()
        res = aux.CholeskyInverse()
        return res
    
    def __repr__(self):
        return repr(self.value)