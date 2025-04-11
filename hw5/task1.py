from typing import Optional

import aiohttp
import asyncio
import os
from datetime import datetime
import random
import re


class WaifuDownloader:
    def __init__(self, max_retries: int = 3, timeout: int = 15):
        self.max_retries = max_retries
        self.timeout = aiohttp.ClientTimeout(total=timeout)
        self.downloaded_count = 0
        self.base_url = "https://www.thiswaifudoesnotexist.net"

    async def _get_image_url(self, session: aiohttp.ClientSession) -> Optional[str]:
        """Получает URL изображения waifu из HTML-страницы"""
        try:
            async with session.get(self.base_url, timeout=self.timeout) as response:
                if response.status == 200:
                    html = await response.text()
                    # Ищем URL изображения в meta-теге og:image
                    match = re.search(r'<meta property="og:image" content="([^"]+)">', html)
                    if match:
                        return match.group(1)
                    # Альтернативный поиск по шаблону URL изображения
                    match = re.search(r'example-\d+\.jpg', html)
                    if match:
                        return f"{self.base_url}/{match.group()}"
        except Exception as e:
            print(f"Ошибка при получении URL изображения: {str(e)}")
        return None

    async def download_waifu(self, session: aiohttp.ClientSession, save_dir: str) -> Optional[str]:
        """Скачивает одно изображение waifu"""
        for attempt in range(self.max_retries):
            try:
                # Сначала получаем URL изображения
                image_url = await self._get_image_url(session)
                if not image_url:
                    continue

                # Генерируем уникальное имя файла
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = os.path.join(save_dir, f"waifu_{timestamp}_{random.randint(1000, 9999)}.jpg")

                # Скачиваем изображение
                async with session.get(image_url, timeout=self.timeout) as response:
                    if response.status == 200:
                        content_type = response.headers.get('Content-Type', '')
                        if 'image' not in content_type:
                            raise ValueError(f"Ожидалось изображение, получен {content_type}")

                        with open(filename, 'wb') as f:
                            async for chunk in response.content.iter_chunked(1024):
                                f.write(chunk)

                        self.downloaded_count += 1
                        print(f"Успешно загружено: {filename}")
                        return filename
                    else:
                        print(f"Попытка {attempt + 1}: Ошибка HTTP {response.status} для {image_url}")
            except (aiohttp.ClientError, asyncio.TimeoutError, ValueError) as e:
                print(f"Попытка {attempt + 1}: Ошибка при скачивании: {str(e)}")

            if attempt < self.max_retries - 1:
                await asyncio.sleep(random.uniform(1, 3))  # Случайная задержка

        return None

    async def worker(self, session: aiohttp.ClientSession, save_dir: str, queue: asyncio.Queue):
        """Рабочий процесс для загрузки изображений"""
        while True:
            try:
                task = await queue.get()
                if task is None:  # Сигнал завершения
                    queue.task_done()
                    break

                await self.download_waifu(session, save_dir)
                queue.task_done()
            except Exception as e:
                print(f"Ошибка в worker: {str(e)}")
                queue.task_done()

    async def download_waifus(self, num_images: int, save_dir: str, concurrency: int = 3):
        """Асинхронно скачивает указанное количество изображений"""
        os.makedirs(save_dir, exist_ok=True)

        connector = aiohttp.TCPConnector(limit=concurrency, force_close=True)

        async with aiohttp.ClientSession(connector=connector) as session:
            queue = asyncio.Queue(maxsize=num_images + concurrency)

            workers = [
                asyncio.create_task(self.worker(session, save_dir, queue))
                for _ in range(concurrency)
            ]

            for _ in range(num_images):
                await queue.put(True)

            for _ in range(concurrency):
                await queue.put(None)

            await queue.join()
            await asyncio.gather(*workers)

            # Дополнительные попытки, если загружено недостаточно
            while self.downloaded_count < num_images:
                remaining = num_images - self.downloaded_count
                print(f"Загружено {self.downloaded_count} из {num_images}. Пробуем загрузить оставшиеся {remaining}...")

                queue = asyncio.Queue(maxsize=remaining + concurrency)
                workers = [
                    asyncio.create_task(self.worker(session, save_dir, queue))
                    for _ in range(min(concurrency, remaining))
                ]

                for _ in range(remaining):
                    await queue.put(True)

                for _ in range(len(workers)):
                    await queue.put(None)

                await queue.join()
                await asyncio.gather(*workers)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Асинхронный загрузчик waifu с thiswaifudoesnotexist.net")
    parser.add_argument("--count", type=int, default=10, help="Количество изображений для загрузки")
    parser.add_argument("--dir", type=str, default=r"C:\Users\User\Desktop\hw\python_project\pp\hw5\artifacts\t1", help="Папка для сохранения")
    parser.add_argument("--retries", type=int, default=3, help="Максимальное количество попыток загрузки")
    parser.add_argument("--concurrency", type=int, default=3, help="Количество одновременных загрузок")
    parser.add_argument("--timeout", type=int, default=20, help="Таймаут загрузки в секундах")

    args = parser.parse_args()

    print(f"Начинаем загрузку {args.count} изображений waifu в папку '{args.dir}'...")
    downloader = WaifuDownloader(max_retries=args.retries, timeout=args.timeout)
    asyncio.run(downloader.download_waifus(args.count, args.dir, args.concurrency))
    print(f"Загрузка завершена! Успешно загружено {downloader.downloaded_count} изображений.")