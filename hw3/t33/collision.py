import numpy as np

from hw3.t33.HashMatrix import HashMatrix


def find_collision():
    """Поиск коллизии для хэш-функции"""
    np.random.seed(42)

    while True:
        # Генерируем матрицы 2x2
        A = HashMatrix([[np.random.randint(0, 10) for _ in range(2)] for _ in range(2)])
        C = HashMatrix([[np.random.randint(0, 10) for _ in range(2)] for _ in range(2)])

        if hash(A) == hash(C) and A != C:
            B = HashMatrix([[np.random.randint(0, 10) for _ in range(2)] for _ in range(2)])
            D = B

            AB = A @ B
            CD = C @ D

            print(type(AB))
            print(type(CD))

            if AB != CD:
                # Сохраняем артефакты
                for name, matrix in [('A', A), ('B', B), ('C', C), ('D', D), ('AB', AB), ('CD', CD)]:
                    matrix.save_to_file(f'C:/Users/User/Desktop/hw/python_project/pp/hw3/artifacts/33/{name}.txt')

                with open('C:/Users/User/Desktop/hw/python_project/pp/hw3/artifacts/33/hash.txt', 'w') as f:
                    f.write(f"Hash(A) = Hash(C) = {hash(A)}\n")
                    f.write(f"Hash(AB) = {hash(AB)}\n")
                    f.write(f"Hash(CD) = {hash(CD)}\n")

                return A, B, C, D


if __name__ == "__main__":
    A, B, C, D = find_collision()
    print(f"Found collision!")
    print(f"Hash(A) = {hash(A)}, Hash(C) = {hash(C)}")
    print(f"A == C: {A == C}")
    print(f"B == D: {B == D}")
    print(f"A @ B == C @ D: {(A @ B) == (C @ D)}")