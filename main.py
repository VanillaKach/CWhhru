import logging
from typing import List

from src.connectors.hh import HeadHunterAPI
from src.connectors.json_saver import JSONSaver
from src.models.vacancy import Vacancy


def setup_logging():
    """Настройка логирования."""
    logging.basicConfig(
        filename="app.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        encoding="utf-8",
    )


def get_valid_input(prompt: str, input_type=str, default=None):
    """Получение и валидация ввода пользователя."""
    while True:
        try:
            user_input = input(prompt)
            if not user_input and default is not None:
                return default
            return input_type(user_input)
        except ValueError:
            print("❌ Ошибка ввода. Попробуйте снова.")


def filter_vacancies(
    vacancies: List[Vacancy], filter_words: List[str]
) -> List[Vacancy]:
    """Фильтрация вакансий по ключевым словам."""
    if not filter_words:
        return vacancies

    filtered = []
    for vacancy in vacancies:
        description = f"{vacancy.name} {vacancy.description}".lower()
        if all(word.lower() in description for word in filter_words):
            filtered.append(vacancy)
    return filtered


def get_vacancies_by_salary(
        vacancies: List[Vacancy],
        salary_range: str
) -> List[Vacancy]:
    """Фильтрация вакансий по зарплате."""
    if not salary_range:
        return vacancies

    try:
        min_salary, max_salary = map(int, salary_range.split("-"))
    except ValueError:
        return vacancies

    ranged = []
    for vacancy in vacancies:
        salary_from = vacancy.salary.get("from")
        salary_to = vacancy.salary.get("to")

        # Если зарплата не указана, пропускаем вакансию
        if salary_from is None and salary_to is None:
            continue

        # Приводим None к 0 для сравнения
        salary_from = salary_from or 0
        salary_to = salary_to or 0

        # Проверяем, что хотя бы одна граница зарплаты попадает в диапазон
        if (min_salary <= salary_from <= max_salary) or \
                (min_salary <= salary_to <= max_salary):
            ranged.append(vacancy)

    return ranged


def sort_vacancies(vacancies: List[Vacancy]) -> List[Vacancy]:
    """Сортировка вакансий по максимальной зарплате (по убыванию)."""
    return sorted(
        vacancies,
        key=lambda v: max(v.salary.get('from') or 0, v.salary.get('to') or 0),
        reverse=True
    )


def print_vacancies(vacancies: List[Vacancy]) -> None:
    """Вывод вакансий."""
    if not vacancies:
        print("❌ Нет вакансий, соответствующих критериям.")
        return

    print("\n📋 Результаты поиска:")
    for i, vacancy in enumerate(vacancies, 1):
        salary_from = vacancy.salary.get("from", "Не указана")
        salary_to = vacancy.salary.get("to", "Не указана")
        currency = vacancy.salary.get("currency", "")

        salary_info = (
            f"{salary_from} - {salary_to} {currency}"
            if currency
            else "Зарплата не указана"
        )

        print(
            f"{i}. {vacancy.name}\n"
            f"   💰 {salary_info}\n"
            f"   🏢 {vacancy.employer}\n"
            f"   🔗 {vacancy.url}\n"
            f"   📅 {vacancy.published_at[:10]}\n"
        )


def user_interaction():
    """Основная функция взаимодействия с пользователем."""
    setup_logging()
    logging.info("Запуск программы")

    try:
        hh_api = HeadHunterAPI()
        json_saver = JSONSaver()

        # Получение вакансий
        search_query = get_valid_input(
            "Введите поисковый запрос (например, 'Python разработчик'): ", str, "Python"
        )

        raw_vacancies = hh_api.get_vacancies(search_query)
        print(f"Найдено вакансий: {len(raw_vacancies)}")  # Для отладки

        if not raw_vacancies:
            print("⚠️ API не вернуло вакансии. Попробуйте другой запрос.")
            return

        vacancies = Vacancy.cast_to_object_list(raw_vacancies)
        logging.info(f"Получено {len(vacancies)} вакансий")

        # Сохранение вакансий
        for vacancy in vacancies:
            json_saver.add_vacancy(vacancy)

        # Фильтрация
        filter_words = input(
            "Введите ключевые слова для фильтрации (через пробел, оставьте пустым чтобы пропустить): "
        ).split()
        filtered_vacancies = filter_vacancies(vacancies, filter_words)

        # Фильтрация по зарплате
        salary_range = input(
            "Введите диапазон зарплат (например, '100000-150000', оставьте пустым чтобы пропустить): "
        )
        ranged_vacancies = get_vacancies_by_salary(filtered_vacancies, salary_range)

        # Сортировка и вывод
        top_n = get_valid_input(
            "Введите количество вакансий для вывода (топ N, по умолчанию 10): ", int, 10
        )
        sorted_vacancies = sort_vacancies(ranged_vacancies)
        print_vacancies(sorted_vacancies[:top_n])

    except Exception as e:
        logging.error(f"Ошибка: {str(e)}", exc_info=True)
        print(f"❌ Произошла ошибка: {str(e)}")
    finally:
        logging.info("Завершение работы программы")


if __name__ == "__main__":
    user_interaction()
