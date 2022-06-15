from datetime import datetime
from pathlib import Path
from typing import TypedDict
import json

from weather_formatter import format_weather
from weather_api_service import Weather


class WeatherStorage:
    """Interface for any storage saving weather data"""
    def save(self, weather: Weather) -> None:
        raise NotImplementedError


class PlainFileWeatherStorage(WeatherStorage):
    """Store weather in plain text file"""
    def __init__(self, file: Path):
        self._file = file

    def save(self, weather: Weather) -> None:
        now = datetime.now()
        formatted_weather = format_weather(weather)
        with open(self._file, 'a', encoding='utf8') as f:
            f.write(f'{now}\n{formatted_weather}\n\n')


class HistoryRecord(TypedDict):
    date: str
    weather: str


class JSONFileWeatherStorage(WeatherStorage):
    """Stores weather in json file"""
    def __init__(self, jsonfile: Path):
        self._jsonfile = jsonfile
        self._init_storage()

    def save(self, weather: Weather) -> None:
        history = self._read_history()
        history.append({
            'date': str(datetime.now()),
            'weather': format_weather(weather)
        })
        self._write(history)

    def _init_storage(self):
        if not self._jsonfile.exists():
            self._jsonfile.write_text('[]')
    
    def _read_history(self) -> list[HistoryRecord]:
        with open(self._jsonfile, 'r', encoding='utf8') as f:
            return json.load(f)

    def _write(self, history: list[HistoryRecord]) -> None:
        with open(self._jsonfile, 'w', encoding='utf8') as f:
            json.dump(history, f, ensure_ascii=False, indent=4)


def save_weather(weather: Weather, storage: WeatherStorage) -> None:
    """Saves weather in the storage"""
    storage.save(weather)
