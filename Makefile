venv:
	/usr/local/bin/python3 -m venv .venv
	./.venv/bin/pip3 install -r requirements.txt

build: venv
	./.venv/bin/python3 setup.py sdist bdist_wheel

publish: venv build
	./.venv/bin/twine check dist/* && twine upload dist/*

clean: venv
	./.venv/bin/pip3 uninstall -y SuperHelper && rm -rf src/*.egg-info
	rm -rf build
	rm -rf dist
	rm -rf ~/Library/Application\ Support/SuperHelper/
	rm -rf ~/.config/SuperHelper
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf .coverage.*
	find . -type d -name __pycache__ -exec rm -r {} \+

dev-install: venv
	./.venv/bin/pip3 install -e .

test: venv
	pytest --cov=src/SuperHelper
