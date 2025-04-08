import pytest
from src.connectors.json_saver import JSONSaver
from src.models.vacancy import Vacancy
import os

@pytest.fixture
def sample_vacancy():
    return Vacancy(
        name="Python Developer",
        url="https://hh.ru/vacancy/123",
        salary={"from": 100000, "to": 150000, "currency": "RUR"},
        description="Описание",
        employer="Яндекс",
        published_at="2024-02-20T00:00:00+0300"
    )

@pytest.fixture
def json_saver(tmp_path):
    file_path = tmp_path / "vacancies.json"
    return JSONSaver(file_path=str(file_path))

def test_add_vacancy(json_saver, sample_vacancy):
    json_saver.add_vacancy(sample_vacancy)
    vacancies = json_saver.get_vacancies()
    assert len(vacancies) == 1
    assert vacancies[0].name == "Python Developer"

def test_delete_vacancy(json_saver, sample_vacancy):
    json_saver.add_vacancy(sample_vacancy)
    json_saver.delete_vacancy(sample_vacancy)
    assert len(json_saver.get_vacancies()) == 0

def test_filter_vacancies(json_saver, sample_vacancy):
    json_saver.add_vacancy(sample_vacancy)
    filtered = json_saver.get_vacancies({"salary_from": 90000})
    assert len(filtered) == 1
