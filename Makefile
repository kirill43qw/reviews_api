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

.PHONY: app-slim
app-slim:
	docker compose up ${APP_CONTAINER} ${DB_CONTAINER} -d --build

.PHONY: app-down
app-down:
	docker compose down

.PHONY: app-logs
app-logs:
	docker logs ${APP_CONTAINER} -f

# .PHONY: monitoring
# monitoring:
# 	docker compose -f ${MONITAORING_FILE} up -d
#
# .PHONY: monitoring-logs
# monitoring-logs:
# 	docker compose -f ${MONITORING_FILE} ${ENV} logs -f

.PHONY: migrate 
migrate:
	${EXEC} ${APP_CONTAINER} python manage.py migrate

.PHONY: migrations
migrations:
	${EXEC} ${APP_CONTAINER} python manage.py makemigrations
