build:
	./.venv/bin/python3 setup.py sdist bdist_wheel

publish: build
	./.venv/bin/twine check dist/* && twine upload dist/*

clean:
	rm -rf build
	rm -rf dist
	find . -type d -name __pycache__ -exec rm -r {} \+

dev-uninstall:
	./.venv/bin/pip3 uninstall SuperHelper && rm -rf src/*.egg-info

dev-install:
	./.venv/bin/pip3 install -e .
