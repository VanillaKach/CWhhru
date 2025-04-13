import pytest
from unittest.mock import patch, Mock
from src.connectors.hh import HeadHunterAPI
from src.utils.cache import CacheManager


@pytest.fixture
def hh_api() -> HeadHunterAPI:
    """Фикстура для HeadHunterAPI."""
    return HeadHunterAPI()


def test_hh_api_init(hh_api: HeadHunterAPI) -> None:
    """Тест инициализации HeadHunterAPI."""
    assert hh_api.BASE_URL == 'https://api.hh.ru/vacancies'
    assert hh_api.headers == {'User-Agent': 'HH-User-Agent'}
    assert hh_api.params['area'] == 113


@patch('src.connectors.hh.requests.get')
def test_get_vacancies_success(
        mock_get: Mock,
        hh_api: HeadHunterAPI
) -> None:
    """Тест успешного получения вакансий."""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {'items': [{'id': '1', 'name': 'Python'}]}
    mock_get.return_value = mock_response

    result = hh_api.get_vacancies('Python')

    assert len(result) == 1
    assert result[0]['name'] == 'Python'
    mock_get.assert_called_once()


@patch('src.connectors.hh.requests.get')
def test_get_vacancies_failure(
    mock_get: Mock,
    hh_api: HeadHunterAPI
) -> None:
    """Тест обработки ошибки при запросе."""
    mock_get.side_effect = Exception('Connection error')
    # Перед тестом очищаем кеш, чтобы гарантировать свежий запрос
    CacheManager.invalidate_cache('get_vacancies')
    result = hh_api.get_vacancies('Python')
    assert result == []

def test_invalidate_cache(hh_api: HeadHunterAPI) -> None:
    """Тест инвалидации кеша."""
    CacheManager.caches['get_vacancies'] = Mock()
    hh_api.invalidate_cache()
    assert 'get_vacancies' in CacheManager.caches
