from dataclasses import dataclass
from typing import Optional, Dict, List
import re


@dataclass
class Vacancy:
    """Класс для представления вакансии с валидацией данных."""
    name: str
    url: str
    salary: Dict[str, Optional[int]]  # {"from": 100, "to": 200, "currency": "RUR"}
    description: str
    employer: str
    published_at: str  # Дата в формате "2024-02-20T14:19:36+0300"

    def __post_init__(self):
        """Валидация данных после инициализации."""
        self._validate_url()
        self._validate_salary()

    def _validate_url(self):
        """Проверка корректности URL."""
        if not re.match(r'^https?://\S+', self.url):
            raise ValueError("Некорректный URL вакансии")

    def _validate_salary(self):
        """Проверка структуры зарплаты."""
        if not isinstance(self.salary, dict):
            raise ValueError("Зарплата должна быть словарём")

        if not all(k in self.salary for k in ["from", "to", "currency"]):
            self.salary = {"from": None, "to": None, "currency": None}

    def __gt__(self, other: 'Vacancy') -> bool:
        """Сравнение вакансий по минимальной зарплате."""
        return (self.salary.get('from') or 0) > (other.salary.get('from') or 0)

    def __lt__(self, other: 'Vacancy') -> bool:
        """Сравнение вакансий по максимальной зарплате."""
        return (self.salary.get('to') or 0) < (other.salary.get('to') or 0)

    @staticmethod
    def cast_to_object_list(data: List[Dict]) -> List['Vacancy']:
        """Преобразование JSON-данных в список объектов Vacancy."""
        vacancies = []
        for item in data:
            vacancy = Vacancy(
                name=item.get('name', 'Без названия'),
                url=item.get('alternate_url', ''),
                salary=item.get('salary', {}),
                description=f"{item.get('snippet', {}).get('requirement', '')}\n"
                            f"{item.get('snippet', {}).get('responsibility', '')}",
                employer=item.get('employer', {}).get('name', ''),
                published_at=item.get('published_at', '')
            )
            vacancies.append(vacancy)
        return vacancies
