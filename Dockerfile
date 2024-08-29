FROM python:3.11.9-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apk update && \
    apk add --no-cache postgresql-dev gcc python3-dev musl-dev \
    libpq-dev nmap 

ADD pyproject.toml /app

RUN pip install --upgrade pip 
RUN pip install poetry 

RUN poetry config virtualenvs.create false 
RUN poetry install --no-root --no-interaction --no-ansi 

COPY . /app/

ENTRYPOINT ["/app/entrypoint.sh"]
