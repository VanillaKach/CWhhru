import pytest
from unittest.mock import patch, Mock
from typing import List, Dict, Any
from src.models.vacancy import Vacancy
from main import filter_vacancies, get_vacancies_by_salary, sort_vacancies


@pytest.fixture
def sample_vacancies() -> List[Vacancy]:
    """Фикстура для тестовых вакансий."""
    return [
        Vacancy(
            name="Python Developer",
            url="https://example.com/1",
            salary={"from": 100000, "to": 150000, "currency": "RUR"},
            description="Backend разработчик на Python",
            employer="Company A",
            published_at="2024-01-01"
        ),
        Vacancy(
            name="Java Developer",
            url="https://example.com/2",
            salary={"from": 120000, "to": None, "currency": "RUR"},
            description="Backend разработчик на Java",
            employer="Company B",
            published_at="2024-01-02"
        ),
        Vacancy(
            name="QA Engineer",
            url="https://example.com/3",
            salary={"from": None, "to": 100000, "currency": "RUR"},
            description="Тестировщик ПО",
            employer="Company C",
            published_at="2024-01-03"
        )
    ]


def test_filter_vacancies(sample_vacancies: List[Vacancy]) -> None:
    """Тест фильтрации вакансий по ключевым словам."""
    filtered = filter_vacancies(sample_vacancies, ["Python"])
    assert len(filtered) == 1
    assert filtered[0].name == "Python Developer"

    filtered = filter_vacancies(sample_vacancies, ["Developer"])
    assert len(filtered) == 2

    filtered = filter_vacancies(sample_vacancies, [])
    assert len(filtered) == 3


def test_get_vacancies_by_salary(sample_vacancies: List[Vacancy]) -> None:
    """Тест фильтрации вакансий по зарплате."""
    filtered = get_vacancies_by_salary(sample_vacancies, "100000-130000")
    # Ожидаем 3 вакансии
    assert len(filtered) == 3

    # Проверяем, что все вакансии пересекаются с диапазоном
    assert all(
        (v.salary.get('from') or 0) <= 130000 and
        (v.salary.get('to') or float('inf')) >= 100000
        for v in filtered
    )

    # Проверяем конкретные вакансии
    names = {v.name for v in filtered}
    assert "Python Developer" in names
    assert "Java Developer" in names
    assert "QA Engineer" in names

    filtered = get_vacancies_by_salary(sample_vacancies, "invalid-format")
    assert len(filtered) == 3


def test_sort_vacancies(sample_vacancies: List[Vacancy]) -> None:
    """Тест сортировки вакансий по зарплате."""
    sorted_vacancies = sort_vacancies(sample_vacancies)
    assert len(sorted_vacancies) == 3

    # Проверяем порядок сортировки по максимальной зарплате
    max_salaries = [
        max(v.salary.get('from') or 0, v.salary.get('to') or 0)
        for v in sorted_vacancies
    ]
    assert max_salaries == [150000, 120000, 100000]

    # Проверяем порядок имен
    assert sorted_vacancies[0].name == "Python Developer"
    assert sorted_vacancies[1].name == "Java Developer"
    assert sorted_vacancies[2].name == "QA Engineer"


@patch('main.HeadHunterAPI')
@patch('main.JSONSaver')
@patch('main.Vacancy.cast_to_object_list')
@patch('main.print_vacancies')
def test_user_interaction(
        mock_print: Mock,
        mock_cast: Mock,
        mock_saver: Mock,
        mock_hh: Mock,
        capsys: pytest.CaptureFixture[str]
) -> None:
    """Тест основного взаимодействия с пользователем."""
    from main import user_interaction

    mock_hh_instance = mock_hh.return_value
    mock_hh_instance.get_vacancies.return_value = [{"id": "1", "name": "Test"}]

    mock_cast.return_value = [
        Vacancy(
            name="Test",
            url="https://example.com",
            salary={"from": 100000, "to": 150000},
            description="",
            employer="",
            published_at=""
        )
    ]

    with patch('main.input', side_effect=["Python", "", "", "2"]):
        user_interaction()

    mock_hh_instance.get_vacancies.assert_called_once_with("Python")
    mock_cast.assert_called_once()
    mock_print.assert_called_once()

    captured = capsys.readouterr()
    assert "Найдено вакансий: 1" in captured.out
