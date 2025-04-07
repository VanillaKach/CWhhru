from src.connectors.hh import HeadHunterAPI
from src.connectors.json_saver import JSONSaver
from src.models.vacancy import Vacancy
from typing import List, Optional

import logging

def user_interaction():
    """Функция для взаимодействия с пользователем через консоль."""
    print("🔍 Поиск вакансий на HeadHunter")

    # Инициализация компонентов
    hh_api = HeadHunterAPI()
    json_saver = JSONSaver()

    # Шаг 1: Поисковый запрос
    search_query = input("Введите поисковый запрос (например, 'Python разработчик'): ")
    vacancies = hh_api.get_vacancies(search_query)
    json_saver._write_file([v.__dict__ for v in vacancies])  # Сохраняем сырые данные

    # Шаг 2: Фильтрация по ключевым словам
    filter_words = input("Введите ключевые слова для фильтрации (через пробел): ").split()
    filtered_vacancies = filter_vacancies(vacancies, filter_words)

    # Шаг 3: Фильтрация по зарплате
    salary_range = input("Введите диапазон зарплат (например, '100000-150000'): ")
    ranged_vacancies = get_vacancies_by_salary(filtered_vacancies, salary_range)

    # Шаг 4: Сортировка и вывод топа N
    top_n = int(input("Введите количество вакансий для вывода (топ N): "))
    sorted_vacancies = sort_vacancies(ranged_vacancies)
    print_vacancies(sorted_vacancies[:top_n])

    cache_management(platform)


def filter_vacancies(vacancies: List[Vacancy], filter_words: List[str]) -> List[Vacancy]:
    """Фильтрация вакансий по ключевым словам в описании."""
    if not filter_words:
        return vacancies

    filtered = []
    for vacancy in vacancies:
        description = f"{vacancy.name} {vacancy.description}".lower()
        if all(word.lower() in description for word in filter_words):
            filtered.append(vacancy)
    return filtered


def get_vacancies_by_salary(vacancies: List[Vacancy], salary_range: str) -> List[Vacancy]:
    """Фильтрация вакансий по диапазону зарплат."""
    if not salary_range:
        return vacancies

    try:
        min_salary, max_salary = map(int, salary_range.split('-'))
    except ValueError:
        return vacancies

    ranged = []
    for vacancy in vacancies:
        salary_from = vacancy.salary.get('from') or 0
        salary_to = vacancy.salary.get('to') or float('inf')
        if min_salary <= salary_from <= max_salary or min_salary <= salary_to <= max_salary:
            ranged.append(vacancy)
    return ranged


def sort_vacancies(vacancies: List[Vacancy]) -> List[Vacancy]:
    """Сортировка вакансий по убыванию зарплаты."""
    return sorted(vacancies, reverse=True)


def print_vacancies(vacancies: List[Vacancy]) -> None:
    """Вывод вакансий в консоль."""
    if not vacancies:
        print("❌ Нет вакансий, соответствующих критериям.")
        return

    print("\n📋 Результаты поиска:")
    for i, vacancy in enumerate(vacancies, 1):
        salary_from = vacancy.salary.get('from', 'Не указана')
        salary_to = vacancy.salary.get('to', 'Не указана')
        print(
            f"{i}. {vacancy.name}\n"
            f"   💰 Зарплата: {salary_from} - {salary_to} {vacancy.salary.get('currency', '')}\n"
            f"   🏢 Работодатель: {vacancy.employer}\n"
            f"   🔗 Ссылка: {vacancy.url}\n"
            f"   📅 Дата публикации: {vacancy.published_at[:10]}\n"
        )

def get_valid_input(prompt: str, input_type=str, default=None):
    while True:
        try:
            user_input = input(prompt)
            if not user_input and default is not None:
                return default
            return input_type(user_input)
        except ValueError:
            print("❌ Ошибка ввода. Попробуйте снова.")

logging.basicConfig(filename='app.log', level=logging.INFO)

def cache_management(api):
    """Меню управления кешем."""
    print("\n🔄 Управление кешем:")
    print("1. Очистить кеш текущего API")
    print("2. Очистить все кеши")
    choice = input("> ")

    if choice == "1":
        api.invalidate_cache()
        print("✅ Кеш API очищен")
    elif choice == "2":
        from src.utils.cache import CacheManager
        CacheManager.invalidate_cache()
        print("✅ Все кеши очищены")

if __name__ == "__main__":
    user_interaction()
