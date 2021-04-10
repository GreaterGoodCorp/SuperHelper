venv:
	/usr/local/bin/python3 -m venv .venv
	./.venv/bin/pip3 install -y -r requirements.txt

build:
	./.venv/bin/python3 setup.py sdist bdist_wheel

publish: build
	./.venv/bin/twine check dist/* && twine upload dist/*

clean: dev-uninstall
	rm -rf build
	rm -rf dist
	rm -rf ~/Library/Application\ Support/SuperHelper/
	rm -rf ~/.config/SuperHelper
	rm -rf .pytest_cache
	find . -type d -name __pycache__ -exec rm -r {} \+

dev-uninstall:
	./.venv/bin/pip3 uninstall -y SuperHelper && rm -rf src/*.egg-info

dev-install:
	./.venv/bin/pip3 install -e .
