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
    _cache = {}
    use_cache = False
    def __matmul__(self, other):
        """Кэшированное матричное умножение с ручным кэшированием"""
        cache_key = (hash(self), hash(other), self.cols)  # Ключ кэша


        if self.cols != other.rows:
                raise ValueError("Number of columns of the first matrix must equal the number of rows of the second")

        if cache_key in self._cache and self.use_cache:
            print("Using cached result")
            return self._cache[cache_key]

        result = super().__matmul__(other)

        self._cache[cache_key] = result
        return result


