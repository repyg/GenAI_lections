import requests
from typing import Tuple, Optional


class GeocodingTool:
    """Класс для работы с геокодированием через OpenStreetMap Nominatim 📍"""

    def __init__(self):
        # Nominatim требует указания User-Agent для избежания блокировки
        self.base_url = "https://nominatim.openstreetmap.org"
        self.headers = {'User-Agent': 'MyGeocodingApp/1.0'}

    def geocode(self, place_name: str) -> Tuple[Optional[float], Optional[float]]:
        """Преобразует название места в координаты (широта, долгота)."""
        url = f"{self.base_url}/search"
        params = {'q': place_name, 'format': 'json', 'limit': 1}

        response = requests.get(url, params=params, headers=self.headers)
        response.raise_for_status()
        data = response.json()

        if data:
            return float(data[0]['lat']), float(data[0]['lon'])
        return None, None

    def reverse_geocode(self, lat: float, lon: float) -> Optional[str]:
        """Преобразует координаты (широта, долгота) в название места."""
        url = f"{self.base_url}/reverse"
        params = {'lat': lat, 'lon': lon, 'format': 'json'}

        response = requests.get(url, params=params, headers=self.headers)
        response.raise_for_status()
        data = response.json()

        return data.get('display_name')

    def use(self, query: str) -> str:
        lat, lon = self.geocode(query)
        if lat is not None and lon is not None:
            return f"Координаты места '{query}': широта {lat}, долгота {lon}"
        return f"Место '{query}' не найдено."