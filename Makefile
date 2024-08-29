DC = docker compose
EXEC = docker exec -it
DB_CONTAINER = postgres_db
APP_CONTAINER = main_app
ENV_FILE = --env-file .env

.PHONY: db
db:
	${DC} up ${DB_CONTAINER} -d

.PHONY: db-down
db-down:
	${DC} down ${DB_CONTAINER}

.PHONY: db-logs
db-logs:
	docker logs ${DB_CONTAINER} -f

.PHONY: app
app:
	${DC} up -d

.PHONY: app-down
app-down:
	${DC} down

.PHONY: app-logs
app-logs:
	docker logs ${APP_CONTAINER} -f

.PHONY: migrate 
migrate:
	${EXEC} ${APP_CONTAINER} python manage.py migrate

.PHONY: migrations
migrations:
	${EXEC} ${APP_CONTAINER} python manage.py makemigrations
