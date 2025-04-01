MAKEFLAGS += --warn-undefined-variables
SHELL := /bin/bash
.SHELLFLAGS := -eu -o pipefail -c
.DEFAULT_GOAL := help

# all targets are phony
.PHONY: $(shell egrep -o ^[a-zA-Z_-]+: $(MAKEFILE_LIST) | sed 's/://')

DEVELOP_COMPOSE = docker-compose -f dev.yml

build: ## executes "docker-compose build"
	@$(DEVELOP_COMPOSE) build

start: ## executes "docker-compose up"
	@$(DEVELOP_COMPOSE) up

stop: ## executes "docker-compose down"
	@$(DEVELOP_COMPOSE) down

logs: ## executes "docker-compose logs -f web"
	@$(DEVELOP_COMPOSE) logs -f web

status: ## executes "docker-compose ps"
	@$(DEVELOP_COMPOSE) ps

restart: stop ## executes stop and start
	@make start

COMPOSE_DJANGO = $(DEVELOP_COMPOSE) run --rm -u `id -u` web

run: guard-cmd ## run command on django container
	@$(COMPOSE_DJANGO) $(cmd)

pre-commit-install: ## Install pre-commit hooks
	pre-commit install

pre-commit: ## Run pre-commit
	pre-commit run --all-files

copy-env: ## Create .env file from .env.example
	cp .env.example .env

add-sample-data: ## Run the script to add sample data
	@$(COMPOSE_DJANGO) python manage.py shell -c "exec(open('scripts/add_sample_data.py').read())"

add-user: ## Run the script to add sample data
	@$(COMPOSE_DJANGO) python manage.py shell -c "exec(open('scripts/add_new_user_with_my_sha256.py').read())"

reset-data: ## Run the script to reset data
	@$(COMPOSE_DJANGO) python manage.py shell -c "exec(open('scripts/reset_data.py').read())"

guard-%:
	@if [ "${${*}}" = "" ]; then \
		echo "Environment variable $* not set"; \
		exit 1; \
	fi

help: ## Print this help
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)
