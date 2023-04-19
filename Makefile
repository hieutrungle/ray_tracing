setup: requirements.txt
	pip install -r requirements.txt

test:
	behave

test_tuples:
	behave -i ./features/tuples.feature
	
test_canvas:
	behave -i ./features/canvas.feature

clean:
	rm -rf __pycache__

.PHONY: setup test clean
