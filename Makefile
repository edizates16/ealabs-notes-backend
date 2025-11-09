# Makefile

# -----------------------------------------------------------------------------
# Renk kodları (opsiyonel)
# -----------------------------------------------------------------------------
GREEN=\033[0;32m
YELLOW=\033[0;33m
RESET=\033[0m

# -----------------------------------------------------------------------------
# Docker Compose komutunu otomatik tespit et (v1: docker-compose, v2: docker compose)
# -----------------------------------------------------------------------------
COMPOSE := $(shell if command -v docker-compose >/dev/null 2>&1; then echo docker-compose; else echo docker compose; fi)

.PHONY: up down logs logs-api test format ps restart rebuild build prune help

## -----------------------------------------------------------------------------
## Docker Compose Komutları
## -----------------------------------------------------------------------------

up:
	@echo "$(GREEN)Tüm servisler ayağa kaldırılıyor (detached mode)...$(RESET)"
	$(COMPOSE) up -d --build

down:
	@echo "$(YELLOW)Tüm servisler durduruluyor ve kaldırılıyor...$(RESET)"
	$(COMPOSE) down

logs:
	@echo "$(GREEN)Tüm servislerin logları gösteriliyor...$(RESET)"
	$(COMPOSE) logs -f

logs-api:
	@echo "$(GREEN)Sadece 'api' servisinin logları gösteriliyor...$(RESET)"
	$(COMPOSE) logs -f api

ps:
	@echo "$(GREEN)Servis durumları listeleniyor...$(RESET)"
	$(COMPOSE) ps

restart:
	@echo "$(YELLOW)Servisler yeniden başlatılıyor...$(RESET)"
	$(COMPOSE) down
	$(COMPOSE) up -d --build

rebuild:
	@echo "$(YELLOW)İmajlar no-cache ile yeniden inşa ediliyor...$(RESET)"
	$(COMPOSE) build --no-cache
	$(COMPOSE) up -d

build:
	@echo "$(YELLOW)İmajlar inşa ediliyor...$(RESET)"
	$(COMPOSE) build

prune:
	@echo "$(YELLOW)Kullanılmayan imajlar/volumeler temizleniyor (dikkat)!$(RESET)"
	-docker image prune -f
	-docker volume prune -f

## -----------------------------------------------------------------------------
## Proje Test ve Formatlama Komutları
## -----------------------------------------------------------------------------

test:
	@echo "$(GREEN)'api' konteyneri içinde pytest çalıştırılıyor...$(RESET)"
	$(COMPOSE) exec api pytest -q tests/

format:
	@echo "$(YELLOW)'api' konteyneri içinde Ruff (format + lint) çalıştırılıyor...$(RESET)"
	docker-compose exec api ruff format .
	docker-compose exec api ruff check . --fix

## -----------------------------------------------------------------------------
## Yardım
## -----------------------------------------------------------------------------

help:
	@echo "$(GREEN)Kullanılabilir hedefler:$(RESET)"
	@echo "  up         - Servisleri detached modda ayağa kaldır"
	@echo "  down       - Tüm servisleri durdur ve kaldır"
	@echo "  logs       - Tüm servislerin loglarını takip et"
	@echo "  logs-api   - Sadece 'api' servisinin loglarını takip et"
	@echo "  ps         - Servis durumlarını listele"
	@echo "  restart    - Servisleri yeniden başlat (build ile)"
	@echo "  build      - İmajları inşa et"
	@echo "  rebuild    - No-cache ile yeniden inşa et ve ayağa kaldır"
	@echo "  prune      - Kullanılmayan imaj/volume temizliği"
	@echo "  test       - 'api' konteyneri içinde pytest çalıştır"
	@echo "  format     - Ruff ile format + otomatik düzeltme"