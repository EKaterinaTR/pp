import time
import threading
import multiprocessing


def fibonacci(n):
    """Вычисление n-го числа Фибоначчи."""
    if n <= 1:
        return n
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)


def sync_execution(n, times=10):
    """Синхронное выполнение функции times раз."""
    start_time = time.time()
    for _ in range(times):
        fibonacci(n)
    end_time = time.time()
    return end_time - start_time


def threading_execution(n, times=10):
    """Выполнение функции times раз в отдельных потоках."""
    threads = []
    start_time = time.time()

    for _ in range(times):
        thread = threading.Thread(target=fibonacci, args=(n,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    end_time = time.time()
    return end_time - start_time


def multiprocessing_execution(n, times=10):
    """Выполнение функции times раз в отдельных процессах."""
    processes = []
    start_time = time.time()

    for _ in range(times):
        process = multiprocessing.Process(target=fibonacci, args=(n,))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    end_time = time.time()
    return end_time - start_time


def main():
    n = 30  # Достаточно большое число, чтобы увидеть разницу во времени
    times = 10

    # Замеряем время для каждого метода
    sync_time = sync_execution(n, times)
    threads_time = threading_execution(n, times)
    multiprocessing_time = multiprocessing_execution(n, times)

    # Записываем результаты в файл
    with open(f"artifacts/fibonacci_results_{n}.txt", "w", encoding="utf-8") as f:
        f.write(f"Результаты сравнения времени выполнения вычисления чисел Фибоначчи (n={n}, times={times}):\n")
        f.write("-" * 70 + "\n")
        f.write(f"Синхронное выполнение: {sync_time:.2f} секунд\n")
        f.write(f"Использование потоков (threading): {threads_time:.2f} секунд\n")
        f.write(f"Использование процессов (multiprocessing): {multiprocessing_time:.2f} секунд\n")
        f.write("-" * 70 + "\n")

        if sync_time < threads_time and sync_time < multiprocessing_time:
            f.write("Вывод: Синхронное выполнение оказалось быстрее всего.\n")
        elif threads_time < multiprocessing_time:
            f.write("Вывод: Использование потоков оказалось быстрее процессов.\n")
        else:
            f.write("Вывод: Использование процессов оказалось быстрее потоков.\n")

if __name__ == "__main__":
    main()
