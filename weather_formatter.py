from weather_api_service import Weather

def format_weather(weather_data: Weather) -> str:
    """Formats weather data in a string"""
    return (f'{weather_data.city}, температура {weather_data.temperature}C, '
            f'{weather_data.weather_type.value}\n'
            f'Восход: {weather_data.sunrise_time.strftime("%H:%M")}\n'
            f'Закат: {weather_data.sunset_time.strftime("%H:%M")}\n')


if __name__ == '__main__':
    from datetime import datetime
    from weather_api_service import WeatherType
    print(format_weather(Weather(
        temperature=18,
        weather_type=WeatherType.CLOUDS,
        sunrise_time=datetime.now(),
        sunset_time=datetime.now(),
        city='New York'
    )))