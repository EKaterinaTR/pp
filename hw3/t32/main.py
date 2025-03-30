import numpy as np
from pathlib import Path

from hw3.t32.material_matrix import MaterialMatrix

# Создаем папку для артефактов
artifacts_dir = Path('C:/Users/User/Desktop/hw/python_project/pp/hw3/artifacts/32')
artifacts_dir.mkdir(parents=True, exist_ok=True)

# Генерация тестовых данных
np.random.seed(0)
matrix_data1 = np.random.randint(0, 10, (3, 3))
matrix_data2 = np.random.randint(0, 10, (3, 3))

# Создание объектов
mat1 = MaterialMatrix(matrix_data1, "steel")
mat2 = MaterialMatrix(matrix_data2, "copper")

# Демонстрация операций
add_result = mat1 + mat2
sub_result = mat1 - mat2
mul_result = mat1 * mat2
matmul_result = mat1 @ mat2
div_result = mat1 / mat2

# Сохранение результатов
mat1.save_to_file(artifacts_dir, 'matrix1')
mat2.save_to_file(artifacts_dir, 'matrix2')
add_result.save_to_file(artifacts_dir, 'matrix+')
sub_result.save_to_file(artifacts_dir, 'matrix-')
mul_result.save_to_file(artifacts_dir, 'matrixmul')
matmul_result.save_to_file(artifacts_dir, 'matrix@')
div_result.save_to_file(artifacts_dir, 'matrix_div')

# Демонстрация вывода в консоль
print("Matrix 1:")
print(mat1)
print("\nMatrix 2:")
print(mat2)
print("\nAddition result:")
print(add_result)
