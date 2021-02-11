install:
		poetry install
package-install:
		pip install --user dist/*.whl
package-uninstall:
		pip uninstall hexlet-code
build:
		poetry build
