install:
	@echo "--> Installing YSNP dependencies"
	pip install -r requirements.txt
	@echo ""


test:
	@echo "--> Running YSNP tests"
	flake8
	isort -c
	coverage run ysnp/manage.py test ysnp
	coverage report #--fail-under=100
	@echo ""

local-build:
	@echo "--> Building images"
	docker-compose -f local.yml build
	@echo ""

local-run:
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

prod-build:
	@echo "--> Building images"
	docker-compose -f production.yml build
	@echo ""

prod-run:
	@echo "--> Running production containers"
	docker-compose -f production.yml up -d
	@echo ""

prod-down:
	@echo "--> Stoping production containers"
	docker-compose -f production.yml down
	@echo ""

prod-logs:
	@echo "--> Showing production containers logs"
	docker-compose -f production.yml logs -f
	@echo ""

prod-deploy:
	@echo "--> Deploying"
	git pull
	docker-compose -f production.yml build
	docker-compose -f production.yml restart
	@echo ""

rmcontainers:
	@echo "--> WARNING: Stoping and removing containers"
	docker stop `docker ps -aq`
	docker rm `docker ps -aq`
	@echo ""
