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
            self.salary = {"from": None, "to": None, "currency": None}
        else:
            self.salary.setdefault("from", None)
            self.salary.setdefault("to", None)
            self.salary.setdefault("currency", None)

    def __gt__(self, other: 'Vacancy') -> bool:
        """Сравнение вакансий по минимальной зарплате."""
        return (self.salary.get('from') or 0) > (other.salary.get('from') or 0)

    def __lt__(self, other: 'Vacancy') -> bool:
        """Сравнение вакансий по максимальной зарплате."""
        return (self.salary.get('to') or 0) < (other.salary.get('to') or 0)

    @staticmethod
    def cast_from_sj(data: List[Dict]) -> List['Vacancy']:
        """Преобразование данных SuperJob в список Vacancy."""
        vacancies = []
        for item in data:
            vacancies.append(Vacancy(
                name=item.get('profession', ''),
                url=item.get('link', ''),
                salary={
                    'from': item.get('payment_from'),
                    'to': item.get('payment_to'),
                    'currency': item.get('currency', 'RUR')
                },
                description=item.get('candidat', ''),
                employer=item.get('client', {}).get('title', ''),
                published_at=item.get('date_published', 0)
            ))
        return vacancies


    @classmethod
    def cast_to_object_list(cls, data: List[Dict]) -> List['Vacancy']:
        """Преобразование списка словарей в список объектов Vacancy."""
        vacancies = []
        for item in data:
            try:
                vacancies.append(cls(
                    name=item.get('name', ''),
                    url=item.get('url', ''),
                    salary=item.get('salary', {'from': None, 'to': None, 'currency': None}),
                    description=item.get('description', ''),
                    employer=item.get('employer', {}).get('name', '') if isinstance(item.get('employer'),
                                                                                    dict) else item.get('employer', ''),
                    published_at=item.get('published_at', '')
                ))
            except ValueError as e:
                continue  # Пропускаем вакансии с невалидными данными
        return vacancies
