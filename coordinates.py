from typing import NamedTuple
from subprocess import Popen, PIPE
from config import USE_ROUNDED_COORDS
import platform

from exceptions import CantGetCoordinates


_pws_script_path = './get_loc.ps1'


class Coordinates(NamedTuple):
    longitude: float
    latitude: float


def get_coordinates() -> Coordinates:
    """Returns current coordinates using gpc-service"""
    current_os = platform.system()
    if current_os == 'Windows':
        coordinates = _get_coordinates_with_pws()
        return coordinates   
    raise NotImplementedError(f"Can't get coordinates for this OS ({current_os})")


def _get_coordinates_with_pws() -> Coordinates:
    """Returns current coordinates using powershell script defined by _pws_script_path"""
    pws_output = _get_pws_output()
    coordinates = _parse_coordinates_from_pws(pws_output)
    return _round_coordinates(coordinates)


def _get_pws_output() -> bytes:
    process = Popen(['powershell.exe', _pws_script_path], stdout=PIPE)
    output, err = process.communicate()
    exit_code = process.wait()
    if err is not None or  exit_code != 0:
        raise CantGetCoordinates
    return output


def _parse_coordinates_from_pws(pws_output) -> Coordinates:
    try:
        output_lines = pws_output.decode().strip().split('\r')
    except UnicodeDecodeError:
        raise CantGetCoordinates
    return Coordinates(
        longitude=float(output_lines[0]), 
        latitude=float(output_lines[1])
    )


def _round_coordinates(coords : Coordinates):
    if USE_ROUNDED_COORDS:
        coords = Coordinates(*map(
            lambda n: round(n, 1), 
            [coords.longitude, coords.latitude]))
    return coords


if __name__ == '__main__':
    print(get_coordinates())
    