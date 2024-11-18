EXEC = docker exec -it
DB_CONTAINER = postgres_db
APP_CONTAINER = main_app
ENV_FILE = --env-file .env
MONITAORING_FILE = monitoring.yaml

.PHONY: db
db:
	docker compose up ${DB_CONTAINER} -d

.PHONY: db-down
db-down:
	docker compose down ${DB_CONTAINER}

.PHONY: postgres
postgres:
	${EXEC} ${DB_CONTAINER} psql -U postgres_user -d reviews_db -p 5432

.PHONY: db-logs
db-logs:
	docker logs ${DB_CONTAINER} -f

.PHONY: app
app:
	docker compose up -d --build

.PHONY: app-without-elastic
app-without-elastic:
	docker compose up ${APP_CONTAINER} ${DB_CONTAINER} -d --build

.PHONY: app-down
app-down:
	docker compose down

.PHONY: logs
logs:
	docker logs ${APP_CONTAINER} -f


.PHONY: migrate 
migrate:
	${EXEC} ${APP_CONTAINER} python manage.py migrate

.PHONY: migrations
migrations:
	${EXEC} ${APP_CONTAINER} python manage.py makemigrations

.PHONY: test
test:
	${EXEC} ${APP_CONTAINER} pytest

.PHONY: sync
sync:
	${EXEC} ${APP_CONTAINER} python3 manage.py upsert_title_search
