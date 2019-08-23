[![CircleCI](https://circleci.com/gh/abcmer/phish-stats.svg?style=svg)](https://circleci.com/gh/abcmer/phish-stats)

# phish-stats

Python package for generating statistics about the band Phish from Vermont.

## Getting Started

These instructions will get you set up for development and testing.

### Prerequisites

- [Python 3.6](https://www.python.org/downloads/release/python-360/)
- [API key from Phish.net](http://api.phish.net/keys/)

### Installing

Clone this repository and change to project root directory

```
git clone https://github.com/abcmer/phish-stats.git
cd phish-stats
```

Create Python3.6 virtual env and activate

```
python3 -m venv venv
source venv/bin/activate
```

Install Python3.6 dependencies

```
pip install -r requirements.txt
```

## Running the tests

Run the unit tests

```
export PHISHNET_API_KEY=<API_KEY>
python -m pytest
```

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
