# Page-loader
It is a console utility for downloading html pages.

### Test statuses:
[![Project check](https://github.com/zavr1k/python-project-lvl3/actions/workflows/project-check.yml/badge.svg?branch=main)](https://github.com/zavr1k/python-project-lvl3/actions/workflows/project-check.yml)
[![Actions Status](https://github.com/zavr1k/python-project-lvl3/workflows/hexlet-check/badge.svg)](https://github.com/zavr1k/python-project-lvl3/actions)
[![Maintainability](https://api.codeclimate.com/v1/badges/55b6ef5c5fee02b4617f/maintainability)](https://codeclimate.com/github/zavr1k/python-project-lvl3/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/55b6ef5c5fee02b4617f/test_coverage)](https://codeclimate.com/github/zavr1k/python-project-lvl3/test_coverage)

---

#### How to install.
1. Clone this repository `git clone git@github.com:zavr1k/python-project-lvl3.git`
2. Use `make build` for build the source.
3. Run `make install` to install the package.

#### Usage.
```
usage: page-loader [-h] [--output OUTPUT] [--log-level {INFO,DEBUG,WARNING}] url

positional arguments:
  url

optional arguments:
  -h, --help            show this help message and exit
  --output OUTPUT, -o OUTPUT
                        Path to directory
  --log-level {INFO,DEBUG,WARNING}
                        Set level for logger
```
[![asciicast](https://asciinema.org/a/412546.svg)](https://asciinema.org/a/412546)
