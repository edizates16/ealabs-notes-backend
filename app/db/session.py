# app/db/session.py

import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool

# .env dosyasından DATABASE_URL'yi al
DATABASE_URL = os.environ.get("DATABASE_URL")

if DATABASE_URL is None:
    raise ValueError("DATABASE_URL ortam değişkeni ayarlanmamış!")

# Asenkron veritabanı motoru oluştur
# pool_pre_ping=True: Bağlantıyı kullanmadan önce "canlı" olup olmadığını kontrol eder.
# NullPool: Asenkron ortamda ve sunucusuz (serverless) senaryolarda bazen 
# SQLAlchemy'nin varsayılan bağlantı havuzu (QueuePool) yerine bu tercih edilir.
# Geliştirme için şimdilik bu daha basit olabilir.
async_engine = create_async_engine(DATABASE_URL, pool_pre_ping=True, poolclass=NullPool)

# Veritabanı oturumları oluşturmak için bir fabrika (session factory)
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    autoflush=False,
    expire_on_commit=False, # Veri çekildikten sonra session kapansa bile objeleri kullanmamızı sağlar
)