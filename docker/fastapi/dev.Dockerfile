FROM python:3.11-slim

# Prevent creating pyc files
ENV PYTHONDONTWRITEBYTECODE=1 \
    # Prevent failing installing poetry
    CRYPTOGRAPHY_DONT_BUILD_RUST=1 \
    # Prevent buffering std out
    PYTHONUNBUFFERED=1

WORKDIR /app
COPY pyproject.toml poetry.lock /app/

RUN python3 -m pip install -U pip && pip3 install poetry==1.4.2 \
    && poetry config virtualenvs.create false || true \
	&& poetry install \
	&& mkdir /app/backend

ADD ./docker/docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod a+x /docker-entrypoint.sh
COPY ./backend /app/backend/

ENTRYPOINT ["sh", "/docker-entrypoint.sh"]