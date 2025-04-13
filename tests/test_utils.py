import pytest
from unittest.mock import Mock
from typing import Any, Dict
from src.utils.cache import CacheManager, api_cache, _generate_key


def test_cache_manager_singleton() -> None:
    """Тест паттерна Singleton для CacheManager."""
    instance1 = CacheManager()
    instance2 = CacheManager()
    assert instance1 is instance2


def test_cache_manager_get_cache() -> None:
    """Тест получения кеша."""
    CacheManager.caches['test_func'] = 'test_cache'
    assert CacheManager.get_cache('test_func') == 'test_cache'
    assert CacheManager.get_cache('non_existent') is None


def test_cache_manager_invalidate_cache() -> None:
    """Тест инвалидации кеша."""
    mock_cache1 = Mock()
    mock_cache2 = Mock()
    CacheManager.caches = {
        'func1': mock_cache1,
        'func2': mock_cache2
    }

    CacheManager.invalidate_cache('func1')
    mock_cache1.clear.assert_called_once()
    mock_cache2.clear.assert_not_called()

    CacheManager.invalidate_cache()
    assert mock_cache1.clear.call_count == 2
    assert mock_cache2.clear.call_count == 1


def test_api_cache_decorator() -> None:
    """Тест декоратора api_cache."""
    mock_func = Mock(return_value='result')
    mock_func.__name__ = 'test_func'

    decorated_func = api_cache(ttl=60)(mock_func)
    result1 = decorated_func('arg1', kwarg='value')
    result2 = decorated_func('arg1', kwarg='value')

    assert result1 == 'result'
    assert result2 == 'result'
    mock_func.assert_called_once()


def test_generate_key() -> None:
    """Тест генерации ключа кеша."""
    args = ('arg1', 'arg2')
    kwargs = {'kwarg1': 'value1', 'kwarg2': 'value2'}
    key = _generate_key(args, kwargs)

    assert key == _generate_key(args, kwargs)
    kwargs_reversed = {'kwarg2': 'value2', 'kwarg1': 'value1'}
    assert key == _generate_key(args, kwargs_reversed)
