# legos.xkcd

[![Travis](https://img.shields.io/travis/bbriggs/legos.xkcd.svg)]() [![PyPI](https://img.shields.io/pypi/pyversions/legos.xkcd.svg)]() [![PyPI](https://img.shields.io/pypi/v/legos.xkcd.svg)]()

[![PyPI](https://img.shields.io/pypi/wheel/legos.xkcd.svg)]() [![PyPI](https://img.shields.io/pypi/l/legos.xkcd.svg)]() [![PyPI](https://img.shields.io/pypi/status/legos.xkcd.svg)]()

Fetch xkcd comics right from chat using this xkcd lego.

## Usage

`!xkcd` returns the latest comic
`!xkcd r` or `!xkcd random` will return a random comic
`!xkcd [int]` will search for and return the comic of corresponding number

## Installation

`pip3 install legos.xkcd`

This is a Lego designed for use with [Legobot](https://github.com/bbriggs/Legobot), so you'll get Legobot along with this. To deploy it, import the package and add it to the active legos like so:

```python
# This is the legobot stuff
from Legobot import Lego
# This is your lego
from legos.xkcd import XKCD

# Legobot stuff here
lock = threading.Lock()
baseplate = Lego.start(None, lock)
baseplate_proxy = baseplate.proxy()

# Add your lego
baseplate_proxy.add_child(XKCD)
```

## Tweaking

While you can use this one as-is, you could also add a localized version to your Legobot deployment by grabbing [xkcd.py](legos/xkcd.py) and deploying is as a local module. [Example of a Legobot instance with local modules](https://github.com/voxpupuli/thevoxfox/)

## Contributing

As always, pull requests are welcome.
