# app/main.py

import logging
from fastapi import FastAPI
from starlette import status
from app.core.logging import setup_logging  # <-- YENİ İMPORT
from app.core.config import settings        # <-- YENİ İMPORT

# --- Loglamayı Ayarla ---
# FastAPI uygulamasını oluşturmadan HEMEN ÖNCE çağırıyoruz.
setup_logging()
# ------------------------

# Loglamanın çalıştığını test etmek için bir log mesajı
logging.info(f"Uygulama '{settings.APP_NAME}' olarak başlatılıyor...")
logging.debug("Bu bir DEBUG logudur, LOG_LEVEL=INFO ise görünmemeli.")

# FastAPI uygulamasını oluştur
app = FastAPI(
    title=settings.APP_NAME, # Ayarları config'den al
    description="EALabs Not Alma Uygulaması API",
    version="0.1.0",
    debug=settings.DEBUG,    # Debug modunu config'den al
)

@app.get(
    "/healthz",
    tags=["Health"],
    summary="Servisin ayakta olup olmadığını kontrol eder",
    status_code=status.HTTP_200_OK,
)
def health_check():
    """
    Basit sağlık kontrolü endpoint'i.
    Servis ayaktaysa 200 OK ve bir JSON mesajı döner.
    """
    logging.info("Health check endpoint'i çağrıldı.")
    return {"status": "OK"}