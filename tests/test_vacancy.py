import pytest
from datetime import datetime
from typing import Dict, Any
from src.models.vacancy import Vacancy


def test_vacancy_creation() -> None:
    """Тест создания вакансии с валидными данными."""
    vacancy_data = {
        "name": "Python Developer",
        "url": "https://example.com/vacancy/1",
        "salary": {"from": 100000, "to": 150000, "currency": "RUR"},
        "description": "Backend разработчик на Python",
        "employer": "Test Company",
        "published_at": "2024-02-20T14:19:36+0300"
    }

    vacancy = Vacancy(**vacancy_data)

    assert vacancy.name == "Python Developer"
    assert vacancy.url == "https://example.com/vacancy/1"
    assert vacancy.salary == {"from": 100000, "to": 150000, "currency": "RUR"}
    assert vacancy.description == "Backend разработчик на Python"
    assert vacancy.employer == "Test Company"
    assert vacancy.published_at == "2024-02-20T14:19:36+0300"


def test_vacancy_with_invalid_url() -> None:
    """Тест создания вакансии с невалидным URL."""
    with pytest.raises(ValueError):
        Vacancy(
            name="Test",
            url="invalid-url",
            salary={},
            description="",
            employer="",
            published_at=""
        )


def test_vacancy_with_partial_salary() -> None:
    """Тест создания вакансии с частичной информацией о зарплате."""
    vacancy = Vacancy(
        name="Test",
        url="https://example.com",
        salary={"from": 100000},
        description="",
        employer="",
        published_at=""
    )

    assert vacancy.salary == {"from": 100000, "to": None, "currency": None}


def test_vacancy_comparison() -> None:
    """Тест сравнения вакансий по зарплате."""
    v1 = Vacancy(
        name="Junior",
        url="https://example.com/1",
        salary={"from": 50000, "to": 80000},
        description="",
        employer="",
        published_at=""
    )

    v2 = Vacancy(
        name="Middle",
        url="https://example.com/2",
        salary={"from": 100000, "to": 150000},
        description="",
        employer="",
        published_at=""
    )

    assert v2 > v1
    assert v1 < v2


def test_cast_to_object_list() -> None:
    """Тест преобразования списка словарей в список объектов Vacancy."""
    data = [
        {
            "name": "Python Developer",
            "url": "https://example.com/1",
            "salary": {"from": 100000, "to": 150000, "currency": "RUR"},
            "description": "Test",
            "employer": "Company",
            "published_at": "2024-02-20T14:19:36+0300"
        },
        {
            "name": "Java Developer",
            "url": "https://example.com/2",
            "salary": {"from": 120000, "to": None, "currency": "RUR"},
            "description": "Test",
            "employer": {"name": "Company"},
            "published_at": "2024-02-20T14:19:36+0300"
        }
    ]

    vacancies = Vacancy.cast_to_object_list(data)

    assert len(vacancies) == 2
    assert isinstance(vacancies[0], Vacancy)
    assert isinstance(vacancies[1], Vacancy)
    assert vacancies[0].name == "Python Developer"
    assert vacancies[1].employer == "Company"
