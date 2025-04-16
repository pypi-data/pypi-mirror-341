SHELL := /bin/bash
.SHELLFLAGS := -ec

.PHONY: publish-test publish-prod package-inspect-test package-inspect-prod package-run-test package-run-prod

VERSION := $(shell date +%Y.%m.%d.%H%M%S)

version-bump:
	sed -i "s/VERSION = \"[^\"]*\"/VERSION = \"$(VERSION)\"/" mcp_alchemy/server.py
	sed -i "s/version = \"[^\"]*\"/version = \"$(VERSION)\"/" pyproject.toml
	sed -i "s/mcp-alchemy==[0-9.]*\"/mcp-alchemy==$(VERSION)\"/g" README.md ~/.config/Claude/claude_desktop_config.json

publish-test:
	rm -rf dist/*
	$(MAKE) version-bump
	uv build
	uv publish --token "$$PYPI_TOKEN_TEST" --publish-url https://test.pypi.org/legacy/
	git checkout README.md pyproject.toml

publish-prod:
	rm -rf dist/*
	$(MAKE) version-bump
	uv build
	uv lock
	uv publish --token "$$PYPI_TOKEN_PROD"
	git commit -am "Published version $(VERSION) to PyPI"
	git push

package-inspect-test:
	rm -rf /tmp/test-mcp-alchemy
	uv venv /tmp/test-mcp-alchemy --python 3.12
	source /tmp/test-mcp-alchemy/bin/activate && uv pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ mcp-alchemy
	tree /tmp/test-mcp-alchemy/lib/python3.12/site-packages/mcp_alchemy
	source /tmp/test-mcp-alchemy/bin/activate && which mcp-alchemy

package-inspect-prod:
	rm -rf /tmp/test-mcp-alchemy
	uv venv /tmp/test-mcp-alchemy --python 3.12
	source /tmp/test-mcp-alchemy/bin/activate && uv pip install mcp-alchemy
	tree /tmp/test-mcp-alchemy/lib/python3.12/site-packages/mcp_alchemy
	source /tmp/test-mcp-alchemy/bin/activate && which mcp-alchemy

package-run-test:
	uvx --default-index https://test.pypi.org/simple/ --index https://pypi.org/simple/ --from mcp-alchemy mcp-alchemy

package-run-prod:
	uvx --from mcp-alchemy mcp-alchemy
