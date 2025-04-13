import requests
from typing import List, Dict, Any, Optional
from src.abstract.api import Parser
from src.utils.cache import api_cache, CacheManager


class HeadHunterAPI(Parser):
    """Класс для работы с API HeadHunter."""
    BASE_URL = 'https://api.hh.ru/vacancies'

    def __init__(self) -> None:
        """Инициализация API с параметрами по умолчанию."""
        self._last_params: Optional[Dict[str, Any]] = None
        self.headers = {'User-Agent': 'HH-User-Agent'}
        self.params = {
            'text': '',
            'page': 0,
            'per_page': 100,
            'area': 113  # Россия
        }

    @api_cache(ttl=1800)
    def get_vacancies(self, query: str, **kwargs: Any) -> List[Dict[str, Any]]:
        """Получить вакансии по запросу."""
        self.params['text'] = query
        try:
            response = requests.get(
                self.BASE_URL,
                headers=self.headers,
                params=self.params,
                timeout=10
            )
            response.raise_for_status()
            return response.json().get('items', [])
        except Exception as e:
            # Принудительно инвалидируем кеш при ошибке
            CacheManager.invalidate_cache(self.get_vacancies.__name__)
            # Возвращаем пустой список, как ожидает тест
            return []

    def invalidate_cache(self) -> None:
        """Инвалидация кеша для текущего API."""
        CacheManager.invalidate_cache(self.get_vacancies.__name__)
