# ProxiesGrabber

## Overview
ProxiesGrabber is a Python package designed to scrape free proxy lists from various online sources. It uses multithreading to enhance performance and efficiently gather proxies.

## Features
- Fetches free proxies from multiple sources
- Uses multithreading for better performance
- Automatically formats proxies into `IP:PORT`
- Simple and easy-to-use interface

## Installation
You can install ProxiesGrabber via GitHub or PyPI.

### Install from GitHub
```sh
pip install git+https://github.com/alfarttusie/ProxiesGrabber.git
```

### Install from PyPI
```sh
pip install ProxiesGrabber
```

## Usage
```python
from proxiesscraper import ProxiesGrabber

scraper = ProxiesGrabber()
print(scraper.list)  # List of formatted proxies
```

## Dependencies
- `requests`

## License
MIT License

## Author
[alfarttusie](https://github.com/alfarttusie)

