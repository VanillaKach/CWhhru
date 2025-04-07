import pytest
from src.connectors.hh import HeadHunterAPI
from unittest.mock import patch


@patch('requests.get')
def test_get_vacancies(mock_get):
    mock_response = {
        'items': [{'name': 'Python Developer'}],
        'pages': 1
    }
    mock_get.return_value.json.return_value = mock_response

    api = HeadHunterAPI()
    result = api.get_vacancies('Python')

    assert len(result) == 1
    assert result[0]['name'] == 'Python Developer'
