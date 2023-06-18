SHELL = /bin/sh
DEVELOP_COMPOSE_FILE_PATH = "./docker/docker-compose.dev.yml"

# 🐳 Docker Compose
# up: CMD=up -d
up: CMD=up
down: CMD=down
backend_sh: CMD=exec backend sh
db_sh: CMD=exec db mysql -u root --password=root auctions 
logs: CMD=logs -f backend

up down sh backend_sh db_sh logs:
	docker-compose -f $(DEVELOP_COMPOSE_FILE_PATH) $(CMD)

.PHONY: linter_apply
linter_apply:
	docker-compose -f $(DEVELOP_COMPOSE_FILE_PATH) exec backend poetry run isort .
	docker-compose -f $(DEVELOP_COMPOSE_FILE_PATH) exec backend poetry run black .

.PHONY: linter_check
linter_check:
	docker-compose -f $(DEVELOP_COMPOSE_FILE_PATH) exec backend poetry run isort . --check
	docker-compose -f $(DEVELOP_COMPOSE_FILE_PATH) exec backend poetry run black . --check

.PHONY: tests
tests:
	docker-compose -f $(DEVELOP_COMPOSE_FILE_PATH) exec backend poetry run pytest --disable-pytest-warnings --durations=0 -vv tests

.PHONY: coverage
coverage:
	docker-compose -f $(DEVELOP_COMPOSE_FILE_PATH) exec backend coverage run --rcfile="../pyproject.toml" -m pytest --disable-pytest-warnings --durations=0 -vv tests
	docker-compose -f $(DEVELOP_COMPOSE_FILE_PATH) exec backend coverage report --rcfile="../pyproject.toml"

# install_from_sractch:

# onboard:

.PHONY: reboot
reboot: down
	-yes | docker image rm app_backend
	make up

.PHONY: prune
prune: down
	-yes | docker system prune -a
	-yes | docker volume rm $$(docker volume ls -q)
	make up