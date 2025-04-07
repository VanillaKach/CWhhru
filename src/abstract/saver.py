from abc import ABC, abstractmethod
from typing import List

class Saver(ABC):
    """Абстрактный класс для сохранения вакансий."""
    @abstractmethod
    def add_vacancy(self, vacancy: 'Vacancy') -> None:
        """Добавить вакансию в хранилище."""
        pass

    @abstractmethod
    def get_vacancies(self, criteria: dict) -> List['Vacancy']:
        """Получить вакансии по критериям."""
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy: 'Vacancy') -> None:
        """Удалить вакансию из хранилища."""
        pass
