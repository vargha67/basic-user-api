install:
	pip install --upgrade pip && \
	pip install -r requirements.txt

lint: 
	pylint --disable=R,C,E1101 ./app

test: 
	python -m pytest -vv ./app/tests

run: 
	python ./app/run.py
	
all: install lint test run