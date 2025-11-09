# app/core/config.py

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Uygulama yapılandırmalarını .env dosyasından okuyan ana sınıf.
    """

    # --- Uygulama Ayarları ---
    APP_NAME: str = "ealabs-notes-backend"
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"

    # --- Veritabanı Ayarları ---
    # DATABASE_URL'yi .env dosyasından doğrudan okuyacak
    DATABASE_URL: str

    # --- Redis Ayarları ---
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0

    # --- S3 (MinIO) Ayarları ---
    S3_ENDPOINT_URL: str
    S3_ACCESS_KEY: str
    S3_SECRET_KEY: str
    S3_BUCKET_NAME: str

    # --- Güvenlik (JWT) Ayarları ---
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        # .env dosyasını oku
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


# Ayarları global olarak kullanılabilir tek bir instance (örnek) olarak oluştur
settings = Settings()
