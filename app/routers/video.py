import os
import time

from fastapi import APIRouter

from app.schemas.uploadfile import (
    ProcessRequest,
    ProcessResponse,
    SuccessResponse,
    ErrorResponse,
)
from app.ml.tools.object_detector import MLObjectDetector


router = APIRouter()

detector = MLObjectDetector()
try:
    detector.initialize()
except Exception:
    pass


@router.post("/process", response_model=ProcessResponse)
async def process_file(request: ProcessRequest) -> ProcessResponse:
    start = time.time()
    try:
        processed_path = detector.process_file(
            request.file_path,
            request.options.object_types,
            request.options.intensity,
            request.options.blur_type,
        )
        processed_size = os.path.getsize(processed_path)
        processing_time_ms = int((time.time() - start) * 1000)
        return SuccessResponse(
            success=True,
            processed_path=processed_path,
            processed_size=processed_size,
            processing_time_ms=processing_time_ms,
        )
    except Exception as e:
        return ErrorResponse(success=False, error_message=str(e))

