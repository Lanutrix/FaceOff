import os
from pathlib import Path
from fastapi import APIRouter, Depends, UploadFile, HTTPException

from app.tools.generate_name_file import generate_name_file
from app.schemas import uploadfile
from app.ml.ml_executor import get_ml_eecutor, MLExecutor

router = APIRouter()

# Папка для сохранения файлов
UPLOAD_FOLDER = "uploads"

# Создаём папку, если её нет
os.makedirs(UPLOAD_FOLDER, exist_ok=True)



@router.post("/uploadfile", response_model=uploadfile.ResponseData)
async def create_upload_file(file: UploadFile, ml_eecutor: MLExecutor = Depends(get_ml_eecutor)):
    contents = await file.read()

    file_ext = file.filename.split('.')[-1].lower()
    file_name = generate_name_file(file.filename, file_ext)    
    
    # Поддерживаемые форматы
    extensions = {'jpg', 'jpeg', 'png', 'bmp', 'tiff', 'tif', 'mp4', 'avi', 'mov', 'mkv', 'wmv', 'flv'}
    if file_ext not in extensions:
        raise HTTPException(status_code=500, detail=f"Ошибка в формате файла: расширение {file_ext} неподдерживается")

    # Сохранение файла на диск
    try:
        file_path = os.path.join(UPLOAD_FOLDER, file_name)
        with open(file_path, "wb") as f:
            f.write(contents)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при сохранении файла: {str(e)}")
    
    # Обработка файла
    try:
        if not ml_eecutor.add_to_queue(file_path):
            raise "невозможно записать в очередь"
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при добавлении файла в очередь: {str(e)}")
    
    return uploadfile.ResponseData(filename=file_name,
                                   content_length=len(contents),
                                   status=True)
