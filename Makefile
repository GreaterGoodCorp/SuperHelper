build:
	python3 setup.py sdist bdist_wheel

publish:
	twine check dist/* && twine upload dist/*

clean:
	find . -type d -name __pycache__ -exec rm -r {} \+
	find . -type d -name build -exec rm -r {} \+
	find . -type d -name dist -exec rm -r {} \+
	find . -type d -name *.egg-info -exec rm -r {} \+
