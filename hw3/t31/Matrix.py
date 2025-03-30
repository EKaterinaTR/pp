class Matrix:
    def __init__(self, data):
        if not isinstance(data, list) or not all(isinstance(row, list) for row in data):
            raise ValueError("Data must be a 2D list")
        self.rows = len(data)
        if self.rows == 0:
            self.cols = 0
        else:
            self.cols = len(data[0])
            if any(len(row) != self.cols for row in data):
                raise ValueError("All rows must have the same length")
        self.data = data

    def __add__(self, other):
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrices dimensions must match for addition")
        result = [
            [self.data[i][j] + other.data[i][j] for j in range(self.cols)]
            for i in range(self.rows)
        ]
        return self.__class__(result)

    def __mul__(self, other):
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrices dimensions must match for component-wise multiplication")
        result = [
            [self.data[i][j] * other.data[i][j] for j in range(self.cols)]
            for i in range(self.rows)
        ]
        return self.__class__(result)

    def __matmul__(self, other):
        if self.cols != other.rows:
            raise ValueError("Number of columns of the first matrix must equal the number of rows of the second")
        result = [
            [
                sum(self.data[i][k] * other.data[k][j] for k in range(self.cols))
                for j in range(other.cols)
            ]
            for i in range(self.rows)
        ]
        return self.__class__(result)

    def save_to_file(self, filename):
        with open(filename, 'w') as f:
            for row in self.data:
                f.write(' '.join(map(str, row)) + '\n')


