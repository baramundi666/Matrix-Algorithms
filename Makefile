install:
	@echo "Installing dependencies"
	pip3 install -r requirements.txt

test:
	@echo "Running tests"
	python3 -m tests