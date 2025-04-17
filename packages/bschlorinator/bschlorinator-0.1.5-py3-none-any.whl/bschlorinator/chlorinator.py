import asyncio
from serial import Serial
from collections.abc import Callable

import platform

try:
    import RPi.GPIO as GPIO
except (ImportError, RuntimeError):
    if platform.machine().startswith("arm"):
        raise  # Fails if on Raspberry Pi
    else:
        from unittest.mock import MagicMock
        GPIO = None


from . import const

def read_line_cr(port: Serial, max_length: int = 256, timeout:float = 1.0) -> list[bytes]:
    """Reads bytes from serial port and returns results as list"""
    read_value = []
    port.timeout = timeout
    while len(read_value) < max_length:
        char = port.read(1)
        if not char:
            break
        read_value.append(char)
        # Breaks out if linebreak
        if char in (b'\r', b'\n'):
            break
    return read_value

async def send_command(port: Serial, command: bytes):
    """Sends command to the serial port and returns response"""
    port.write(command)
    await asyncio.sleep(0.15)
    return read_line_cr(port)


def parse_response(response: list[bytes], multiplier: float, parser: Callable):
    """Parses response to a string"""
    if response:
        data = [value for value in map(ord, response)]
        return parser(data, multiplier)
    return ''

async def read_sensor_data(port: Serial) -> dict:
    """Reads and updates data of chlorinator sensor"""
    # Clear buffer to prevent wrong values
    port.reset_input_buffer()
    port.reset_output_buffer()

    zipped_sensors = zip(const.keys, const.commands, const.multipliers, const.parsers)
    data = {}
    for key, command, multiplier, parser in zipped_sensors:
        response = await send_command(port, command)
        data[key] = parse_response(response, multiplier, parser)
    return data

async def configure_serial(port: Serial, channel: int = 1) -> None:
    """Configures serial port and channel to send on"""
    channel_cmd = f"ATS200={channel-1}"
    commands = [
        channel_cmd,
        "ATS201=1",
        "ATS202=7",
        "ATS250=2",
        "ATS252=1",
        "ATS255=0",
        "ATS256=2",
        "ATS258=1",
        "ATS296=1"
    ]
    port.reset_input_buffer()
    port.reset_output_buffer()
    await asyncio.sleep(1)

    # Set serial to a command mode
    port.write(b"+++")
    await asyncio.sleep(1)

    for cmd in commands:
        print(f"Sending: {cmd}")
        port.write((cmd + "\x0d").encode())
        await asyncio.sleep(1)
    # Set serial back to data mode
    port.write(b'ATO\x0d')
    await asyncio.sleep(1)


async def reset_serial_module(gpio_pin: int) -> None:
    """Reset serial module"""
    GPIO.output(gpio_pin, GPIO.LOW)
    await asyncio.sleep(3)
    GPIO.output(gpio_pin, GPIO.HIGH)
    await asyncio.sleep(1)

def init_gpio(gpio_pin: int) -> None:
    """Init GPIO"""
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(gpio_pin, GPIO.OUT, initial=GPIO.LOW)

async def config_channel(port: Serial, channel: int) -> None:
    """Configuration of channel for serial port"""
    channel_cmd = f'ATS200={channel - 1}'
    port.reset_input_buffer()
    port.reset_output_buffer()
    await asyncio.sleep(1)

    # Set serial to a command mode
    port.write(b'+++')
    await asyncio.sleep(1)
    port.write((channel_cmd + '\x0d').encode())
    await asyncio.sleep(1)
    # Get back to data mode
    port.write('ATO\x0d'.encode())
    await asyncio.sleep(1)