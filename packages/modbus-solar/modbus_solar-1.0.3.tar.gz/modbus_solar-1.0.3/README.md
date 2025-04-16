# Modbus Solar

[![pypi](https://img.shields.io/pypi/v/modbus-solar.svg)](https://pypi.org/project/modbus-solar/)
[![python](https://img.shields.io/pypi/pyversions/modbus-solar.svg)](https://pypi.org/project/modbus-solar/)
[![built with nix](https://builtwithnix.org/badge.svg)](https://builtwithnix.org)

## Intro

This project is to pull stats out of a Renogy DCC50S solar charge controller.

The connection will be made via Modbus/RS485.

The end state will be to output stats in `json` format ready to be ingested into something like an InfluxDb instance or to publish to a MQTT Topic.

## Pre-Reqs

You require a Modbus/RS485 connector, most probably will be a USB varient. Most applications will be using a small IoT device or Raspberry Pi to serve the USB device and then connect back to a logging system of some sort.

The Modbus parameters are hard coded but variabalised for the device ID and the salve address which could change.

## Using

### To install

```bash
pip install modbus-solar
```

### To Use

1. `python`

    ```python
    #!/usr/bin/env python
    from modbus_solar import get_all
    import json

    # json.dumps() ensures you can parse through jq
    stats = json.dumps(get_all())
    print(stats)
    ```

1. `bash`

    ```bash
    modbus-solar --help
    modbus-solar
    ```

## Releases

My aim is to keep to [semver versioning](https://semver.org/)

The pipeline will push to PyPi so this should be the main way of getting the recent packages. But the pipeline will also create releases in Gitlab for versions that are tagged

## Development

My development has taken place using NixOS, I've included the `shell.nix` for anyone that requires it.

However the build pipeline is performed using the basic python:3.11 image from Gitlab.

To build run the following:

```bash
python -m build --sdist --wheel
```
