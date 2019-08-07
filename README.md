## Pre-requisites

- [python 3.7+](https://www.python.org/downloads/)
- [gnu make](http://ftp.gnu.org/gnu/make/)

These probably already exist on your machine, so don't reinstall unless needed.

## Development/Test setup

Make a virtual environment:
```bash
mkvirtualenv -p python3 file-processing-pipeline # or your preferred way to create a virtual environment
```

Install dependencies for development and run time:
```bash
make init-dev
```

## Misc

### How to create a big file
(cd test/resources/; python make_big_file.py)

TODO:
- string constants
- docs
- maybe bdd?
- maybe yaml schema
