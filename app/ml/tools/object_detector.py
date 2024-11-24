from app.ml.tools.model import Model
from app.ml.tools.write_box import BoxProcessor
from typing import List, Tuple, Optional, Union
import cv2
import numpy as np
import os
from moviepy.editor import VideoFileClip

class MLObjectDetector:
    """Главный класс модуля для детекции объектов в изображениях и видео"""

    def __init__(self, model_path: str = "yolov8n.pt", confidence_threshold: float = 0.5):
        self.yolo_processor = Model(model_path, confidence_threshold)
        self.box_processor = BoxProcessor()

    def initialize(self):
        """Инициализация модуля"""
        self.yolo_processor.load_model()

    def _get_output_filename(self, input_path: str) -> str:
        """Генерирует имя выходного файла с суффиксом _blur"""
        dir_name = os.path.dirname(input_path)
        base_name = os.path.basename(input_path)
        name, ext = os.path.splitext(base_name)
        output_name = f"{name}_blur{ext}"
        return os.path.join(dir_name, output_name)

    def detect_objects(self, image_source: Union[str, np.ndarray],
                      min_area: Optional[int] = None,
                      min_confidence: Optional[float] = None) -> Tuple[List[dict], np.ndarray]:
        """
        Полный цикл детекции объектов для изображений
        """
        # Загружаем изображение если это путь
        if isinstance(image_source, str):
            image = cv2.imread(image_source)
        else:
            image = image_source

        # Выполняем предсказание
        results = self.yolo_processor.predict(image_source)

        # Извлекаем информацию о боксах
        boxes_info = self.yolo_processor.extract_boxes(results)

        # Применяем фильтры если заданы
        if min_area is not None:
            boxes_info = self.box_processor.filter_boxes_by_area(boxes_info, min_area)

        if min_confidence is not None:
            boxes_info = self.box_processor.filter_boxes_by_confidence(boxes_info, min_confidence)

        # Рисуем боксы на изображении
        result_image = self.box_processor.draw_boxes(image, boxes_info)

        return boxes_info, result_image

    def process_image(self, image_path: str,
                     min_area: Optional[int] = None,
                     min_confidence: Optional[float] = None) -> str:
        """
        Обработка изображения с сохранением результата
        """
        boxes_info, result_image = self.detect_objects(
            image_path, min_area, min_confidence
        )
        
        output_path = self._get_output_filename(image_path)
        cv2.imwrite(output_path, result_image)
        
        print(f"Обработанное изображение сохранено: {output_path}")
        return output_path

    def process_video(self, video_path: str,
                     min_area: Optional[int] = None,
                     min_confidence: Optional[float] = None) -> str:
        """
        Обработка видео с сохранением результата и звука
        """
        print(f"Начинается обработка видео: {video_path}")
        
        # Открываем видео для чтения
        cap = cv2.VideoCapture(video_path)
        
        if not cap.isOpened():
            raise ValueError(f"Не удалось открыть видео файл: {video_path}")

        # Получаем параметры видео
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        # Создаем временный файл для видео без звука
        temp_output = self._get_output_filename(video_path).replace('.', '_temp.')
        
        # Настраиваем кодек для записи видео
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(temp_output, fourcc, fps, (width, height))

        frame_count = 0
        
        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Обрабатываем кадр
                boxes_info, processed_frame = self.detect_objects(
                    frame, min_area, min_confidence
                )
                
                # Записываем обработанный кадр
                out.write(processed_frame)
                
                frame_count += 1

        finally:
            cap.release()
            out.release()

        print(f"Видео обработано, добавляется звук...")
        
        # Добавляем звук к обработанному видео
        output_path = self._add_audio_to_video(video_path, temp_output)
        
        # Удаляем временный файл
        if os.path.exists(temp_output):
            os.remove(temp_output)
        
        print(f"Обработанное видео с звуком сохранено: {output_path}")
        return output_path

    def _add_audio_to_video(self, original_video_path: str, processed_video_path: str) -> str:
        """
        Добавляет звук из оригинального видео к обработанному
        """
        output_path = self._get_output_filename(original_video_path)
        
        try:
            # Загружаем оригинальное видео для извлечения аудио
            original_clip = VideoFileClip(original_video_path)
            
            # Загружаем обработанное видео
            processed_clip = VideoFileClip(processed_video_path)
            
            # Проверяем наличие аудио в оригинальном видео
            if original_clip.audio is not None:
                # Добавляем аудио к обработанному видео
                final_clip = processed_clip.set_audio(original_clip.audio)
            else:
                print("Оригинальное видео не содержит аудио")
                final_clip = processed_clip
            
            # Сохраняем результат
            final_clip.write_videofile(
                output_path, 
                codec='libx264',
                audio_codec='aac',
                temp_audiofile='{output_path}-temp-audio.m4a',
                remove_temp=True
            )
            
            # Освобождаем ресурсы
            original_clip.close()
            processed_clip.close()
            final_clip.close()
            
        except Exception as e:
            print(f"Ошибка при добавлении аудио: {e}")
            # Если не удалось добавить аудио, просто переименовываем файл
            os.rename(processed_video_path, output_path)
        
        return output_path

    def process_file(self, file_path: str,
                    min_area: Optional[int] = None,
                    min_confidence: Optional[float] = None) -> str:
        """
        Универсальный метод для обработки файлов (изображений или видео)
        """
        file_path = f"uploads/{file_path}"
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Файл не найден: {file_path}")
        
        # Определяем тип файла по расширению
        file_ext = os.path.splitext(file_path)[-1].lower()
        
        # Поддерживаемые форматы
        image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif'}
        video_extensions = {'.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv'}
        
        if file_ext in image_extensions:
            return self.process_image(file_path, min_area, min_confidence)
        elif file_ext in video_extensions:
            return self.process_video(file_path, min_area, min_confidence)
        else:
            raise ValueError(f"Неподдерживаемый формат файла: {file_ext}")
