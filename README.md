# Парсер вакансий с HeadHunter (hh.ru)

Проект представляет собой консольное приложение для поиска, фильтрации и управления вакансиями с платформы hh.ru.

## 📌 Основные возможности

- Получение вакансий с API HeadHunter по заданным параметрам
- Сохранение вакансий в JSON-файл
- Фильтрация вакансий по:
  - Ключевым словам
  - Зарплатному диапазону
  - Работодателю
- Сортировка вакансий по зарплате
- Удаление вакансий
- Кеширование запросов к API
- Логирование операций

## 🛠 Технологии

- Python 3.12+
- Библиотеки:
  - `requests` - для работы с API
  - `cachetools` - для кеширования
  - `pydantic` (через dataclasses) - для валидации данных
  - `pytest` - для тестирования

## ⚙️ Установка и запуск

1. Клонируйте репозиторий:
```bash
git clone https://github.com/yourusername/hh-parser.git
cd hh-parser
Установите зависимости:

bash
Copy
pip install -r requirements.txt
Запустите приложение:

bash
Copy
python main.py
🏗 Структура проекта
Copy
hh-parser/
├── data/                    # Каталог для хранения данных
│   └── vacancies.json       # Файл с сохраненными вакансиями
├── src/
│   ├── abstract/            # Абстрактные классы
│   ├── connectors/          # Классы для работы с API и файлами
│   ├── models/              # Модели данных
│   └── utils/               # Вспомогательные утилиты
├── tests/                   # Тесты
├── main.py                  # Основной скрипт
└── README.md                # Документация
🔧 Основные модули
hh.py
Класс для работы с API HeadHunter:

Поиск вакансий

Кеширование запросов

Обработка ошибок

json_saver.py
Класс для работы с файлами:

Сохранение вакансий в JSON

Чтение вакансий из файла

Фильтрация и удаление вакансий

vacancy.py
Модель вакансии с:

Валидацией данных

Методами сравнения вакансий

Преобразованием данных из API

cache.py
Система кеширования:

TTLCache с временем жизни

Инвалидация кеша

Thread-safe реализация

🧪 Тестирование
Для запуска тестов:

bash
Copy
pytest tests/
Тесты покрывают:

Работу с API

Фильтрацию и сортировку

Валидацию данных

Кеширование

============================ test session starts ============================
platform linux -- Python 3.12.3, pytest-7.4.4, pluggy-1.5.0 -- /home/ubuvan/Py/CWhhru/.venv/bin/python
cachedir: .pytest_cache
rootdir: /home/ubuvan/Py/CWhhru
configfile: pytest.ini
testpaths: tests
plugins: cov-4.1.0
collected 24 items                                                          

tests/test_hh_api.py::test_hh_api_init PASSED                         [  4%]
tests/test_hh_api.py::test_get_vacancies_success PASSED               [  8%]
tests/test_hh_api.py::test_get_vacancies_failure PASSED               [ 12%]
tests/test_hh_api.py::test_invalidate_cache PASSED                    [ 16%]
tests/test_json_saver.py::test_json_saver_init PASSED                 [ 20%]
tests/test_json_saver.py::test_add_vacancy PASSED                     [ 25%]
tests/test_json_saver.py::test_add_duplicate_vacancy PASSED           [ 29%]
tests/test_json_saver.py::test_get_vacancies PASSED                   [ 33%]
tests/test_json_saver.py::test_delete_vacancy PASSED                  [ 37%]
tests/test_json_saver.py::test_save_and_load_filtered_vacancies PASSED [ 41%]
tests/test_main.py::test_filter_vacancies PASSED                      [ 45%]
tests/test_main.py::test_get_vacancies_by_salary PASSED               [ 50%]
tests/test_main.py::test_sort_vacancies PASSED                        [ 54%]
tests/test_main.py::test_user_interaction PASSED                      [ 58%]
tests/test_utils.py::test_cache_manager_singleton PASSED              [ 62%]
tests/test_utils.py::test_cache_manager_get_cache PASSED              [ 66%]
tests/test_utils.py::test_cache_manager_invalidate_cache PASSED       [ 70%]
tests/test_utils.py::test_api_cache_decorator PASSED                  [ 75%]
tests/test_utils.py::test_generate_key PASSED                         [ 79%]
tests/test_vacancy.py::test_vacancy_creation PASSED                   [ 83%]
tests/test_vacancy.py::test_vacancy_with_invalid_url PASSED           [ 87%]
tests/test_vacancy.py::test_vacancy_with_partial_salary PASSED        [ 91%]
tests/test_vacancy.py::test_vacancy_comparison PASSED                 [ 95%]
tests/test_vacancy.py::test_cast_to_object_list PASSED                [100%]

---------- coverage: platform linux, python 3.12.3-final-0 -----------


📄 Логирование
Приложение ведет логи в файл app.log с информацией:

О запуске и завершении работы

Об ошибках

О количестве полученных вакансий

📝 Пример использования
Запустите приложение

Введите поисковый запрос (например "Python разработчик")

При необходимости укажите фильтры:

Ключевые слова

Диапазон зарплат

Просмотрите результаты

Вакансии автоматически сохранятся в файл

📈 Планы по развитию
Добавление поддержки других платформ (SuperJob, Rabota.ru)

Реализация графического интерфейса

Добавление системы уведомлений о новых вакансиях

Интеграция с базами данных

🤝 Участие в проекте
PR и предложения приветствуются! Перед внесением изменений:

Создайте issue с описанием идеи

Сделайте fork проекта

Создайте отдельную ветку для ваших изменений

Отправьте PR

📜 Лицензия
MIT License