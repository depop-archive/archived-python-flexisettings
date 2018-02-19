.PHONY: pypi, tag

pypi:
	rm dist/*
	python setup.py sdist
	twine upload --config-file=.pypirc dist/*
	make tag

tag:
	git tag $$(python -c "from flexisettings.__about__ import __version__; print __version__")
	git push --tags
