# Contributing

Contributions are encouraged! Please use the issue page to submit feature requests or bug reports. Issues with attached PRs will be given priority and have a much higher likelihood of acceptance. Please also open an issue and associate it with any submitted PRs. That said, the aim is to keep this library as lightweight as possible. Only features with broad based use cases will be considered.

We are actively seeking additional maintainers. If you're interested, please contact [me](https://github.com/bckohan).


## Installation

### Install Just

We provide a platform independent justfile with recipes for all the development tasks. You should [install just](https://just.systems/man/en/installation.html) if it is not on your system already.

`django-enum` uses [uv](https://docs.astral.sh/uv) for environment, package and dependency management:

```bash
    just install_uv
```

Next, initialize and install the development environment:

```bash
    just setup <optional python version>
    just install
```

## Documentation

`django-enum` documentation is generated using [Sphinx](https://www.sphinx-doc.org). Any new feature PRs must provide updated documentation for the features added. To build the docs run:

```bash
    just install-docs
    just docs
```

You can run a live documentation server that will automatically update during editing using:

```bash
    just docs-live
```

## Static Analysis

`django-enum` uses [ruff](https://docs.astral.sh/ruff) for python linting and formatting. [mypy](http://mypy-lang.org) is used for static type checking. Before any PR is accepted the following must be run, and static analysis tools should not produce any errors or warnings. Disabling certain errors or warnings where justified is acceptable:

```bash
    just check
```

## Running Tests

`django-enum` uses [pytest](https://docs.pytest.org/) to define and run tests. All the tests are housed under ``tests/``. Before a PR is accepted, all tests must be passing and the code coverage must be at 100%. A small number of exempted error handling branches are acceptable.

To run the full suite:

```bash
    just test
```

To run a single test, or group of tests in a class:

```bash
    just test <path_to_tests_file>::ClassName::FunctionName
```

For instance to run all tests in ExampleTests, and then just the
test_color example test you would do:

```bash
    just test tests/test_examples.py::ExampleTests
    just test tests/test_examples.py::ExampleTests::test_color
```

## RDBMS

By default, the tests will run against postgresql so in order to run the tests you will need to have a postgresql server running that is accessible to the default postgres user with no password. The test suite can be run against any RDBMS supported by Django. Just set the ``RDBMS`` environment variable to one of:

  * postgres
  * sqlite
  * mysql
  * mariadb
  * oracle

The settings for each RDBMS can be found in ``tests/settings.py``. The database settings can be altered via environment variables that are referenced therein. The default settings are designed to work out of the box with the official docker images for each RDBMS. Reference the github actions workflow for an example of how to run the tests against each RDBMS using docker containers.

Additional dependency groups will need to be installed for some RDBMS, to run the full suite against a given RDBMS, set the ``RDBMS`` environment variable and run test-all with the appropriate db client argument.

```bash
    just test-all  # sqlite tests
    just test-all psycopg3  # for postgres using psycopg3
    just test-all psycopg2  # for postgres using psycopg2
    just test-all mysql  # for mysql or mariadb
    just test-all oracle  # for oracle
```

## Issuing Releases

The release workflow is triggered by tag creation. You must have [git tag signing enabled](https://docs.github.com/en/authentication/managing-commit-signature-verification/signing-commits). Our justfile has a release shortcut:

```bash
    just release x.x.x
```

## Just Recipes

```bash
build                        # build docs and package
build-docs                   # build the docs
build-docs-html              # build html documentation
build-docs-pdf               # build pdf documentation
check                        # run all static checks
check-docs                   # lint the documentation
check-docs-links             # check the documentation links for broken links
check-format                 # check if the code needs formatting
check-lint                   # lint the code
check-package                # run package checks
check-readme                 # check that the readme renders
check-types                  # run static type checking
clean                        # remove all non repository artifacts
clean-docs                   # remove doc build artifacts
clean-env                    # remove the virtual environment
clean-git-ignored            # remove all git ignored files
coverage                     # generate the test coverage report
docs                         # build and open the documentation
docs-live                    # serve the documentation, with auto-reload
fetch-refs LIB               # fetch the intersphinx references for the given package
fix                          # fix formatting, linting issues and import sorting
format                       # format the code and sort imports
install *OPTS="--all-extras" # update and install development dependencies
install-docs                 # install documentation dependencies
install-precommit            # install git pre-commit hooks
install_uv                   # install the uv package manager
lint                         # sort the imports and fix linting issues
manage *COMMAND              # run the django admin
open-docs                    # open the html documentation
precommit                    # run the pre-commit checks
release VERSION              # issue a relase for the given semver string (e.g. 2.1.0)
run +ARGS                    # run the command in the virtual environment
runserver                    # run the development server
setup python="python"        # setup the venv, pre-commit hooks and playwright dependencies
sort-imports                 # sort the python imports
test *TESTS                  # run tests
test-all DB_CLIENT="dev"     # run all tests
test-lock +PACKAGES          # lock to specific python and versions of given dependencies
validate_version VERSION     # validate the given version string against the lib version
```
