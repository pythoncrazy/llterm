all: clean build publish

build:
	python -m build

clean:
	rm -rf build dist llterm.egg-info

publish: build
	twine upload dist/*
