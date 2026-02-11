set windows-shell := ["powershell.exe", "-NoLogo", "-Command"]
set unstable := true
set script-interpreter := ['uv', 'run', '--script']

export PYTHONPATH := source_directory()
export DJANGO_SETTINGS_MODULE := "tests.settings"

[private]
default:
    @just --list --list-submodules

# run the django admin
[script]
manage *COMMAND:
    import os
    import sys
    from django.core import management
    os.environ["DJANGO_SETTINGS_MODULE"] = "tests.settings"
    management.execute_from_command_line(sys.argv + "{{ COMMAND }}".split(" "))

# install the uv package manager
[linux]
[macos]
install_uv:
    curl -LsSf https://astral.sh/uv/install.sh | sh

# install the uv package manager
[windows]
install_uv:
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# setup the venv, pre-commit hooks
setup python="python":
    uv venv -p {{ python }}
    @just install-precommit

# install git pre-commit hooks
install-precommit:
    @just run --no-default-groups --group precommit --exact --isolated pre-commit install

# update and install development dependencies
install *OPTS="--all-extras":
    @just install-precommit
    uv sync {{ OPTS }}

_install-docs:
    uv sync --no-default-groups --group docs --all-extras

# run the development server
runserver:
    @just manage makemigrations
    @just manage migrate
    @just manage runserver 8027

[script]
_lock-python:
    import tomlkit
    import sys
    f='pyproject.toml'
    d=tomlkit.parse(open(f).read())
    d['project']['requires-python']='=={}'.format(sys.version.split()[0])
    open(f,'w').write(tomlkit.dumps(d))

# lock to specific python and versions of given dependencies
test-lock +PACKAGES: _lock-python
    uv add --no-sync {{ PACKAGES }}
    uv sync --reinstall --no-default-groups --no-install-project

# run static type checking with mypy
check-types-mypy *RUN_ARGS:
    @just run --no-default-groups --all-extras --group typing {{ RUN_ARGS }} mypy

# run static type checking with pyright
check-types-pyright *RUN_ARGS:
    @just run --no-default-groups --all-extras --group typing {{ RUN_ARGS }} pyright

# run all static type checking
check-types: check-types-mypy check-types-pyright

# run all static type checking in an isolated environment
check-types-isolated:
    @just check-types-mypy --exact --isolated
    @just check-types-pyright --exact --isolated

# run package checks
check-package:
    uv pip check

# remove doc build artifacts
[script]
clean-docs:
    import shutil
    shutil.rmtree('./doc/build', ignore_errors=True)

# remove the virtual environment
[script]
clean-env:
    import shutil
    import sys
    shutil.rmtree(".venv", ignore_errors=True)

# remove all git ignored files
clean-git-ignored:
    git clean -fdX

# remove all non repository artifacts
clean: clean-docs clean-env clean-git-ignored

# build html documentation
build-docs-html: _install-docs
    @just run sphinx-build --fresh-env --builder html --doctree-dir ./doc/build/doctrees ./doc/source ./doc/build/html

[script]
_open-pdf-docs:
    import webbrowser
    from pathlib import Path
    webbrowser.open(f"file://{Path('./doc/build/pdf/django-enum.pdf').absolute()}")

# build pdf documentation
build-docs-pdf: _install-docs
    @just run sphinx-build --fresh-env --builder latex --doctree-dir ./doc/build/doctrees ./doc/source ./doc/build/pdf
    make -C ./doc/build/pdf
    @just _open-pdf-docs

# build the docs
build-docs: build-docs-html

# build docs and package
build: build-docs-html
    uv build

# open the html documentation
[script]
open-docs:
    import os
    import webbrowser
    webbrowser.open(f'file://{os.getcwd()}/doc/build/html/index.html')

# build and open the documentation
docs: build-docs-html open-docs

# serve the documentation, with auto-reload
docs-live: _install-docs
    @just run --no-default-groups --group docs sphinx-autobuild doc/source doc/build --open-browser --watch src --port 8000 --delay 1

_link_check:
    -uv run --no-default-groups --group docs sphinx-build -b linkcheck -Q -D linkcheck_timeout=10 ./doc/source ./doc/build

# check the documentation links for broken links
[script]
check-docs-links: _link_check
    import os
    import sys
    import json
    from pathlib import Path
    # The json output isn't valid, so we have to fix it before we can process.
    data = json.loads(f"[{','.join((Path(os.getcwd()) / 'doc/build/output.json').read_text().splitlines())}]")
    broken_links = [
        link for link in data
        if (
            link["status"] not in {"working", "redirected", "unchecked", "ignored"}
            and link["uri"] not in {"https://www.mysql.com"}
        )
    ]
    if broken_links:
        for link in broken_links:
            print(f"[{link['status']}] {link['filename']}:{link['lineno']} -> {link['uri']}", file=sys.stderr)
        sys.exit(1)

# lint the documentation
check-docs:
    @just run --no-default-groups --group docs doc8 --ignore-path ./doc/build --max-line-length 100 -q ./doc

# fetch the intersphinx references for the given package
[script]
fetch-refs LIB: _install-docs
    import os
    from pathlib import Path
    import logging as _logging
    import sys
    import runpy
    from sphinx.ext.intersphinx import inspect_main
    _logging.basicConfig()

    libs = runpy.run_path(Path(os.getcwd()) / "doc/source/conf.py").get("intersphinx_mapping")
    url = libs.get("{{ LIB }}", None)
    if not url:
        sys.exit(f"Unrecognized {{ LIB }}, must be one of: {', '.join(libs.keys())}")
    if url[1] is None:
        url = f"{url[0].rstrip('/')}/objects.inv"
    else:
        url = url[1]

    raise SystemExit(inspect_main([url]))

# lint the code
check-lint:
    @just run --no-default-groups --group lint ruff check --select I
    @just run --no-default-groups --group lint ruff check

# check if the code needs formatting
check-format:
    @just run --no-default-groups --group lint ruff format --check

# check that the readme renders
check-readme:
    @just run --no-default-groups --group lint -m readme_renderer ./README.md -o /tmp/README.html

# sort the python imports
sort-imports:
    @just run --no-default-groups --group lint ruff check --fix --select I

# format the code and sort imports
format: sort-imports
    just --fmt --unstable
    @just run --no-default-groups --group lint ruff format

# sort the imports and fix linting issues
lint: sort-imports
    @just run --no-default-groups --group lint ruff check --fix

# fix formatting, linting issues and import sorting
fix: lint format

# run all static checks
check: check-lint check-format check-types check-package check-docs check-readme

# run all checks including documentation link checking (slow)
check-all: check check-docs-links

# regenerate test migrations using the lowest version of Django
remake-test-migrations:
    - rm tests/**/migrations/00*.py
    uv run --no-default-groups  --exact --isolated --resolution lowest-direct --all-extras --group test django-admin makemigrations

# run all tests
test-all DB_CLIENT="dev":
    # No Optional Dependency Unit Tests
    # todo clean this up, rerunning a lot of tests
    @just run --no-default-groups --exact --group test --group {{ DB_CLIENT }} --isolated pytest --cov-append
    @just run --no-default-groups --exact --extra properties --group test --group {{ DB_CLIENT }} --isolated pytest --cov-append
    @just run --no-default-groups --exact --extra rest --group test --group {{ DB_CLIENT }} --isolated pytest --cov-append
    @just run --no-default-groups --exact --all-extras --group test --group {{ DB_CLIENT }} --isolated pytest --cov-append

# test properties integration
test-properties *TESTS:
    @just run --no-default-groups --extra properties --group test --exact --isolated pytest {{ TESTS }} --cov-append

# test drf integration
test-drf *TESTS:
    @just run --no-default-groups --extra rest --group test --exact --isolated pytest {{ TESTS }} --cov-append

# test filters integration
test-filters *TESTS:
    @just run --no-default-groups --extra filters --group test --exact --isolated pytest {{ TESTS }} --cov-append

test *TESTS:
    @just run --no-default-groups --exact --group test --isolated pytest {{ TESTS }} --cov-append

# debug an test
debug-test *TESTS:
    @just run pytest \
      -o addopts='-ra -q' \
      -s --trace --pdbcls=IPython.terminal.debugger:Pdb \
      {{ TESTS }}

# run the pre-commit checks
precommit:
    @just run pre-commit

# generate the test coverage report
coverage:
    @just run --no-default-groups --group coverage coverage combine --keep *.coverage
    @just run --no-default-groups --group coverage coverage report
    @just run --no-default-groups --group coverage coverage xml

# run the command in the virtual environment
run +ARGS:
    uv run {{ ARGS }}

# run the tests and capture screenshots for the docs
generate-screenshots *TESTS:
    @just run --no-default-groups --all-extras --group test --exact --isolated pytest --record-screenshots -m screenshots {{ TESTS }}

# revert screenshots to HEAD
revert-screenshots:
    git checkout doc/source/widgets/*.png

# validate the given version string against the lib version
[script]
validate_version VERSION:
    import re
    import tomllib
    import django_enum
    from packaging.version import Version
    raw_version = "{{ VERSION }}".lstrip("v")
    version_obj = Version(raw_version)
    # the version should be normalized
    assert str(version_obj) == raw_version
    # make sure all places the version appears agree
    assert raw_version == tomllib.load(open('pyproject.toml', 'rb'))['project']['version']
    assert raw_version == django_enum.__version__
    print(raw_version)

# issue a relase for the given semver string (e.g. 2.1.0)
release VERSION: install check-all
    @just validate_version v{{ VERSION }}
    git tag -s v{{ VERSION }} -m "{{ VERSION }} Release"
    git push origin v{{ VERSION }}
