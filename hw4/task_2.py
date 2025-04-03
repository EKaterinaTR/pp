import math
import concurrent.futures
import time
import os
from typing import Callable


def compute_chunk(f: Callable[[float], float], a: float, b: float,
                  n_iter: int, start: int, end: int) -> float:
    """Вычисляет часть интеграла от start до end итераций"""
    chunk_acc = 0.0
    step = (b - a) / n_iter
    for i in range(start, end):
        chunk_acc += f(a + i * step) * step
    return chunk_acc


def integrate(f: Callable[[float], float],
              a: float,
              b: float,
              *,
              n_jobs: int = 1,
              n_iter: int = 10000000,
              executor_type: str = 'thread') -> float:
    """
    Вычисляет интеграл функции f на интервале [a, b] методом прямоугольников.

    Поддерживает параллельное вычисление с использованием ThreadPoolExecutor или ProcessPoolExecutor.

    Args:
        f: Интегрируемая функция
        a: Начало интервала
        b: Конец интервала
        n_jobs: Количество рабочих процессов/потоков
        n_iter: Количество итераций (прямоугольников)
        executor_type: Тип исполнителя ('thread' или 'process')

    Returns:
        Приближенное значение интеграла
    """
    chunk_size = n_iter // n_jobs
    futures = []

    if executor_type == 'thread':
        executor_class = concurrent.futures.ThreadPoolExecutor
    elif executor_type == 'process':
        executor_class = concurrent.futures.ProcessPoolExecutor
    else:
        raise ValueError("executor_type должен быть 'thread' или 'process'")

    with executor_class(max_workers=n_jobs) as executor:
        # Разбиваем работу на части и отправляем на выполнение
        for i in range(n_jobs):
            start_idx = i * chunk_size
            # Для последнего chunk учитываем возможный остаток
            end_idx = (start_idx + chunk_size) if i < n_jobs - 1 else n_iter
            futures.append(
                executor.submit(compute_chunk, f, a, b, n_iter, start_idx, end_idx)
            )

        # Собираем результаты
        acc = sum(future.result() for future in concurrent.futures.as_completed(futures))

    return acc


def benchmark():
    """Сравнивает производительность ThreadPoolExecutor и ProcessPoolExecutor"""
    cpu_num = os.cpu_count()
    max_jobs = cpu_num * 2 if cpu_num else 4  # На случай если os.cpu_count() вернет None

    results = []
    total_times = {'thread': 0.0, 'process': 0.0}  # Для хранения общего времени

    for executor_type in ['thread', 'process']:
        executor_total_time = 0.0  # Общее время для текущего типа исполнителя

        for n_jobs in range(1, max_jobs + 1):
            start_time = time.time()
            result = integrate(math.cos, 0, math.pi / 2,
                               n_jobs=n_jobs,
                               executor_type=executor_type)
            elapsed = time.time() - start_time

            executor_total_time += elapsed  # Суммируем время

            results.append({
                'executor': executor_type,
                'n_jobs': n_jobs,
                'time': elapsed,
                'result': result
            })

            print(f"{executor_type} with {n_jobs} jobs: {elapsed:.4f} sec, result={result:.6f}")

        total_times[executor_type] = executor_total_time  # Сохраняем общее время

    # Сохраняем результаты в файл с указанием кодировки UTF-8
    with open('artifacts/integration_benchmark.csv', 'w', encoding='utf-8') as f:
        # Записываем заголовок
        f.write("executor,n_jobs,time,result\n")

        # Записываем все результаты
        for r in results:
            f.write(f"{r['executor']},{r['n_jobs']},{r['time']},{r['result']}\n")

        # Добавляем разделитель и общее время
        f.write("\nTotal times:\n")
        f.write(f"ThreadPoolExecutor total time: {total_times['thread']:.4f} sec\n")
        f.write(f"ProcessPoolExecutor total time: {total_times['process']:.4f} sec\n")

    print("\nBenchmark results saved to integration_benchmark.csv")
    print(f"ThreadPoolExecutor total time: {total_times['thread']:.4f} sec")
    print(f"ProcessPoolExecutor total time: {total_times['process']:.4f} sec")


if __name__ == '__main__':
    benchmark()