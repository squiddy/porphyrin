import json
from io import StringIO
from unittest import mock

import pytest

from . import app
from .atc_catalog import AtcCode, convert_data


@pytest.fixture
def client():
    return app.test_client()


def test_atc_code_levels():
    code = AtcCode('C03CA01', 'name', None)
    assert code.first_level == 'C'
    assert code.second_level == '03'
    assert code.third_level == 'C'
    assert code.fourth_level == 'A'
    assert code.fifth_level == '01'


def test_atc_code_groups():
    catalog = mock.Mock()
    code = AtcCode('C03CA01', 'name', catalog)

    code.first_group
    catalog.lookup.assert_called_once_with('C')
    catalog.reset_mock()

    code.second_group
    catalog.lookup.assert_called_once_with('C03')
    catalog.reset_mock()

    code.third_group
    catalog.lookup.assert_called_once_with('C03C')
    catalog.reset_mock()

    code.fourth_group
    catalog.lookup.assert_called_once_with('C03CA')
    catalog.reset_mock()


def test_convert_data():
    source = StringIO('''
AB01432,,This is a test,,
CA014A2,,This is another test,,
    '''.strip())

    target = StringIO()
    convert_data(source, target)

    target.seek(0)
    assert json.load(target) == {
        'AB01432': 'This is a test',
        'CA014A2': 'This is another test'}


def test_index(client):
    rv = client.get('/')
    assert rv.status_code == 200


@mock.patch('porphyrin.views.catalog')
@mock.patch('porphyrin.views.naposapi')
def test_lookup(mock_napos, mock_catalog, client):
    mock_catalog.lookup.return_value = AtcCode('ABAAC01', 'name', mock_catalog)

    rv = client.get('/classification/lookup/?atc_code=ABAAC01')
    assert rv.status_code == 200
    mock_napos.lookup_classification.assert_called_once_with('ABAAC01')
    mock_catalog.lookup.assert_has_calls([
        mock.call('ABAAC01'),
        mock.call('A'),
        mock.call('A'),
        mock.call('ABA'),
        mock.call('ABA'),
        mock.call('ABAA'),
        mock.call('ABAA'),
        mock.call('ABAAC'),
        mock.call('ABAAC')
    ])