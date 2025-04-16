# checknet

A simple Python library to check internet connectivity using a TCP socket.

## Installation

```bash
pip install checknet

from checknet import is_connected

if is_connected():
    print("Online")
else:
    print("Offline")