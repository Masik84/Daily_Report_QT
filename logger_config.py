import logging
from logging.handlers import RotatingFileHandler
import os
import sys
from pathlib import Path

def setup_logging():
    """Настройка комплексной системы логирования с более детальными сообщениями"""
    try:
        # Создаем папку для логов рядом с исполняемым файлом
        log_dir = Path(__file__).parent / "logs"
        log_dir.mkdir(exist_ok=True)
        
        log_file = log_dir / "app.log"
        
        # Основной логгер приложения
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        
        # Очистка существующих обработчиков
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)
            handler.close()
        
        # Улучшенный формат логов
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(name)s - %(filename)s:%(lineno)d - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Файловый обработчик с ротацией
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=5*1024*1024,  # 5 MB
            backupCount=3,
            encoding='utf-8'
        )
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.DEBUG)
        
        # Консольный обработчик (только WARNING и выше)
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        console_handler.setLevel(logging.INFO)
        
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        logger.info("Логирование успешно настроено. Логи будут записываться в %s", log_file)
        logger.debug("Текущая рабочая директория: %s", os.getcwd())
        
        return logger
        
    except Exception as e:
        print(f"CRITICAL: Ошибка настройки логирования: {str(e)}")
        raise