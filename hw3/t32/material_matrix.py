import numpy as np


class NumpyOperationsMixin:
    """Примесь для арифметических операций с использованием NumPy"""
    def __add__(self, other):
        return self.__class__(self.data + other.data)

    def __sub__(self, other):
        return self.__class__(self.data - other.data)

    def __mul__(self, other):
        return self.__class__(self.data * other.data)

    def __matmul__(self, other):
        return self.__class__(self.data @ other.data)

    def __truediv__(self, other):
        return self.__class__(self.data / other.data)


class FileIOMixin:
    """Примесь для записи объекта в файл"""
    def save_to_file(self, artifacts_dir, filename):
        with open(artifacts_dir / f'{filename}.txt', 'w') as f:
            f.write(f"Material: {self.material}\n")
            np.savetxt(f, self.data, fmt='%g')


class PrettyPrintMixin:
    """Примесь для красивого отображения в консоли"""
    def __str__(self):
        return (f"MaterialMatrix(material='{self.material}', "
                f"shape={self.data.shape}, dtype={self.data.dtype}):\n"
                f"{str(self.data)}")


class PropertyMixin:
    """Примесь для добавления свойств (getter/setter)"""
    @property
    def material(self):
        return self._material

    @material.setter
    def material(self, value):
        if not isinstance(value, str):
            raise ValueError("Material must be a string")
        self._material = value

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        if not isinstance(value, np.ndarray):
            raise ValueError("Data must be a numpy array")
        self._data = value


class MaterialMatrix(NumpyOperationsMixin, FileIOMixin,
                   PrettyPrintMixin, PropertyMixin):
    """Основной класс матрицы с материалом"""
    def __init__(self, data, material="unknown"):
        self.data = np.array(data)
        self.material = material