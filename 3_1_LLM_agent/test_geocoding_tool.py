import unittest
from unittest.mock import patch
from geocoding_tool import GeocodingTool


class TestGeocodingTool(unittest.TestCase):
    def setUp(self):
        self.tool = GeocodingTool()

    @patch('geocoding_tool.requests.get')
    def test_geocode_success(self, mock_get):
        # Мокаем успешный ответ
        mock_get.return_value.json.return_value = [{'lat': '55.7558', 'lon': '37.6173'}]
        mock_get.return_value.status_code = 200

        lat, lon = self.tool.geocode("Москва")
        self.assertEqual(lat, 55.7558)
        self.assertEqual(lon, 37.6173)

    @patch('geocoding_tool.requests.get')
    def test_reverse_geocode_success(self, mock_get):
        # Мокаем успешный ответ для обратного геокодирования
        mock_get.return_value.json.return_value = {'display_name': 'Москва, Россия'}
        mock_get.return_value.status_code = 200

        address = self.tool.reverse_geocode(55.7558, 37.6173)
        self.assertEqual(address, 'Москва, Россия')

    @patch('geocoding_tool.requests.get')
    def test_geocode_not_found(self, mock_get):
        # Мокаем пустой ответ (место не найдено)
        mock_get.return_value.json.return_value = []
        mock_get.return_value.status_code = 200

        lat, lon = self.tool.geocode("UnknownPlace123")
        self.assertIsNone(lat)
        self.assertIsNone(lon)


if __name__ == '__main__':
    unittest.main()