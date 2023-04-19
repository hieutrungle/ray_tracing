setup: requirements.txt
	pip install -r requirements.txt

test:
	behave

clean:
	rm -rf __pycache__

.PHONY: setup test clean
