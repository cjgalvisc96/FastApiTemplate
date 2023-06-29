SHELL = /bin/sh
DEVELOP_COMPOSE_FILE_PATH = "./docker/docker-compose.dev.yml"

# 🐳 Docker Compose
up: CMD=up -d
down: CMD=down
backend_sh: CMD=exec backend sh
db_sh: CMD=exec db mysql --user=root --password=root app_database 
test_db_sh: CMD=exec db mysql --user=root --password=root test_app_database 
test: CMD=run --rm backend poetry run pytest --disable-pytest-warnings --durations=0 -vv tests/
# test: CMD=run --rm backend poetry run pytest --disable-pytest-warnings --durations=0 -vv tests/unit/users/
# test: CMD=run --rm backend poetry run pytest --disable-pytest-warnings --durations=0 -vv tests/integration

.PHONY: up down backend_sh db_sh test_db_sh test
up down backend_sh db_sh test_db_sh test:
	docker-compose -f $(DEVELOP_COMPOSE_FILE_PATH) $(CMD)

.PHONY: linter_apply
linter_apply:
	docker-compose -f $(DEVELOP_COMPOSE_FILE_PATH) exec backend poetry run isort .
	docker-compose -f $(DEVELOP_COMPOSE_FILE_PATH) exec backend poetry run black .

.PHONY: linter_check
linter_check:
	docker-compose -f $(DEVELOP_COMPOSE_FILE_PATH) exec backend poetry run isort . --check
	docker-compose -f $(DEVELOP_COMPOSE_FILE_PATH) exec backend poetry run black . --check

.PHONY: coverage
coverage:
	docker-compose -f $(DEVELOP_COMPOSE_FILE_PATH) exec backend coverage run --rcfile="./pyproject.toml" -m pytest --disable-pytest-warnings --durations=0 -vv tests
	docker-compose -f $(DEVELOP_COMPOSE_FILE_PATH) exec backend coverage report --rcfile="./pyproject.toml"

# onboard:

.PHONY: reboot
reboot: down
	-yes | docker image rm app_backend app_celery_worker app_celery_beat
	make up

.PHONY: install_from_scratch
install_from_scratch: down
	sudo rm -rf docker/localstack_data
	-sudo rm celerybeat-schedule
	-yes | docker system prune -a
	-yes | docker volume rm $$(docker volume ls -q)
	make up

.PHONY: logs
logs: 
	docker logs app_backend -f