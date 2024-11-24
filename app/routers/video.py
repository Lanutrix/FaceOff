import os
from pathlib import Path
from fastapi import APIRouter, Depends, UploadFile, HTTPException

from app.tools.generate_name_file import generate_name_file
from app.schemas import uploadfile
from app.ml.ml_executor import get_ml_executor, MLExecutor

router = APIRouter()

# Папка для сохранения файлов
UPLOAD_FOLDER = "uploads"

# Создаём папку, если её нет
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
SUPPORTED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'bmp', 'tiff', 'tif', 'mp4', 'avi', 'mov', 'mkv', 'wmv', 'flv'}


@router.post("/uploadfile", response_model=uploadfile.ResponseData)
async def create_upload_file(file: UploadFile, ml_executor: MLExecutor = Depends(get_ml_executor)):
    contents = await file.read()
    
    file_ext = file.filename.split('.')[-1].lower()
    file_name = generate_name_file(file.filename, file_ext)    
    
    # Поддерживаемые форматы
    if file_ext not in SUPPORTED_EXTENSIONS:
        raise HTTPException(
            status_code=400, 
            detail=f"Неподдерживаемый формат файла: {file_ext}"
        )

    # Сохранение файла на диск
    try:
        file_path = os.path.join(UPLOAD_FOLDER, file_name)
        with open(file_path, "wb") as f:
            f.write(contents)
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Ошибка при сохранении файла: {str(e)}"
        )
    
    # Обработка файла
    if not ml_executor.add_to_queue(file_name):
        raise HTTPException(
            status_code=500, 
            detail=f"Ошибка: невозможно добавить файл в очередь обработки"
        )

        
    
    return uploadfile.ResponseData(
        filename=file_name,
        content_length=len(contents),
        status=True
    )


@router.post("/check_status_file", response_model=uploadfile.AnswerGetStatusFile)
async def check_upload_file(file: uploadfile.GetStatusFile, ml_eecutor: MLExecutor = Depends(get_ml_executor)):
    filename = file.filename
    file_ext = filename.split('.')[-1].lower()
    # Поддерживаемые форматы

    if file_ext not in SUPPORTED_EXTENSIONS:
        raise HTTPException(status_code=500, detail=f"Ошибка в формате файла: расширение {file_ext} неподдерживается")

    
    # Обработка файла
    status_data = ml_eecutor.get_status(filename)

    if status_data is None:
        raise HTTPException(status_code=500, detail=f"Ошибка чтения из очереди: файл отсутствует")
   
    
    return uploadfile.AnswerGetStatusFile(**status_data)
