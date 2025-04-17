import pytest
import copy
import random
import time

from typing import List, Generator

from omniscript import Filter, OmniEngine, AddressNode
from tests.Utils import exists


@pytest.fixture(scope="function")
def get_random_index(default_filter_list: List[Filter]) -> int:
    """ Fixture to return random index """
    return random.randint(0, len(default_filter_list) - 1)


@pytest.fixture(scope="function")
def filter_fixture(engine: OmniEngine, default_filter_list: List[Filter]) -> Generator:
    """ A changeable list of filters and tear down reset """
    yield default_filter_list

    # Reset the filter list with the original after every function call
    engine.set_filter_list(default_filter_list)


@pytest.fixture(scope="function")
def filter_string(host: str) -> str:
    """ Filter string fixture """
    return f'addr(ip: {host})'


@pytest.mark.skipif(not exists.data_directory_exists(),
                    reason='Cannot access non existent directory in repo -> src/data')
@pytest.mark.api
def test_get_filter_list(engine: OmniEngine, default_filter_list: List[Filter]):
    """ Test the get filter list command """
    assert default_filter_list == engine.get_filter_list(
        False), 'Get Filter List cache failure. Should not have refreshed'


@pytest.mark.skipif(not exists.data_directory_exists(),
                    reason='Cannot access non existent directory in repo -> src/data')
@pytest.mark.api
def test_filter_caching_small_timeout(default_filter_list: List[Filter], engine: OmniEngine):
    """ Test for filter caching with a list timeout """
    engine.set_filter_list_timeout(5)
    time.sleep(10)
    updated_filter_list = engine.get_filter_list(False)

    _ = set(default_filter_list) & set(updated_filter_list)

    assert len(set(default_filter_list) & set(updated_filter_list)) != len(default_filter_list), (
        'Get Filter List cache failure. Should have refreshed')


@pytest.mark.skipif(not exists.data_directory_exists(),
                    reason='Cannot access non existent directory in repo -> src/data')
@pytest.mark.api
def test_filter_caching_large_timeout(default_filter_list: List[Filter], engine: OmniEngine):
    """ Test for filter caching with a list large timeout """
    engine.set_filter_list_timeout(120)
    updated_filter_list = engine.get_filter_list()

    _ = set(default_filter_list) & set(updated_filter_list)

    assert len(set(default_filter_list) & set(updated_filter_list)) != len(default_filter_list), (
        'Get Filter List force refresh failure')


@pytest.mark.skipif(not exists.data_directory_exists(),
                    reason='Cannot access non existent directory in repo -> src/data')
@pytest.mark.api
def test_filter_get(engine: OmniEngine, filter_fixture: List[Filter], get_random_index: int):
    """ Test the get for a single alarm using the ID """

    expected = filter_fixture[get_random_index]
    actual = engine.get_filter(expected)

    assert expected == actual, f'Failed comparison check for {expected} and {actual}'


@pytest.mark.skipif(not exists.data_directory_exists(),
                    reason='Cannot access non existent directory in repo -> src/data')
@pytest.mark.api
def test_set_filter_list(engine: OmniEngine, filter_fixture: List[Filter]):
    """ Test the setting of a new list of filters """

    # Need an independent list so using deep copy. Only copy the first 30
    expected_list = copy.deepcopy(filter_fixture[:30])
    expected_len = len(expected_list)

    engine.set_filter_list(expected_list)

    actual_list = engine.get_filter_list()
    actual_len = len(actual_list)

    assert expected_len == actual_len, (
        f'List lengths do not match: Expected -> {expected_len} vs Actual -> {actual_len}')

    for expected, actual in zip(expected_list, actual_list):
        assert expected == actual, f'Failed comparison check for {expected} and {actual}'


@pytest.mark.skipif(not exists.data_directory_exists(),
                    reason='Cannot access non existent directory in repo -> src/data')
@pytest.mark.api
@pytest.mark.skip('Disabling all test. Deletes filters.')
def test_delete_filter_list(engine: OmniEngine, filter_fixture: List[Filter]):
    """ Test deleting entire filter list """

    _ = filter_fixture

    engine.delete_filter_list()

    assert not engine.get_filter_list(), 'Failed deletion of entire filter list'


@pytest.mark.skipif(not exists.data_directory_exists(),
                    reason='Cannot access non existent directory in repo -> src/data')
@pytest.mark.api
@pytest.mark.skip('Disabling all test. Deletes filter.')
def test_delete_single_filter(engine: OmniEngine, filter_fixture: List[Filter],
                              get_random_index: int):
    """ Test deleting a single filter """
    filter = filter_fixture[get_random_index]

    engine.delete_filter(filter)

    assert engine.get_filter(
        filter) is None, f'Failed to delete filter {filter}'


@pytest.mark.skipif(not exists.data_directory_exists(),
                    reason='Cannot access non existent directory in repo -> src/data')
@pytest.mark.api
def test_convert_filter_string(engine: OmniEngine, filter_fixture: List[Filter],
                               filter_string: str):
    """ Test the converting of a filter string to a filter object """
    _ = filter_fixture

    filter = engine.convert_filter_string(filter_string)

    assert filter is not None, 'Failed to convert filter'
    assert filter.criteria is not None, 'Failed to create filter node'
    assert filter.criteria._class_name == AddressNode._class_name, (
        'Failed to create address node filter from string')
