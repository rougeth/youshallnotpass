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


build-local:
	@echo "--> Building images"
	docker-compose -f local.yml build
	@echo ""


run-local:
	@echo "--> Running local containers"
	docker-compose -f local.yml up -d
	@echo ""

stop-local:
	@echo "--> Stop local containers"
	docker-compose -f local.yml stop
	@echo ""
