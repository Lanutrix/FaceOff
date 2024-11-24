from dataclasses import dataclass
from typing import Optional, Any

@dataclass
class ResponseData:
    filename: str
    content_length: int
    status: bool
    
    def __post_init__(self):
        # Дополнительная валидация при необходимости
        if self.content_length < 0:
            raise ValueError("content_length не может быть отрицательным")
        
@dataclass
class GetStatusFile:
    filename: str

@dataclass
class AnswerGetStatusFile:
    status: str
    added_time: float
    start_time: float
    end_time: Optional[float] = None
    error: Optional[str] = None
    result: Optional[Any] = None

if __name__ == "__main__":
    # Пример использования
    response = ResponseData(
        filename="example.txt",
        content_length=1024,
        status=True
    )
