<div align="center">
    <h1>lora-gpiozero</h1>
    A simple implementation of LoRa for the raspberry pi5, 
    utilising gpiozero and spidev already installed on Raspberry Pi OS.
</div>

> Tested with a sx1278 lora module at 433MHz.

## :runner: To install and use on a raspberrypi
> Create a virtual environment that can access system packages
```commandline
python3 -m venv .venv --system-site-packages
source .venv/bin/activate
```
> Install with pip
```commandline
pip install lora-gpiozero
```