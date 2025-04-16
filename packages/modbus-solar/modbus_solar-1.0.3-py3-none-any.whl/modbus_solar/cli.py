# cli.py

import typer
import json
from .get import get_all

app = typer.Typer()

@app.command()
def cli_get_all( modbus_device: str = "/dev/ttyUSB0", modbus_slave_address: int = 1 ):
	typer.echo(json.dumps(get_all(modbus_device=modbus_device,modbus_slave_address=modbus_slave_address)))

if __name__ == "__main__":
	app()
