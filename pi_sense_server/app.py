from dataclasses import asdict

from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route

from pi_sense_server.sensors import TempSensorReading, read_all_sensors, load_sensors


async def main(request):
    readings = await read_all_sensors()
    return JSONResponse([asdict(read) for read in readings])



app = Starlette(routes=[Route("/", main)], on_startup=[load_sensors])