from ml.object_detector import MLObjectDetector
import cv2


# Инициализация детектора
detector = MLObjectDetector("models/yolov11m-face.pt", confidence_threshold=0.5)
detector.initialize()

# Универсальная обработка файла (автоматически определит тип)
output_path = detector.process_file(
    "video.MOV",  # или "img.jpg"
    min_area=500,
    min_confidence=0.7
)

print(f"Результат сохранен в: {output_path}")

