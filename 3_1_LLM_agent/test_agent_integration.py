import unittest
from unittest.mock import patch
from llm_agent.core_v2 import LLMAgent


class TestLLMAgentIntegration(unittest.TestCase):

    @patch('llm_agent.core_v2.LLMAgent._make_api_request')
    @patch('geocoding_tool.requests.get')
    def test_agent_with_geocoding_tool(self, mock_osm_get, mock_llm_request):
        # 1. Мокаем ответ от OpenStreetMap API
        mock_osm_get.return_value.status_code = 200
        mock_osm_get.return_value.json.return_value = [{'lat': '55.7558', 'lon': '37.6173'}]

        # 2. Могаем ответы от LLM (Ollama)
        # Первый вызов - это планирование. Второй вызов - генерация финального ответа.
        mock_llm_request.side_effect = [
            {
                "choices": [{
                    "message": {
                        "content": '{"plan": [{"action": "geocoding", "input": "Москва"}]}'
                    }
                }]
            },
            {
                "choices": [{
                    "message": {
                        "content": "Координаты Москвы: широта 55.7558, долгота 37.6173."
                    }
                }]
            }
        ]

        # 3. Инициализируем агента и запускаем процесс
        agent = LLMAgent(local=True, ollama_model="qwen3.5:2b")
        response = agent.process_query("Найти координаты Москвы")

        # 4. Проверяем, что агент корректно отработал план и вернул нужные данные
        self.assertIn("55.7558", response)
        self.assertEqual(mock_llm_request.call_count, 2)
        mock_osm_get.assert_called_once()


if __name__ == '__main__':
    unittest.main()