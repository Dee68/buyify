# Makefile for Buyify Docker setup

# =====================
# Default target
# =====================
.PHONY: help
help:
	@echo "Available commands:"
	@echo "  make build           Build Docker images without cache"
	@echo "  make up              Start dev containers (build first if needed)"
	@echo "  make down            Stop dev containers and remove volumes"
	@echo "  make migrate         Run Django migrations"
	@echo "  make makemigrations  Run Django makemigrations"
	@echo "  make shell           Open Django shell in web container"
	@echo "  make logs            View dev container logs"
	@echo "  make clean           Remove orphan containers and volumes"
	@echo "  make prod-build      Build production Docker images"
	@echo "  make prod-up         Start production containers"
	@echo "  make prod-down       Stop production containers and remove volumes"
	@echo "  make prod-deploy     Build, migrate, collect static, and start prod containers"

# =====================
# Development commands
# =====================
.PHONY: build
build:
	docker compose build --no-cache

.PHONY: up
up:
	docker compose up --remove-orphans

.PHONY: down
down:
	docker compose down -v

.PHONY: migrate
migrate:
	docker compose run --rm web python manage.py migrate

.PHONY: makemigrations
makemigrations:
	docker compose run --rm web python manage.py makemigrations

.PHONY: shell
shell:
	docker compose run --rm web python manage.py shell

.PHONY: logs
logs:
	docker compose logs -f

.PHONY: clean
clean:
	docker compose down --remove-orphans -v

# =========================
# Testing

.PHONY: test
test:
	docker compose run --rm web pytest -q


# =====================
# Production commands
# =====================
.PHONY: prod-build
prod-build:
	docker compose -f docker-compose.prod.yml build --no-cache

.PHONY: prod-up
prod-up:
	docker compose -f docker-compose.prod.yml up --remove-orphans -d

.PHONY: prod-down
prod-down:
	docker compose -f docker-compose.prod.yml down -v

# One-command deployment for production
.PHONY: prod-deploy
prod-deploy:
	docker compose -f docker-compose.prod.yml build --no-cache
	docker compose -f docker-compose.prod.yml run --rm web python manage.py migrate
	docker compose -f docker-compose.prod.yml run --rm web python manage.py collectstatic --noinput
	docker compose -f docker-compose.prod.yml up --remove-orphans -d
