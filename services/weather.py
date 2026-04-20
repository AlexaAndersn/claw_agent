import httpx
from core.config import settings

GEOCODE_CACHE = {}


async def get_coordinates(city: str) -> tuple:
    if city in GEOCODE_CACHE:
        return GEOCODE_CACHE[city]
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(
                "https://geocode-maps.yandex.ru/1.x",
                params={
                    "geocode": city,
                    "format": "json",
                    "apikey": settings.yandex_weather_api_key
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                point = data.get("response", {}).get("GeoObjectCollection", {}).get("featureMember", [{}])[0].get("GeoObject", {}).get("Point", {}).get("pos", "")
                if point:
                    lon, lat = point.split()
                    GEOCODE_CACHE[city] = (float(lat), float(lon))
                    return float(lat), float(lon)
    except Exception as e:
        print(f"Geocoding error: {e}")
    
    return None, None


async def get_weather_text(city: str = None) -> str:
    city = city or settings.default_city

    if not settings.yandex_weather_api_key:
        return "Погода недоступна (нет API ключа)"

    lat, lon = await get_coordinates(city)
    
    if lat is None or lon is None:
        lat, lon = 55.7881, 49.1221

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                "https://api.weather.yandex.ru/v2/forecast",
                params={"lat": lat, "lon": lon, "extra": "true"},
                headers={
                    "X-Yandex-API-Key": settings.yandex_weather_api_key,
                    "Content-Type": "application/json",
                },
            )

            if response.status_code == 200:
                data = response.json()
                fact = data.get("fact", {})
                temp = fact.get("temp", "?")
                condition = fact.get("condition", "unknown")
                condition_text = translate_condition(condition)
                return f"{temp}°C, {condition_text}"
            else:
                return "Погода недоступна"
    except Exception as e:
        print(f"Weather API error: {e}")
        return "Погода недоступна"


def translate_condition(condition: str) -> str:
    translations = {
        "clear": "ясно",
        "partly-cloudy": "малооблачно",
        "cloudy": "облачно",
        "overcast": "пасмурно",
        "drizzle": "морось",
        "light-rain": "лёгкий дождь",
        "rain": "дождь",
        "heavy-rain": "сильный дождь",
        "snow": "снег",
        "snowfall": "снегопад",
        "thunderstorm": "гроза",
        "hail": "град",
        "fog": "туман",
    }
    return translations.get(condition, condition)