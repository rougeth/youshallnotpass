local-build:
	@echo "--> Building images"
	docker-compose -f local.yml build
	@echo ""

local-up:
	@echo "--> Running local containers"
	docker-compose -f local.yml up -d
	@echo ""

local-down:
	@echo "--> Stoping local containers"
	docker-compose -f local.yml down
	@echo ""

local-logs:
	@echo "--> Showing local containers logs"
	docker-compose -f local.yml logs -f
	@echo ""

build:
	@echo "--> Building images"
	docker-compose -f production.yml build
	@echo ""

up:
	@echo "--> Running production containers"
	docker-compose -f production.yml up -d
	@echo ""

down:
	@echo "--> Stoping production containers"
	docker-compose -f production.yml down
	@echo ""

logs:
	@echo "--> Showing production containers logs"
	docker-compose -f production.yml logs -f
	@echo ""

deploy:
	@echo "--> Deploying"
	git pull
	docker-compose -f production.yml build
	docker-compose -f production.yml up -d
	@echo ""

deploy-django:
	@echo "--> Deploying Django"
	git pull
	docker-compose -f production.yml build django celeryworker
	docker-compose -f production.yml up -d django celeryworker
	@echo ""
