.ONESHELL:
ENV_PREFIX=$(shell python -c "if __import__('pathlib').Path('.venv/bin/pip').exists(): print('.venv/bin/')")
USING_POETRY=$(shell grep "tool.poetry" pyproject.toml && echo "yes")

.PHONY: help
help:             ## Show the help.
	@echo "Usage: make <target>"
	@echo ""
	@echo "Targets:"
	@fgrep "##" Makefile | fgrep -v fgrep


.PHONY: show
show:             ## Show the current environment.
	@echo "Current environment:"
	@if [ "$(USING_POETRY)" ]; then poetry env info && exit; fi
	@echo "Running using $(ENV_PREFIX)"
	@$(ENV_PREFIX)python -V
	@$(ENV_PREFIX)python -m site

.PHONY: install
install:          ## Install the project in dev mode.
	@if [ "$(USING_POETRY)" ]; then poetry install && exit; fi
	@echo "Don't forget to run 'make virtualenv' if you got errors."
	$(ENV_PREFIX)pip install -e .[test]

.PHONY: fmt
fmt:              ## Format code using black & isort.
	$(ENV_PREFIX)isort learn_raft/
	$(ENV_PREFIX)black -l 150 learn_raft/
	$(ENV_PREFIX)black -l 150 tests/

.PHONY: lint
lint:             ## Run pep8, black, mypy linters.
	$(ENV_PREFIX)flake8 learn_raft/
	$(ENV_PREFIX)black --check -l 150 learn_raft/
	$(ENV_PREFIX)black --check -l 150 tests/
	#$(ENV_PREFIX)mypy --ignore-missing-imports learn_raft/

.PHONY: test
test:         ## Run tests and generate coverage report.
	$(ENV_PREFIX)pytest -v --cov-config .coveragerc --cov=learn_raft -l --tb=short --maxfail=1 tests/
	$(ENV_PREFIX)coverage xml
	$(ENV_PREFIX)coverage html

.PHONY: watch
watch:            ## Run tests on every change.
	ls **/**.py | entr $(ENV_PREFIX)pytest -s -vvv -l --tb=long --maxfail=1 tests/

.PHONY: clean
clean:            ## Clean unused files.
	@find ./ -name '*.pyc' -exec rm -f {} \;
	@find ./ -name '__pycache__' -exec rm -rf {} \;
	@find ./ -name 'Thumbs.db' -exec rm -f {} \;
	@find ./ -name '*~' -exec rm -f {} \;
	@rm -rf .cache
	@rm -rf .pytest_cache
	@rm -rf .mypy_cache
	@rm -rf build
	@rm -rf dist
	@rm -rf *.egg-info
	@rm -rf htmlcov
	@rm -rf .tox/
	@rm -rf docs/_build

.PHONY: virtualenv
virtualenv:       ## Create a virtual environment.
	@if [ "$(USING_POETRY)" ]; then poetry install && exit; fi
	@echo "creating virtualenv ..."
	@rm -rf .venv
	@python3 -m venv .venv
	@./.venv/bin/pip install -U pip
	@./.venv/bin/pip install -e .[test]
	@echo
	@echo "!!! Please run 'source .venv/bin/activate' to enable the environment !!!"

.PHONY: release
release:          ## Create a new tag for release.
	@echo "WARNING: This operation will create s version tag and push to github"
	@read -p "Version? (provide the next x.y.z semver) : " TAG
	@echo "$${TAG}" > learn_raft/VERSION
	@$(ENV_PREFIX)gitchangelog > HISTORY.md
	@git add learn_raft/VERSION HISTORY.md
	@git commit -m "release: version $${TAG} 🚀"
	@echo "creating git tag : $${TAG}"
	@git tag $${TAG}
	@git push -u origin HEAD --tags
	@echo "Github Actions will detect the new tag and release the new version."

.PHONY: docs
docs:             ## Build the documentation.
	@echo "building documentation ..."
	@$(ENV_PREFIX)mkdocs build
	URL="site/index.html"; xdg-open $$URL || sensible-browser $$URL || x-www-browser $$URL || gnome-open $$URL

.PHONY: proto
proto:
	@echo "generating proto"
	@python -m grpc.tools.protoc \
				 -I=./learn_raft/protos \
				 --python_out=./learn_raft/stubs \
				 --grpc_python_out=./learn_raft/stubs \
				 learn_raft/protos/raft.proto learn_raft/protos/cluster_manager.proto
	@python -m grpc.tools.protoc \
				 -I=./learn_raft_kvstore/protos \
				 --python_out=./learn_raft_kvstore/stubs \
				 --grpc_python_out=./learn_raft_kvstore/stubs \
				 ./learn_raft_kvstore/protos/kvstore.proto

.PHONY: start_all
start_all:
	@echo "Starting all servers in config"
	@pip install -e .
	@learn_raft --config-file ./learn_raft_kvstore/config/conf.yaml start-cluster-manager --id 9999 --host 0.0.0.0 --port 9999
	#@learn_raft --config-file ./learn_raft_kvstore/config/conf.yaml start-raft-node --id 1 --host 0.0.0.0  --port 5090 --cluster-manager-ip 0.0.0.0:9999
	#@learn_raft start-kv-node --config ./learn_raft_kvstore/config/conf.yaml --id 8888 --host 0.0.0.0  --port 8888 --cluster_manager_ip 0.0.0.0:9999
#	@learn_raft start-raft-node --config ./learn_raft_kvstore/config/conf.yaml --id 2 --host 0.0.0.0  --port 5091 --cluster_manager_ip 0.0.0.0:9999 --state-dir /tmp/state1
#	@learn_raft start-raft-node --config ./learn_raft_kvstore/config/conf.yaml --id 3 --host 0.0.0.0  --port 5092 --cluster_manager_ip 0.0.0.0:9999 --state-dir /tmp/state1

.PHONY: start_cluster_manager
start_cluster_manager:
	@echo "Starting Cluster manager"
	@pip install -e .
	@learn_raft --config-file ./learn_raft_kvstore/config/conf.yaml start-cluster-manager --id 9999 --host 0.0.0.0 --port 9999
	#@learn_raft --config-file ./learn_raft_kvstore/config/conf.yaml start-raft-node --id 1 --host 0.0.0.0  --port 5090 --cluster-manager-ip 0.0.0.0:9999
	#@learn_raft start-kv-node --config ./learn_raft_kvstore/config/conf.yaml --id 8888 --host 0.0.0.0  --port 8888 --cluster_manager_ip 0.0.0.0:9999
#	@learn_raft start-raft-node --config ./learn_raft_kvstore/config/conf.yaml --id 2 --host 0.0.0.0  --port 5091 --cluster_manager_ip 0.0.0.0:9999 --state-dir /tmp/state1
#	@learn_raft start-raft-node --config ./learn_raft_kvstore/config/conf.yaml --id 3 --host 0.0.0.0  --port 5092 --cluster_manager_ip 0.0.0.0:9999 --state-dir /tmp/state1

#@learn_raft start-raft-node --config ./learn_raft_kvstore/config/conf.yaml --id 1 --host 0.0.0.0  --port 5090 --cluster_manager_ip 0.0.0.0:9999 --state-dir /tmp/state1

.PHONY: start_raft_node1
start_raft_node1:
	@echo "Starting Raft Node"
	@pip install -e .
	@learn_raft --config-file ./learn_raft_kvstore/config/conf.yaml start-raft-node --id 1 --host 0.0.0.0  --port 5090 --cluster-manager-ip 0.0.0.0:9999

.PHONY: start_raft_node2
start_raft_node2:
	@echo "Starting Raft Node"
	@pip install -e .
	@learn_raft --config-file ./learn_raft_kvstore/config/conf.yaml start-raft-node --id 2 --host 0.0.0.0  --port 5091 --cluster-manager-ip 0.0.0.0:9999