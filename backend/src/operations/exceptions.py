import logging
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError, DataError, OperationalError
from sqlalchemy.ext.asyncio import AsyncSession

# Настройка логгера
logger = logging.getLogger(__name__)

async def handle_error(session: AsyncSession, error: Exception):
    # Откатываем транзакцию
    await session.rollback()

    error_detail = {
        "status": "error",
        "description": {
            "error_message": str(error),
        }
    }

    # Обрабатываем специфичные типы ошибок
    if isinstance(error, IntegrityError):
        # Логируем ошибку IntegrityError
        logger.error("IntegrityError occurred: %s", str(error))
        error_detail["message"] = "Invalid data provided. This operation violates integrity constraints."
        raise HTTPException(status_code=400, detail=error_detail)
    elif isinstance(error, DataError):
        # Логируем ошибку DataError
        logger.error("DataError occurred: %s", str(error))
        error_detail["message"] = "Invalid data format or type provided."
        raise HTTPException(status_code=400, detail=error_detail)
    elif isinstance(error, OperationalError):
        # Логируем ошибку OperationalError
        logger.error("OperationalError occurred: %s", str(error))
        error_detail["message"] = "An operational error occurred while processing the request."
        raise HTTPException(status_code=500, detail=error_detail)
    else:
        # Логируем остальные ошибки как неожиданные
        logger.error("UnexpectedError occurred: %s", str(error))
        error_detail["message"] = "An unexpected error occurred during request processing."
        raise HTTPException(status_code=500, detail=error_detail)
