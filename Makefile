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

run:
	@echo "--> Running YSNP"
	python ysnp/manage.py runserver 0.0.0.0:8000
	@echo ""
