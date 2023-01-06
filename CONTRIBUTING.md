# Contributing

When contributing to this repository, please first discuss the change you wish to make via a GitHub issue,
email, or any other method with the owners of this repository before making a change. 

Please note we have a [code of conduct](./CODE_OF_CONDUCT.md), please follow it in all your interactions with the project.

## Pull Request Process

Before submitting a pull request:

1. Ensure tests pass for bug fixes.
2. Ensure new tests are added to cover new features or non trivial changes.
3. Ensure relevant documentation is updated.

## Environment Setup

Install the following:

* [Poetry](https://python-poetry.org/docs/#installation)
* GDAL
    * macOS: `brew install gdal`
    * Debian/Ubuntu: `sudo apt-get install libgdal-dev`

Run the following

1. Clone the repository:

        $ git clone git@github.com:noteable-io/dx.git && cd dx

2. Install dependencies:

        $ poetry install

3. Validate the environment by running the tests:

        $ poetry run pytest
