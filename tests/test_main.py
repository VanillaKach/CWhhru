import pytest
from main import filter_vacancies, get_vacancies_by_salary, sort_vacancies
from src.models.vacancy import Vacancy

@pytest.fixture
def sample_vacancies():
    return [
        Vacancy("Python", "url1", {"from": 100000, "to": 150000, "currency": "RUR"}, "Описание Python", "Яндекс", "2024-02-20"),
        Vacancy("Java", "url2", {"from": 90000, "to": 120000, "currency": "RUR"}, "Описание Java", "Google", "2024-02-19"),
    ]

def test_filter_vacancies(sample_vacancies):
    filtered = filter_vacancies(sample_vacancies, ["python"])
    assert len(filtered) == 1
    assert filtered[0].name == "Python"

def test_salary_filter(sample_vacancies):
    ranged = get_vacancies_by_salary(sample_vacancies, "100000-140000")
    assert len(ranged) == 1
    assert ranged[0].name == "Python"

def test_sort_vacancies(sample_vacancies):
    sorted_vacs = sort_vacancies(sample_vacancies)
    assert sorted_vacs[0].salary['from'] == 100000
