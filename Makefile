.PHONY: pypi, tag, mypy, pytest, test

pypi:
	rm -f dist/*
	python setup.py sdist
	twine upload --config-file=.pypirc dist/*
	make tag

tag:
	git tag $$(python -c "from flexisettings.__about__ import __version__; print(__version__)")
	git push --tags


mypy:
	PYTHONPATH=.:test_project:$$PYTHONPATH mypy --py2 --ignore-missing-imports flexisettings

pytest:
	PYTHONPATH=.:test_project:$$PYTHONPATH py.test -v -s --pdb test_project/tests/

test: mypy pytest
