import json
import logging
from typing import List, Dict, Any, Optional
from pathlib import Path
from src.abstract.saver import Saver
from src.models.vacancy import Vacancy


class JSONSaver(Saver):
    """Класс для сохранения вакансий в JSON-файл."""

    def __init__(self, file_path: str = "data/vacancies.json") -> None:
        """Инициализация с указанием пути к файлу."""
        self.file_path = Path(file_path)
        self.file_path.parent.mkdir(exist_ok=True)

    def _read_file(self) -> List[Dict[str, Any]]:
        """Чтение данных из файла."""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _write_file(self, data: List[Dict[str, Any]]) -> None:
        """Запись данных в файл."""
        with open(self.file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=2, ensure_ascii=False)

    def add_vacancy(self, vacancy: Vacancy) -> None:
        """Добавить вакансию в файл с проверкой на дубликаты."""
        try:
            vacancies = self._read_file()
            if not isinstance(vacancies, list):  # Защита от неправильного формата
                vacancies = []

            # Проверяем, есть ли уже такая вакансия (по URL)
            if any(v.get('url') == vacancy.url for v in vacancies):
                return

            vacancies.append({
                "name": vacancy.name,
                "url": vacancy.url,
                "salary": vacancy.salary,
                "description": vacancy.description,
                "employer": vacancy.employer,
                "published_at": vacancy.published_at
            })
            self._write_file(vacancies)
        except (IOError, OSError) as e:
            logging.error("Ошибка при добавлении вакансии: %s", str(e))
            raise

    def get_vacancies(self, criteria: Optional[Dict[str, Any]] = None) -> List[Vacancy]:
        """Получить вакансии по критериям."""
        raw_vacancies = self._read_file()
        if not criteria:
            return Vacancy.cast_to_object_list(raw_vacancies)

        filtered = []
        for vacancy in raw_vacancies:
            match = True
            for key, value in criteria.items():
                if key == "salary_from":
                    if (vacancy["salary"].get("from") or 0) < value:
                        match = False
                elif vacancy.get(key) != value:
                    match = False
            if match:
                filtered.append(vacancy)

        return Vacancy.cast_to_object_list(filtered)

    def delete_vacancy(self, vacancy: Vacancy) -> None:
        """Удалить вакансию из файла."""
        vacancies = self._read_file()
        updated = [v for v in vacancies if v["url"] != vacancy.url]
        self._write_file(updated)

    def save_filtered_vacancies(
        self,
        vacancies: List[Vacancy],
        filename: str = "filtered_vacancies.json"
    ) -> None:
        """Сохранить отфильтрованные вакансии в отдельный файл."""
        path = self.file_path.parent / filename
        try:
            with open(path, 'w', encoding='utf-8') as file:
                data = [v.__dict__ for v in vacancies]
                json.dump(data, file, indent=2, ensure_ascii=False)
        except (IOError, OSError) as e:
            logging.error("Ошибка при сохранении файла: %s", str(e))
            raise

    def load_from_filtered(self, filename: str) -> List[Vacancy]:
        """Загрузить вакансии из файла с фильтрацией."""
        path = self.file_path.parent / filename
        try:
            with open(path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                return Vacancy.cast_to_object_list(data)
        except FileNotFoundError:
            return []
        except json.JSONDecodeError as e:
            logging.error("Ошибка при чтении файла: %s", str(e))
            return []
