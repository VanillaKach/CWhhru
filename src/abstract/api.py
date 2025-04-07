from abc import ABC, abstractmethod
from typing import List, Dict

class Parser(ABC):
    """Абстрактный класс для работы с API вакансий."""
    @abstractmethod
    def get_vacancies(self, query: str) -> List[Dict]:
        """Получить вакансии по запросу."""
        pass
