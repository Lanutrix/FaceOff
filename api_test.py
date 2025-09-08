"""Helper script to exercise the processing API.

The script sends a few sample files to the running service and prints the
response.  When the service is not available the request library raises a
``RequestException`` which previously caused a noisy traceback.  To make quick
manual checks friendlier we catch these errors and display a concise message
instead of crashing.
"""

import argparse
import requests
import os


def send_file(url: str, file_path: str, blur_amount: int, blur_type: str) -> None:
    """Send a file to the API and print the result.

    Any :class:`requests.exceptions.RequestException` is caught so the script
    fails gracefully when the backend is not running or closes the connection.
    """
    try:
        if not os.path.exists(file_path):
            print(f"Файл не найден: {file_path}")
            return
            
        with open(file_path, 'rb') as f:
            files = {'file': f}
            data = {
                'blur_amount': blur_amount,
                'blur_type': blur_type
            }
            r = requests.post(url, files=files, data=data, timeout=30)
            print(f"Статус: {r.status_code}")
            if r.status_code == 200:
                print(f"Ответ: {r.json()}")
            else:
                print(f"Ошибка: {r.text}")
    except requests.exceptions.RequestException as exc:  # network related
        print(f"Ошибка запроса: {exc}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Send test requests to API")
    parser.add_argument(
        "--url",
        default="http://localhost:8000/api/uploadfile",
        help="API endpoint to use",
    )
    return parser.parse_args()


def run_face_test(url: str) -> None:
    """Тест с изображением лица"""
    print("=== Тест с изображением лица ===")
    file_path = "uploads/i.jpg"
    send_file(url, file_path, blur_amount=5, blur_type="gaus")


def run_car_test(url: str) -> None:
    """Тест с видео автомобиля"""
    print("=== Тест с видео автомобиля ===")
    file_path = "uploads/v.mp4"
    send_file(url, file_path, blur_amount=8, blur_type="pixelization")


def run_png_test(url: str) -> None:
    """Тест с PNG изображением"""
    print("=== Тест с PNG изображением ===")
    file_path = "uploads/p.jpg"  # Используем существующий файл
    send_file(url, file_path, blur_amount=3, blur_type="pixelization")


if __name__ == "__main__":
    args = parse_args()
    print(f"Тестируем API по адресу: {args.url}")
    print("Убедитесь, что сервер запущен командой: python -m uvicorn app.main:app --reload")
    print()
    
    run_face_test(args.url)
    print()
    run_car_test(args.url)
    print()
    run_png_test(args.url)