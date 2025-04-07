import pytest
from src.models.vacancy import Vacancy
from datetime import datetime

def test_vacancy_creation():
    """Тест корректного создания вакансии."""
    vacancy = Vacancy(
        name="Python Developer",
        url="https://hh.ru/vacancy/123",
        salary={"from": 100000, "to": 150000, "currency": "RUR"},
        description="Требуется опыт...",
        employer="Яндекс",
        published_at="2024-02-20T14:19:36+0300"
    )
    assert vacancy.name == "Python Developer"

def test_salary_comparison():
    """Тест сравнения вакансий по зарплате."""
    v1 = Vacancy("A", "...", {"from": 100, "to": 200, "currency": "RUR"}, "...", "...", "...")
    v2 = Vacancy("B", "...", {"from": 150, "to": 300, "currency": "RUR"}, "...", "...", "...")
    assert v2 > v1
    assert v1 < v2

def test_invalid_url():
    """Тест валидации URL."""
    with pytest.raises(ValueError):
        Vacancy("A", "invalid_url", {"from": 100}, "...", "...", "...")
