FROM python:3.11.9-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apk update && \
    apk add --no-cache postgresql-dev gcc python3-dev musl-dev libpq-dev nmap && \
    pip install --upgrade pip && \
    pip install poetry 


ADD pyproject.toml /app
RUN poetry config virtualenvs.create false && \
    poetry install --no-root --no-interaction --no-ansi 
    # poetry install --without dev --no-root --no-interaction --no-ansi 

COPY . /app/

RUN chmod +x /app/entrypoint.sh 

ENTRYPOINT ["/app/entrypoint.sh"]
