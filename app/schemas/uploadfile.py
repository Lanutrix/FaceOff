from dataclasses import dataclass

@dataclass
class ResponseData:
    filename: str
    content_length: int
    status: bool
    
    def __post_init__(self):
        # Дополнительная валидация при необходимости
        if self.content_length < 0:
            raise ValueError("content_length не может быть отрицательным")

if __name__ == "__main__":
    # Пример использования
    response = ResponseData(
        filename="example.txt",
        content_length=1024,
        status=True
    )
