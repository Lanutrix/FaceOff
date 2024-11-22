import os
from pathlib import Path
from fastapi import APIRouter, Depends, UploadFile, HTTPException

from tools.generate_name_file import generate_name_file
from schemas import uploadfile

router = APIRouter()

# Папка для сохранения файлов
UPLOAD_FOLDER = "uploads"

# Создаём папку, если её нет
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@router.post("/uploadfile", response_model=uploadfile.ResponseData)
async def create_upload_file(file: UploadFile):
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
    
    return uploadfile.ResponseData(filename=file_name,
                                   content_length=len(contents),
                                   status=True)
