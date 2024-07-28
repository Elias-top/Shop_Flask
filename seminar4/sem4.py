import os
import time
import asyncio
import aiohttp
from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse
import argparse

# Директория для сохранения изображений
DOWNLOAD_DIR = "downloaded_images"

# Создаем директорию, если она не существует
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

# Предопределённый список URL-адресов
# URLS = [
#     "https://cdn.pixabay.com/photo/2023/10/26/04/52/old-8341706_640.jpg",
#     "https://cdn.pixabay.com/photo/2024/06/19/05/37/animal-8839173_640.jpg",
#     "https://cdn.pixabay.com/photo/2024/03/31/06/17/googles-8666108_640.jpg"
# ]

#Для запуска программы с передачей URL-адресов выполните следующую команду:
#py.exe sem4.py https://cdn.pixabay.com/photo/2023/10/26/04/52/old-8341706_640.jpg https://cdn.pixabay.com/photo/2024/06/19/05/37/animal-8839173_640.jpg https://cdn.pixabay.com/photo/2024/03/31/06/17/googles-8666108_640.jpg

def download_image(url):
    filename = os.path.basename(urlparse(url).path)
    file_path = os.path.join(DOWNLOAD_DIR, filename)

    async def download():
        start_time = time.time()
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    with open(file_path, 'wb') as f:
                        f.write(await response.read())
                    download_time = time.time() - start_time
                    print(f"Загружено: {filename}, Время: {download_time:.2f} секунд")
                else:
                    print(f"Ошибка загрузки: {filename}")

    asyncio.run(download())


def download_images(urls):
    """Функция для загрузки всех изображений из списка URL с использованием многопроцессорности."""
    start_time = time.time()

    print("Загрузка изображений используя многопроцессорность...")
    # Используем ProcessPoolExecutor для многопроцессорности
    with ProcessPoolExecutor() as executor:
        executor.map(download_image, urls)

    print("Загрузка изображений используя многопоточность...")
    # Используем ThreadPoolExecutor для многопоточности
    with ThreadPoolExecutor() as executor:
        executor.map(download_image, urls)

    total_time = time.time() - start_time
    print(f"Общее время загрузки: {total_time:.2f} секунд")


def main():
    # Инициализация парсера аргументов командной строки
    parser = argparse.ArgumentParser(
        description="Загрузчик изображений с использованием многопроцессорности и асинхронности.")

    # Добавление аргумента для передачи URL-адресов
    parser.add_argument(
        "urls",
        metavar="URL",
        type=str,
        nargs="+",
        help="Список URL-адресов изображений для загрузки."
    )

    # Парсинг аргументов
    args = parser.parse_args()

    # Запуск загрузки изображений
    print("Начинаем загрузку изображений...")
    download_images(args.urls)


if __name__ == '__main__':
    main()