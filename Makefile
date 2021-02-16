install:
		poetry install
package-install:
		pip install dist/*.whl
package-uninstall:
		pip uninstall hexlet-code
build:
		poetry build
lint:
		poetry run flake8 page_loader tests
test: lint
		poetry run pytest tests
coverage:
		poetry run coverage run --source=page_loader -m pytest tests
		poetry run coverage xml
push: test
		git push

.PHONY: install, package-install, package-uninstall, lint, build
