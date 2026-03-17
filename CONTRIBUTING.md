# Contributing

Contributions are encouraged! Please use the issue page to submit feature requests or bug reports. Issues with attached PRs will be given priority and have a much higher likelihood of acceptance. Please also open an issue and associate it with any submitted PRs. That said, the aim is to keep this library as lightweight as possible. Only features with broad based use cases will be considered.

We are actively seeking additional maintainers. If you're interested, please contact [me](https://github.com/bckohan).


## Installation

### Install Just

We provide a platform independent justfile with recipes for all the development tasks. You should [install just](https://just.systems/man/en/installation.html) if it is not on your system already.

`django-enum` uses [uv](https://docs.astral.sh/uv) for environment, package, and dependency management. ``just setup`` will install the necessary build tooling if you do not already have it:

```sh
just setup <python version>
```

**This will also install prek** If you wish to submit code that does not pass pre-commit checks you can disable [prek](https://prek.j178.dev/) by running:

```sh
just run prek uninstall
```

### Install the Dev environment

To install all development dependencies run the ``install`` recipe:

```sh
just install
```

## Documentation

`django-enum` documentation is generated using [Sphinx](https://www.sphinx-doc.org). Any new feature PRs must provide updated documentation for the features added. To build the docs run:

```sh
just docs  # build and open docs
just check-docs  # lint the docs
just check-docs-links  # check for broken links in the docs
```

You can run a live documentation server that will automatically update during editing using:

```sh
just docs-live
```

## Static Analysis

`django-enum` uses [ruff](https://docs.astral.sh/ruff/) for Python linting, header import standardization and code formatting. [mypy](http://mypy-lang.org/) and [pyright](https://github.com/microsoft/pyright) are used for static type checking. Before any PR is accepted the following must be run, and static analysis tools should not produce any errors or warnings. Disabling certain errors or warnings where justified is acceptable:

To fix formatting and linting problems that are fixable run:

```sh
just fix
```

To run all static analysis without automated fixing you can run:

```sh
just check
```

## Running Tests

`django-enum` uses [pytest](https://docs.pytest.org/) to define and run tests. All the tests are housed under ``tests/``. Before a PR is accepted, all tests must be passing and the code coverage must be at 100%. A small number of exempted error handling branches are acceptable.

**Note if not using** ``just test-all`` **you will need to make sure the migrations exist first by running** ``just manage makemigrations``

To run the full suite in an isolated virtual environment with only the minimal test dependencies installed you should use ``test-all``:

```sh
just test-all 
```

To run the full test suite against a specific python/django/database driver you can pass sync options to ``test-all``. This requires the djXX dependency groups. For example to run against python 3.11 on Django 5.2.x:

```sh
just test-all -p 3.11 --group dj52 --group psycopg3
```


To run the full suite:

```sh
    just test
```

To run a single test, or group of tests in a class:

```sh
    just test <path_to_tests_file>::ClassName::FunctionName
```

For instance to run all tests in ExampleTests, and then just the
test_color example test you would do:

```sh
    just test tests/test_examples.py::ExampleTests
    just test tests/test_examples.py::ExampleTests::test_color
```

## Testing Different Databases

By default, the tests will run against postgresql so in order to run the tests you will need to have a postgresql server running that is accessible to the default postgres user with no password. The test suite can be run against any RDBMS supported by Django. Just set the ``RDBMS`` environment variable to one of:

  * postgres
  * sqlite
  * mysql
  * mariadb
  * oracle

The settings for each RDBMS can be found in ``tests/settings.py``. The database settings can be altered via environment variables that are referenced therein. The default settings are designed to work out of the box with the official docker images for each RDBMS. Reference the github actions workflow for an example of how to run the tests against each RDBMS using docker containers.

Additional dependency groups will need to be installed for some RDBMS, to run the full suite against a given RDBMS, set the ``RDBMS`` environment variable and run test-all with the appropriate db client argument.

```sh
    just test-all  # sqlite tests
    just test-all --group psycopg3  # for postgres using psycopg3
    just test-all --group psycopg2  # for postgres using psycopg2
    just test-all --group mysql  # for mysql or mariadb
    just test-all --group oracle  # for oracle
```

### Debugging tests

To debug a test use the ``debug-test`` recipe:

```sh
just debug-test tests/test_examples.py::ExampleTests::test_color
```

This will set a breakpoint at the start of the test.

The ``test`` and ``debug-test`` recipes use the installed virtual environment - not an isolated one like ``test-all``. To run specific tests or debug tests against specific Python or Django versions you must first install the environment you want:

```sh
just install -p 3.11 --group dj52
just test -k test_call_command
just debug-test -k test_call_command
```

## Issuing Releases

The release workflow is triggered by tag creation. You must have [git tag signing enabled](https://docs.github.com/en/authentication/managing-commit-signature-verification/signing-commits). Our justfile has a release shortcut:

```sh
    just release x.x.x
```

## Just Recipes

```sh
build                        # build docs and package
build-docs                   # build the docs
build-docs-html              # build html documentation
build-docs-pdf               # build pdf documentation
check *ENV                   # run all static checks
check-all *ENV               # run all checks including documentation link checking (slow)
check-docs *ENV              # lint the documentation
check-docs-links             # check the documentation links for broken links
check-format *ENV            # check if the code needs formatting
check-lint *ENV              # lint the code
check-package                # run package checks
check-readme *ENV            # check that the readme renders
check-types *ENV             # run all static type checking
check-types-isolated *ENV    # run all static type checking in an isolated environment
check-types-mypy *ENV        # run static type checking with mypy
check-types-pyright *ENV     # run static type checking with pyright
clean                        # remove all non repository artifacts
clean-docs                   # remove doc build artifacts
clean-env                    # remove the virtual environment
clean-git-ignored            # remove all git ignored files
coverage                     # generate the test coverage report
debug-test *TESTS            # debug an test
docs                         # build and open the documentation
docs-live                    # serve the documentation, with auto-reload
fetch-refs LIB               # fetch the intersphinx references for the given package
fix *ENV                     # fix formatting, linting issues and import sorting
format *ENV                  # format the code and sort imports
generate-screenshots *TESTS  # run the tests and capture screenshots for the docs
install *OPTS="--all-extras" # update and install development dependencies
install-precommit            # install git pre-commit hooks
install-uv                   # install the uv package manager
lint *ENV                    # sort the imports and fix linting issues
make-test-migrations         # make test migrations
manage *COMMAND              # run the django admin
open-docs                    # open the html documentation
precommit                    # run the pre-commit checks
release VERSION              # issue a release for the given semver string (e.g. 2.1.0)
remake-test-migrations       # regenerate test migrations using the lowest version of Django
revert-screenshots           # revert screenshots to HEAD
run +ARGS                    # run the command in the virtual environment
runserver                    # run the development server
setup python="python"        # setup the venv, pre-commit hooks
sort-imports *ENV            # sort the python imports
test *TESTS                  # run specific tests
test-all *ENV                # run all tests
test-drf *TESTS              # test drf integration
test-filters *TESTS          # test filters integration
test-properties *TESTS       # test properties integration
validate_version VERSION     # validate the given version string against the lib version
zizmor                       # run zizmor security analysis of CI
```
