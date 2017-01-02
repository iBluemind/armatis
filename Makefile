.PHONY: all test clean ready rst docs

all:
	@echo 'test           Run the unit test codes'
	@echo 'ready          Make sure to ready to commit'
	@echo 'clean          Remove the useless files'
	@echo 'rst            Make the rst file from markdown file'
	@echo 'dist           Distribution on PyPI'
	@echo 'docs           Generate latest documentation'

test:
	@python setup.py test

clean:
	@rm -f armatis/*.pyc

rst:
	@pandoc --from=markdown --to=rst --output=README.rst README.md

ready: clean test

dist:
	@python setup.py egg_info sdist bdist_wheel
	@twine upload dist/*

docs:
	$(MAKE) -C docs pickle 
	$(MAKE) -C docs changes
	$(MAKE) -C docs html
