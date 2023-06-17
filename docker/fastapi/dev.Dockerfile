# FROM python:3.10-alpine3.18
FROM python:3.11-alpine3.18

# Prevent creating pyc files
ENV PYTHONDONTWRITEBYTECODE=1 \
    # Prevent failing installing poetry
    CRYPTOGRAPHY_DONT_BUILD_RUST=1 \
    # Prevent buffering std out
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=${PYTHONPATH}:${PWD} 

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

ADD ./docker/docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod a+x /docker-entrypoint.sh

RUN mkdir /app/backend
COPY ./backend /app/backend/

# ENTRYPOINT ["sh", "/docker-entrypoint.sh"]