# app/core/logging.py

import logging
import json
import sys
from datetime import datetime
from app.core.config import settings # Ayarlarımızı import ediyoruz

class JsonFormatter(logging.Formatter):
    """
    Log kayıtlarını JSON formatına çeviren özel Formatter.
    """
    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            "timestamp": datetime.fromtimestamp(record.created).isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "funcName": record.funcName,
            "lineNo": record.lineno,
        }
        
        # Eğer bir hata (exception) varsa, onu da ekle
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
            
        return json.dumps(log_data)

def setup_logging():
    """
    Uygulama için loglamayı ayarlar.
    """
    # Zaten ayarlanmış olan varsayılan handler'ları (varsa) kaldır
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    # Yeni bir handler oluştur (logları terminale/stdout'a yazacak)
    stream_handler = logging.StreamHandler(sys.stdout)
    
    # Handler için JSON Formatter'ı ayarla
    stream_handler.setFormatter(JsonFormatter())

    # logging.root (ana logger) ayarla
    # LOG_LEVEL ayarını .env -> settings üzerinden al (AC'yi karşılıyor)
    logging.root.setLevel(settings.LOG_LEVEL)
    logging.root.addHandler(stream_handler)
    
    # Uvicorn ve FastAPI loglarının da bizim formatımızı kullanmasını sağla
    logging.getLogger("uvicorn").handlers = [stream_handler]
    logging.getLogger("uvicorn.access").handlers = [stream_handler]
    logging.getLogger("fastapi").handlers = [stream_handler]