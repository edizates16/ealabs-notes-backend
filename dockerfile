# 1. Adım: Temel Python imajını seç
# 'slim' versiyonu, gereksiz araçlar olmadan daha küçük bir imaj sağlar
FROM python:3.11-slim

# 2. Adım: Çalışma Dizinini Ayarla
# Konteyner içindeki tüm komutlar bu dizinden çalışacak
WORKDIR /app

# 3. Adım: Ortam Değişkenleri
# Python'un .pyc dosyaları oluşturmasını engeller ve logları anında yazdırır
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 4. Adım: Bağımlılıkları Kur
# Önce sadece bağımlılık dosyasını kopyala ki, kod değiştiğinde
# kütüphaneleri tekrar tekrar indirmek zorunda kalmayalım (Docker cache)
COPY pyproject.toml .

# 5. Adım: Bağımlılıkları kur
# Sanal ortam (venv) kullanmıyoruz çünkü konteynerin kendisi zaten izole bir ortam.
# Geliştirme (dev) araçlarını da kuruyoruz.
RUN pip install --no-cache-dir --upgrade pip \
    && pip install -e ".[dev]"

# 6. Adım: Uygulama Kodunu Kopyala
# 'app' klasörümüzü konteynerdeki /app/app dizinine kopyala
COPY ./app /app/app

# 7. Adım: Çalıştırma Komutu
# Konteyner başladığında Uvicorn sunucusunu başlat.
# --host 0.0.0.0: Konteynerin dışından (yani Docker host'tan) erişime izin ver.
# --port 8000: 8000 portunu dinle.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]