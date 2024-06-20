build:
	docker compose build

build_no_cache:
	docker compose build --no-cache

start_db:
	docker compose up db -d

start_dev:
	docker compose up app -d

stop:
	docker compose down

initdb:
	python cli.py init-db

makemigrations:
	python cli.py make-migrations

migrate: 
	python cli.py migrate
