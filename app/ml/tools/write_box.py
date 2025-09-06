from typing import List
import cv2
import numpy as np


class BoxProcessor:
    """Класс для обработки и визуализации боксов с помощью OpenCV"""

    @staticmethod
    def draw_boxes(image: np.ndarray, boxes_info: List[dict],
                   blur_amount: int = 50, blur_type: str = "gaus") -> np.ndarray:
        """
        Применение размытия внутри бокса на изображении

        Args:
            image: Изображение в формате numpy array
            boxes_info: Информация о боксах
            blur_amount: Степень размытия от 1 до 100
            blur_type: Тип размытия: "gaus" или "pixelization"

        Returns:
            Изображение с размытыми боксами
        """
        result_image = image.copy()

        for box in boxes_info:
            x_min, y_min, x_max, y_max = box["coordinates"]

            # Вырезаем область бокса
            roi = result_image[y_min:y_max, x_min:x_max]

            if blur_type == "pixelization":
                # Пикселизация: уменьшаем размер и возвращаем обратно
                h, w = roi.shape[:2]
                # Чем выше blur_amount, тем сильнее уменьшение
                down_w = max(1, w // max(1, blur_amount))
                down_h = max(1, h // max(1, blur_amount))
                temp = cv2.resize(roi, (down_w, down_h), interpolation=cv2.INTER_LINEAR)
                blurred_roi = cv2.resize(temp, (w, h), interpolation=cv2.INTER_NEAREST)
            else:
                # Гауссово размытие
                k = max(1, int(blur_amount) * 2 + 1)  # ядро должно быть нечетным
                blurred_roi = cv2.GaussianBlur(roi, (k, k), 0)

            # Вставляем размытый бокс обратно в изображение
            result_image[y_min:y_max, x_min:x_max] = blurred_roi

        return result_image
    
    @staticmethod
    def filter_boxes_by_area(boxes_info: List[dict], min_area: int = 500) -> List[dict]:
        """
        Фильтрация боксов по минимальной площади
        
        Args:
            boxes_info: Информация о боксах
            min_area: Минимальная площадь бокса
            
        Returns:
            Отфильтрованный список боксов
        """
        filtered_boxes = []
        
        for box in boxes_info:
            x_min, y_min, x_max, y_max = box['coordinates']
            area = (x_max - x_min) * (y_max - y_min)
            
            if area >= min_area:
                box['area'] = area
                filtered_boxes.append(box)
        
        return filtered_boxes
    
    @staticmethod
    def filter_boxes_by_confidence(boxes_info: List[dict], min_confidence: float = 0.7) -> List[dict]:
        """
        Фильтрация боксов по уверенности
        
        Args:
            boxes_info: Информация о боксах
            min_confidence: Минимальная уверенность
            
        Returns:
            Отфильтрованный список боксов
        """
        return [box for box in boxes_info if box['confidence'] >= min_confidence]
