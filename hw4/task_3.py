import multiprocessing
import time
import threading
from datetime import datetime
import codecs
import random


def process_a(input_queue, output_queue):
    """
    Процесс A: принимает сообщения из input_queue, применяет .lower(),
    и отправляет в output_queue раз в 5 секунд.
    """
    def worker():
        while True:
            message = input_queue.get()
            print(f"[{datetime.now()}] Process A получил: {message}")  # Логирование получения
            if message == "STOP":
                break
            processed_message = message.lower()
            print(f"[{datetime.now()}] Process A обработал: {message} -> {processed_message}")  # Логирование обработки
            output_queue.put(processed_message)
            print(f"[{datetime.now()}] Process A отправил в B: {processed_message}")  # Логирование отправки
            time.sleep(5)

    thread = threading.Thread(target=worker)
    thread.start()
    thread.join()


def process_b(input_queue, output_queue):
    """
    Процесс B: принимает сообщения из input_queue, применяет rot13,
    печатает в stdout и отправляет в output_queue.
    """
    def worker():
        while True:
            message = input_queue.get()
            print(f"[{datetime.now()}] Process B получил: {message}")  # Логирование получения
            if message == "STOP":
                break
            rot13_message = codecs.encode(message, 'rot13')
            print(f"[{datetime.now()}] Process B обработал: {message} -> {rot13_message}")  # Логирование обработки
            output_queue.put(rot13_message)
            print(f"[{datetime.now()}] Process B отправил в главный процесс: {rot13_message}")  # Логирование отправки

    thread = threading.Thread(target=worker)
    thread.start()
    thread.join()


def process_user_simulator(output_queue):
    """
    Процесс-симулятор пользователя: автоматически отправляет сообщения в queue_a.
    """
    messages = [
        "Hello World!",
        "Python is awesome",
        "ROT13 Test",
        "Multiprocessing",
        "Goodbye!"
    ]

    while True:
        message = random.choice(messages)
        print(f"[{datetime.now()}] Симулятор пользователя отправил: {message}")
        output_queue.put(message)
        time.sleep(3)


def main():
    """
    Главный процесс: создает очереди и процессы, обрабатывает ввод пользователя.
    """
    queue_a = multiprocessing.Queue()
    queue_b = multiprocessing.Queue()
    queue_main = multiprocessing.Queue()

    p_a = multiprocessing.Process(target=process_a, args=(queue_a, queue_b))
    p_b = multiprocessing.Process(target=process_b, args=(queue_b, queue_main))
    p_user_sim = multiprocessing.Process(target=process_user_simulator, args=(queue_a,))

    p_a.start()
    p_b.start()
    p_user_sim.start()

    print("Главный процесс запущен. Симулятор пользователя активен (Ctrl+C для выхода).")

    try:
        while True:
            received = queue_main.get()
            print(f"[{datetime.now()}] Главный процесс получил: {received}")

    except KeyboardInterrupt:
        print("\nЗавершение работы...")
        queue_a.put("STOP")
        queue_b.put("STOP")
        p_user_sim.terminate()

    p_a.join()
    p_b.join()
    p_user_sim.join()
    print("Главный процесс завершен.")


if __name__ == "__main__":
    main()