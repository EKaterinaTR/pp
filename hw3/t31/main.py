import numpy as np

from hw3.t31.Matrix import Matrix

np.random.seed(0)
matrix_a = np.random.randint(0, 10, (10, 10))
matrix_b = np.random.randint(0, 10, (10, 10))

A = Matrix(matrix_a.tolist())
B = Matrix(matrix_b.tolist())

folder = 'C:/Users/User/Desktop/hw/python_project/pp/hw3/artifacts/31'
try:
    add_result = A + B
    add_result.save_to_file(f'{folder}/matrix+.txt')
except ValueError as e:
    print(f"Addition error: {e}")

try:
    mul_result = A * B
    mul_result.save_to_file(f'{folder}/matrixmul.txt')
except ValueError as e:
    print(f"Multiplication error: {e}")

try:
    matmul_result = A @ B
    matmul_result.save_to_file(f'{folder}/matrix@.txt')
except ValueError as e:
    print(f"Matrix multiplication error: {e}")