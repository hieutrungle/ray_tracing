setup: requirements.txt
	pip install -r requirements.txt

test:
	behave

test_tuples:
	behave -i ./features/tuples.feature
	
test_canvas:
	behave -i ./features/canvas.feature

test_matrices:
	behave -i ./features/matrices.feature

test_trans:
	behave -i ./features/transformations.feature

test_rays:
	behave -i ./features/rays.feature

test_spheres:
	behave -i ./features/spheres.feature

test_intersections:
	behave -i ./features/intersections.feature

clean:
	rm -rf __pycache__

.PHONY: setup test clean
