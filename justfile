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
install-uv:
    curl -LsSf https://astral.sh/uv/install.sh | sh

# install the uv package manager
[windows]
install-uv:
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# setup the venv, pre-commit hooks
setup python="python":
    uv venv -p {{ python }}
    @just install-prek

# install git pre-commit hooks
install-prek:
    uv tool install prek
    uv run prek install

# update and install development dependencies
install *OPTS="--all-extras":
    uv sync {{ OPTS }}

# run the development server
runserver:
    @just manage makemigrations
    @just manage migrate
    @just manage runserver 8027

# run static type checking with mypy
check-types-mypy *ENV:
    @just run {{ ENV }} --no-default-groups --all-extras --group typing mypy

# run static type checking with pyright
check-types-pyright *ENV:
    @just run {{ ENV }} --no-default-groups --all-extras --group typing pyright

# run all static type checking
check-types *ENV:
    @just check-types-mypy {{ ENV }}
    @just check-types-pyright {{ ENV }}

# run all static type checking in an isolated environment
check-types-isolated *ENV:
    @just check-types-mypy {{ ENV }} --exact --isolated
    @just check-types-pyright {{ ENV }} --exact --isolated

# run package checks
check-package:
    uv pip check

# remove doc build artifacts
[script]
clean-docs:
    import shutil
    shutil.rmtree('./doc/build', ignore_errors=True)

# remove the virtual environment
clean-env:
    python -c "import shutil, pathlib; p=pathlib.Path('.venv'); shutil.rmtree(p, ignore_errors=True) if p.exists() else None"

# remove all git ignored files
clean-git-ignored:
    git clean -fdX

# remove all non repository artifacts
clean: clean-docs clean-env clean-git-ignored

# build html documentation
build-docs-html:
    @just run --group docs --all-extras --isolated --no-default-groups --exact sphinx-build --fresh-env --builder html --doctree-dir ./doc/build/doctrees ./doc/source ./doc/build/html

[script]
_open-pdf-docs:
    import webbrowser
    from pathlib import Path
    webbrowser.open(f"file://{Path('./doc/build/pdf/djangoenum.pdf').absolute()}")

# build pdf documentation
build-docs-pdf:
    @just run --group docs --all-extras --isolated --no-default-groups --exact sphinx-build --fresh-env --builder latex --doctree-dir ./doc/build/doctrees ./doc/source ./doc/build/pdf
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
docs-live:
    @just run --group docs --all-extras --isolated --no-default-groups sphinx-autobuild doc/source doc/build --open-browser --watch src --port 0 --delay 1

_link-check:
    -uv run --no-default-groups --group docs sphinx-build -b linkcheck -Q -D linkcheck_timeout=10 ./doc/source ./doc/build

# check the documentation links for broken links
[script]
check-docs-links: _link-check
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
check-docs *ENV:
    @just run {{ ENV }} --no-default-groups --group docs doc8 --ignore-path ./doc/build --max-line-length 100 -q ./doc

_install-docs:
    uv sync --no-default-groups --group docs --all-extras

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
check-lint *ENV:
    @just run {{ ENV }} --no-default-groups --group lint ruff check --select I
    @just run {{ ENV }} --no-default-groups --group lint ruff check

# check if the code needs formatting
check-format *ENV:
    @just run {{ ENV }} --no-default-groups --group lint ruff format --check

# check that the readme renders
check-readme *ENV:
    @just run {{ ENV }} --no-default-groups --group lint -m readme_renderer ./README.md -o /tmp/README.html

# sort the python imports
sort-imports *ENV:
    @just run {{ ENV }} --no-default-groups --group lint ruff check --fix --select I

# format the code and sort imports
format *ENV:
    @just sort-imports {{ ENV }}
    just --fmt --unstable
    @just run {{ ENV }} --no-default-groups --group lint ruff format

# sort the imports and fix linting issues
lint *ENV:
    @just sort-imports {{ ENV }}
    @just run {{ ENV }} --no-default-groups --group lint ruff check --fix

# fix formatting, linting issues and import sorting
fix *ENV:
    @just lint {{ ENV }}
    @just format {{ ENV }}

# run bandit static security analysis
bandit:
    @just run --no-default-groups --group lint bandit -c pyproject.toml -r ./src -f sarif -o bandit.sarif

# run all static checks
check *ENV:
    @just check-lint {{ ENV }}
    @just check-format {{ ENV }}
    @just check-types {{ ENV }}
    @just check-package
    @just check-docs {{ ENV }}
    @just check-readme {{ ENV }}

# run all checks including documentation link checking (slow)
check-all *ENV:
    @just check {{ ENV }}
    @just check-docs-links

# run zizmor security analysis of CI
zizmor:
    cargo install --locked zizmor
    zizmor --format sarif .github/workflows/ > zizmor.sarif

# regenerate test migrations using the lowest version of Django
remake-test-migrations:
    - rm tests/**/migrations/00*.py
    @just make-test-migrations

# make test migrations
make-test-migrations:
    uv run --no-default-groups  --exact --isolated --resolution lowest-direct --all-extras --group test django-admin makemigrations

# run all tests
test-all *ENV:
    # No Optional Dependency Unit Tests
    # todo clean this up, rerunning a lot of tests
    @just run {{ ENV }} --no-default-groups --exact --group test --isolated pytest --cov-append
    @just run {{ ENV }} --no-default-groups --exact --extra properties --group test --isolated pytest --cov-append
    @just run {{ ENV }} --no-default-groups --exact --extra rest --group test --isolated pytest --cov-append
    @just run {{ ENV }} --no-default-groups --exact --all-extras --group test --isolated pytest --cov-append

# test properties integration
test-properties *TESTS:
    @just run --no-default-groups --extra properties --group test --exact --isolated pytest {{ TESTS }} --cov-append

# test drf integration
test-drf *TESTS:
    @just run --no-default-groups --extra rest --group test --exact --isolated pytest {{ TESTS }} --cov-append

# test filters integration
test-filters *TESTS:
    @just run --no-default-groups --extra filters --group test --exact --isolated pytest {{ TESTS }} --cov-append

# run specific tests
test *TESTS:
    @just run --group test --no-sync pytest {{ TESTS }}

# debug an test
debug-test *TESTS:
    @just run pytest \
      -o addopts='-ra -q' \
      -s --trace --pdbcls=IPython.terminal.debugger:Pdb \
      --headed {{ TESTS }}

# run the pre-commit checks
prek:
    @just run prek run

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

# issue a release for the given semver string (e.g. 2.1.0)
release VERSION: install check-all
    @just validate_version v{{ VERSION }}
    git tag -s v{{ VERSION }} -m "{{ VERSION }} Release"
    git push https://github.com/django-commons/django-enum.git v{{ VERSION }}
