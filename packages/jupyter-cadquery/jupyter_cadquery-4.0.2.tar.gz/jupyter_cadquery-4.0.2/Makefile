.PHONY: clean_notebooks wheel install tests check_version dist check_dist upload_test upload bump release create-release docker docker_upload

PYCACHE := $(shell find . -name '__pycache__')
EGGS := $(wildcard *.egg-info)
CURRENT_VERSION := $(shell awk '/current_version = / {print $$3}' pyproject.toml)

# https://github.com/jupyter/nbconvert/issues/637

JQ_RULES := '(.cells[] | select(has("outputs")) | .outputs) = [] \
| (.cells[] | select(has("execution_count")) | .execution_count) = null \
| .metadata = { \
	"language_info": {"name":"python", "pygments_lexer": "ipython3"}, \
	"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"} \
} \
| .cells[].metadata = {}'

clean_notebooks: ./examples/*.ipynb ./examples/assemblies/*.ipynb
	@for file in $^ ; do \
		echo "$${file}" ; \
		jq --indent 1 $(JQ_RULES) "$${file}" > "$${file}_clean"; \
		mv "$${file}_clean" "$${file}"; \
		python validate_nb.py "$${file}"; \
	done

clean: clean_notebooks
	@echo "=> Cleaning"
	@rm -fr build dist $(EGGS) $(PYCACHE)

prepare: clean
	git add .
	git status
	git commit -m "cleanup before release"

# Version commands

bump:
	@echo Current version: $(CURRENT_VERSION)
ifdef part
	bump-my-version bump $(part) --allow-dirty && grep current pyproject.toml
else ifdef version
	bump-my-version bump --allow-dirty --new-version $(version) && grep current pyproject.toml
else
	@echo "Provide part=major|minor|patch|release|build and optionally version=x.y.z..."
	exit 1
endif

# Dist commands

dist:
	@rm -f dist/*
	@python -m build 

release:
	git add .
	git status
	git diff-index --quiet HEAD || git commit -m "Latest release: $(CURRENT_VERSION)"
	git tag -a v$(CURRENT_VERSION) -m "Latest release: $(CURRENT_VERSION)"
	
create-release:
	@github-release release -u bernhard-42 -r jupyter-cadquery -t v$(CURRENT_VERSION) -n jupyter-cadquery-$(CURRENT_VERSION)
	@sleep 2
	@github-release upload  -u bernhard-42 -r jupyter-cadquery -t v$(CURRENT_VERSION) -n jupyter_cadquery-$(CURRENT_VERSION).tar.gz -f dist/jupyter_cadquery-$(CURRENT_VERSION).tar.gz
	@github-release upload  -u bernhard-42 -r jupyter-cadquery -t v$(CURRENT_VERSION) -n jupyter_cadquery-$(CURRENT_VERSION)-py3-none-any.whl -f dist/jupyter_cadquery-$(CURRENT_VERSION)-py3-none-any.whl

install: dist
	@echo "=> Installing jupyter_cadquery"
	@pip install --upgrade .

check_dist:
	@twine check dist/*

upload:
	@twine upload dist/*


docker:
	@rm -fr docker/examples
	@cp -R examples docker/
	@cp jupyter_cadquery/viewer/viewer.ipynb docker/
	@cd docker && docker build -t bwalter42/jupyter_cadquery:$(CURRENT_VERSION) .
	@rm -fr docker/examples
	@rm -fr docker/viewer.ipynb

upload_docker: 
	@docker push bwalter42/jupyter_cadquery:$(CURRENT_VERSION)
