from hw3.t31.Matrix import Matrix


class HashMixin:
    """Примесь для хэширования матриц.
    Хэш-функция: (сумма всех элементов * количество элементов) % 1000
    """
    def __hash__(self):
        total_sum = sum(sum(row) for row in self.data)
        num_elements = self.rows * self.cols
        return (total_sum * num_elements) % 1000



class HashMatrix(HashMixin,Matrix):
    def __matmul__(self, other):
        return super().__matmul__(other)