import requests
from typing import List, Dict
from src.abstract.api import Parser
from src.models.vacancy import Vacancy

from src.utils.cache import CacheManager

class HeadHunterAPI(Parser):
    """Класс для работы с API HeadHunter."""

    def __init__(self):
        self._last_params = None


    BASE_URL = 'https://api.hh.ru/vacancies'

    def __init__(self):
        self.headers = {'User-Agent': 'HH-User-Agent'}
        self.params = {
            'text': '',
            'page': 0,
            'per_page': 100,  # Максимум для HH
            'area': 113  # Россия
        }

    @api_cache(ttl=1800)
    def get_vacancies(self, query: str, **kwargs) -> List[Dict]:
        """Получить вакансии по запросу."""
        current_params = {"query": query, **kwargs}
        if self._last_params and self._last_params != current_params:
            self.invalidate_cache()
        self._last_params = current_params
        self.params['text'] = query
        vacancies = []

        while True:
            response = requests.get(self.BASE_URL, headers=self.headers, params=self.params)
            response.raise_for_status()  # Проверка на ошибки HTTP
            data = response.json()

            vacancies.extend(data.get('items', []))

            # Проверка на последнюю страницу
            if self.params['page'] >= data.get('pages', 1) - 1:
                break

            self.params['page'] += 1

        return vacancies

    def get_vacancies(self, query: str) -> List[Vacancy]:
        """Возвращает список объектов Vacancy."""
        raw_vacancies = self._fetch_raw_vacancies(query)
        return Vacancy.cast_to_object_list(raw_vacancies)

    def invalidate_cache(self):
        """Очистка кеша для этого API."""
        CacheManager.invalidate_cache("get_vacancies")
