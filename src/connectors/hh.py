import requests
from typing import List, Dict
from src.abstract.api import Parser
from src.utils.cache import api_cache, CacheManager


class HeadHunterAPI(Parser):
    BASE_URL = 'https://api.hh.ru/vacancies'

    def __init__(self):
        self._last_params = None
        self.headers = {
            'User-Agent': 'MyApp/1.0 (my-app-feedback@example.com)',
            'Authorization': 'Bearer YOUR_ACCESS_TOKEN'  # Если используете OAuth
        }
        self.params = {
            'text': '',
            'page': 0,
            'per_page': 100,
            'area': 113  # Россия
        }

    @api_cache(ttl=1800)
    def get_vacancies(self, query: str, **kwargs) -> Dict:
        """Получить вакансии по запросу."""
        self.params['text'] = query
        try:
            response = requests.get(self.BASE_URL,
                                 headers=self.headers,
                                 params=self.params)
            print(f"API Response: {response.status_code}")  # Логирование
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Ошибка запроса к API: {e}")
            return {'items': []}  # Возвращаем пустой результат при ошибке

    def invalidate_cache(self):
        """Инвалидация кеша для текущего API."""
        CacheManager.invalidate_cache(self.get_vacancies.__name__)
