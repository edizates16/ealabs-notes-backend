#!/bin/bash
# create-buckets.sh

# MinIO'nun ayağa kalkmasını bekleyen basit bir döngü (robust yöntem)
echo "MinIO'nun hazır olması bekleniyor..."
until mc alias set myminio $S3_ENDPOINT_URL $S3_ACCESS_KEY $S3_SECRET_KEY; do
    echo "MinIO'ya bağlanılamadı, 5 saniye sonra tekrar denenecek..."
    sleep 5
done

echo "MinIO bağlantısı başarılı."

# Bucket'ın var olup olmadığını kontrol et
if ! mc ls myminio | grep -q $S3_BUCKET_NAME; then
  echo "'$S3_BUCKET_NAME' bucket'ı oluşturuluyor..."
  mc mb myminio/$S3_BUCKET_NAME
  
  # Bucket'ı public (herkese açık) yap (opsiyonel, ama genelde istenir)
  mc policy set public myminio/$S3_BUCKET_NAME
  echo "'$S3_BUCKET_NAME' bucket'ı başarıyla oluşturuldu ve public yapıldı."
else
  echo "'$S3_BUCKET_NAME' bucket'ı zaten mevcut."
fi