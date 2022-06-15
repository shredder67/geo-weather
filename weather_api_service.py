from typing import NamedTuple
from datetime import datetime
from enum import Enum
import json
from json.decoder import JSONDecodeError
import urllib.request
from urllib.error import URLError
import ssl

from coordinates import Coordinates
from config import OPENWEATHER_URL
from exceptions import ApiServiceError


Celsius = int


class WeatherType(Enum):
    THUNDERSTORM = 'Гроза'
    DRIZZLE = 'Изморозь'
    RAIN = 'Дождь'
    SNOW = 'Снег'
    CLEAR = 'Ясно'
    FOG = 'Туман'
    CLOUDS = 'Облачно'


class Weather(NamedTuple):
    temperature: Celsius
    weather_type: WeatherType
    sunrise_time: datetime
    sunset_time: datetime
    city: str


def get_weather(coordinates: Coordinates) -> Weather:
    """Requests weather in OpenWeather API and returns it"""

    openweather_res = get_openweather_res(coordinates.latitude, coordinates.longitude)
    weather = _parse_openweather_res(openweather_res)
    return weather


def get_openweather_res(latitude: float, longitude: float) -> str:
    ssl._create_default_https_context = ssl._create_unverified_context
    url = OPENWEATHER_URL.format(lat=latitude, lon=longitude)
    try:
        return urllib.request.urlopen(url).read()
    except URLError:
        raise ApiServiceError


def _parse_openweather_res(openweather_res: str) -> Weather:
    try:
        openweather_dict = json.loads(openweather_res)
    except JSONDecodeError:
        raise ApiServiceError
    return Weather(
        temperature=_parse_temperature(openweather_dict),
        weather_type=_parse_weather_type(openweather_dict),
        sunrise_time=_parse_sunrise_time(openweather_dict),
        sunset_time=_parse_sunset_time(openweather_dict),
        city='Moscow'
    )


def _parse_temperature(openweather_dict: dict) -> Celsius:
    return round(openweather_dict['main']['temp'])


def _parse_weather_type(openweather_dict: dict) -> WeatherType:
    try:
        weather_type_id = str(openweather_dict['weather'][0]['id'])
    except (IndexError, KeyError):
        raise ApiServiceError
    weather_types = {
        '1': WeatherType.THUNDERSTORM,
        '3': WeatherType.DRIZZLE,
        '5': WeatherType.RAIN,
        '6': WeatherType.SNOW,
        '7': WeatherType.FOG,
        '800': WeatherType.CLEAR,
        '80': WeatherType.CLOUDS
    }
    for _id, _weather_type in weather_types.items():
        if weather_type_id.startswith(_id):
            return _weather_type
    raise ApiServiceError

def _parse_sunrise_time(openweather_dict: dict) -> datetime:
     return datetime.fromtimestamp(openweather_dict['sys']['sunrise'])


def _parse_sunset_time(openweather_dict: dict) -> datetime:
     return datetime.fromtimestamp(openweather_dict['sys']['sunset'])


if __name__ == '__main__':
    print(get_weather(Coordinates(10., 20.)))
