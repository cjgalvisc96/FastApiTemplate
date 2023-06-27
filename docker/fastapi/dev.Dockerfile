FROM python:3.11-alpine3.18

# Prevent creating pyc files
ENV PYTHONDONTWRITEBYTECODE=1 \
    # Prevent failing installing poetry
    CRYPTOGRAPHY_DONT_BUILD_RUST=1 \
    # Prevent buffering std out
    PYTHONUNBUFFERED=1 \
    # Owners
    PYTHONPATH=${PYTHONPATH}:${PWD} \
    HOST=0.0.0.0 \
    PORT=8000

WORKDIR /app

# Dependencies
RUN apk add --no-cache \
    build-base \
    mysql-dev


# COPY pyproject.toml poetry.lock /app/
# RUN python3 -m pip install -U pip && pip3 install poetry==1.4.2 \
#     && poetry config virtualenvs.create false || true \
# 	&& poetry install

# TODO: ==Temporary
COPY requirements.txt /app/  
RUN pip install -r requirements.txt
# TODO: Temporary==

RUN mkdir /app/backend
COPY ./backend /app/backend/

CMD uvicorn backend.app:app --host ${HOST} --port ${PORT} --reload