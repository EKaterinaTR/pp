import numpy as np
import pytest

from hw3.t31.Matrix import Matrix


def test_matrix_operations():
    """Тестирование операций Matrix с использованием NumPy для проверки"""
    # Тестовые данные
    np.random.seed(42)
    a_np = np.random.randint(0, 10, (3, 3))
    b_np = np.random.randint(0, 10, (3, 3))

    # Создаем экземпляры Matrix
    a = Matrix(a_np.tolist())
    b = Matrix(b_np.tolist())

    # Проверка сложения
    add_result = a + b
    add_expected = a_np + b_np
    assert np.array_equal(np.array(add_result.data), add_expected)

    # Проверка покомпонентного умножения
    mul_result = a * b
    mul_expected = a_np * b_np
    assert np.array_equal(np.array(mul_result.data), mul_expected)

    # Проверка матричного умножения
    matmul_result = a @ b
    matmul_expected = a_np @ b_np
    assert np.array_equal(np.array(matmul_result.data), matmul_expected)

    # Проверка на несовместимых размерностях
    c_np = np.random.randint(0, 10, (3, 4))
    c = Matrix(c_np.tolist())

    with pytest.raises(ValueError):
        a + c  # Несовместимые размеры для сложения

    with pytest.raises(ValueError):
        a * c  # Несовместимые размеры для покомпонентного умножения

    # Проверка матричного умножения с совместимыми размерами
    d_np = np.random.randint(0, 10, (4, 3))
    d = Matrix(d_np.tolist())
    matmul_result2 = c @ d
    matmul_expected2 = c_np @ d_np
    assert np.array_equal(np.array(matmul_result2.data), matmul_expected2)


def test_edge_cases():
    """Тестирование граничных случаев"""
    # Пустая матрица
    empty = Matrix([])
    assert empty.rows == 0
    assert empty.cols == 0

    # Матрица 1x1
    m1 = Matrix([[5]])
    m2 = Matrix([[3]])
    assert (m1 + m2).data == [[8]]
    assert (m1 * m2).data == [[15]]
    assert (m1 @ m2).data == [[15]]


if __name__ == "__main__":
    pytest.main(["-v", __file__])