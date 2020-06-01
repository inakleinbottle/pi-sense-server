import asyncio
import dataclasses

from datetime import datetime
from pathlib import Path


import aiofiles

@dataclasses.dataclass()
class TempSensorReading:
    id: str
    read_time: datetime
    temperature: float
    status: str


TEMP_SENSORS_PATH = Path("/sys/bus/w1/devices/")
SENSORS = None


async def load_sensors():
    global SENSORS

    sensors = TEMP_SENSORS_PATH.glob("28*")
    SENSORS = tuple(p.stem for p in sensors)


async def get_path_for_sensor(sensor):
    return TEMP_SENSORS_PATH.joinpath(sensor, "w1_slave")


async def read_sensor(sensor):
    path = await get_path_for_sensor(sensor)


    async with aiofiles.open(path) as f:
        contents = f.read()

    if not contents:
        return TempSensorReading(
            sensor, 
            datetime.datetime.now(),
            0.0,
            "Read failed"
        )

    lines = list(contents.splitlines())

    if not lines[0].endswith("YES"):
        return TempSensorReading(
            sensor, 
            datetime.datetime.now(),
            0.0,
            "Sensor failed"
        )

    _, t_str = lines[1].strip().split("=")

    t_float = int(t_str) / 1000

    return TempSensorReading(
        sensor, 
        datetime.datetime.now(),
        t_float,
        "Read OK"
    )


async def read_all_sensors():

    return asyncio.gather(
        [read_sensor(sensor) for sensor in SENSORS]
    )