import pytest
import json
from pathlib import Path
from typing import Dict, Any
from unittest.mock import Mock
from src.models.vacancy import Vacancy
from src.connectors.json_saver import JSONSaver


@pytest.fixture
def temp_json_file(tmp_path: Path) -> Path:
    """Фикстура для временного JSON-файла."""
    return tmp_path / "test_vacancies.json"


@pytest.fixture
def sample_vacancy() -> Vacancy:
    """Фикстура для тестовой вакансии."""
    return Vacancy(
        name="Python Developer",
        url="https://example.com/vacancy/1",
        salary={"from": 100000, "to": 150000, "currency": "RUR"},
        description="Test description",
        employer="Test Company",
        published_at="2024-02-20T14:19:36+0300"
    )


def test_json_saver_init(temp_json_file: Path) -> None:
    """Тест инициализации JSONSaver."""
    saver = JSONSaver(str(temp_json_file))
    assert saver.file_path == temp_json_file
    assert temp_json_file.parent.exists()


def test_add_vacancy(temp_json_file: Path, sample_vacancy: Vacancy) -> None:
    """Тест добавления вакансии."""
    saver = JSONSaver(str(temp_json_file))
    saver.add_vacancy(sample_vacancy)

    assert temp_json_file.exists()
    with open(temp_json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        assert len(data) == 1
        assert data[0]["name"] == "Python Developer"


def test_add_duplicate_vacancy(
        temp_json_file: Path,
        sample_vacancy: Vacancy
) -> None:
    """Тест добавления дублирующейся вакансии."""
    saver = JSONSaver(str(temp_json_file))
    saver.add_vacancy(sample_vacancy)
    saver.add_vacancy(sample_vacancy)

    with open(temp_json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        assert len(data) == 1


def test_get_vacancies(
        temp_json_file: Path,
        sample_vacancy: Vacancy
) -> None:
    """Тест получения вакансий."""
    saver = JSONSaver(str(temp_json_file))
    saver.add_vacancy(sample_vacancy)

    vacancies = saver.get_vacancies()
    assert len(vacancies) == 1
    assert isinstance(vacancies[0], Vacancy)
    assert vacancies[0].name == "Python Developer"

    filtered = saver.get_vacancies({"name": "Python Developer"})
    assert len(filtered) == 1

    filtered = saver.get_vacancies({"name": "Java Developer"})
    assert len(filtered) == 0


def test_delete_vacancy(
        temp_json_file: Path,
        sample_vacancy: Vacancy
) -> None:
    """Тест удаления вакансии."""
    saver = JSONSaver(str(temp_json_file))
    saver.add_vacancy(sample_vacancy)
    saver.delete_vacancy(sample_vacancy)

    with open(temp_json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        assert len(data) == 0


def test_save_and_load_filtered_vacancies(
        temp_json_file: Path,
        sample_vacancy: Vacancy
) -> None:
    """Тест сохранения и загрузки отфильтрованных вакансий."""
    saver = JSONSaver(str(temp_json_file))
    saver.add_vacancy(sample_vacancy)

    saver.save_filtered_vacancies([sample_vacancy], "filtered.json")
    filtered_file = temp_json_file.parent / "filtered.json"
    assert filtered_file.exists()

    loaded = saver.load_from_filtered("filtered.json")
    assert len(loaded) == 1
    assert isinstance(loaded[0], Vacancy)
