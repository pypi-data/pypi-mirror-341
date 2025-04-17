import pytest
import copy
import random

from typing import List, Generator, Union

from omniscript import Alarm, EngineStatus, OmniEngine, OmniId, find_alarm


@pytest.fixture(scope="module")
def default_alarm_list(engine: OmniEngine) -> Union[List[Alarm], None]:
    """ Default list of alarms on any engine """
    return engine.get_alarm_list()


@pytest.fixture(scope="function")
def alarm_list(engine: OmniEngine, default_alarm_list: List[Alarm]) -> Generator:
    """ Fixture to store default list of alarms. """
    yield default_alarm_list

    # Reset the alarm list with the original after every function call
    engine.set_alarm_list(default_alarm_list)


@pytest.fixture(scope="function")
def get_random_index(default_alarm_list: List[Alarm]) -> int:
    """ Fixture to return random index """
    return random.randint(0, len(default_alarm_list) - 1)


@pytest.fixture(scope="module")
def engine_status(engine: OmniEngine) -> EngineStatus:
    """ Current status of the engine. """
    return engine.get_status()


@pytest.mark.api
@pytest.mark.order(1)
def test_get_alarm_list(default_alarm_list: List[Alarm], engine_status: EngineStatus):
    """ Test for successful get of the list """
    num_alarms = len(default_alarm_list)
    expected_alarm_count = engine_status.alarm_count

    assert num_alarms == expected_alarm_count, (
        f'Failed default alarm list check. Expected {expected_alarm_count} got {num_alarms}')


@pytest.mark.api
@pytest.mark.order(2)
def test_add_alarm(engine: OmniEngine, default_alarm_list: List[Alarm], get_random_index: int):
    """ Test for adding an individual alarm. """
    new_alarm_name = 'Pytest New Alarm Name'
    new_alarm_id = OmniId(True)

    status = engine.get_status()
    initial_alarm_count = status.alarm_count

    alarm = copy.deepcopy(default_alarm_list[get_random_index])
    alarm.id = new_alarm_id
    alarm.name = new_alarm_name

    engine.add_alarm(alarm)
    status = engine.get_status()

    assert status.alarm_count > initial_alarm_count, 'Failed to add alarm.'

    alarm_get = engine.get_alarm(new_alarm_id)

    assert alarm_get, f'Failed to get new alarm: {new_alarm_name}'

    engine.delete_alarm(new_alarm_id)
    alarm_verify = engine.get_alarm(new_alarm_id)

    assert not alarm_verify, f'Failed to delete new alarm: {new_alarm_name}'


@pytest.mark.api
@pytest.mark.order(3)
def test_set_alarm_list(engine: OmniEngine, alarm_list: List[Alarm]):
    """ Test the setting of a new list of alarms """

    # Need an independent list so using deep copy. Only copy the first 30
    expected_list = copy.deepcopy(alarm_list[:30])
    expected_len = len(expected_list)

    engine.set_alarm_list(expected_list)

    actual_list = engine.get_alarm_list()
    actual_len = len(actual_list)

    assert expected_len == actual_len, (
        f'List lengths do not match: Expected -> {expected_len} vs Actual -> {actual_len}')

    for expected, actual in zip(expected_list, actual_list):
        assert expected == actual, f'Failed comparison check for {expected} and {actual}'


@pytest.mark.api
@pytest.mark.order(4)
def test_alarm_get(engine: OmniEngine, alarm_list: List[Alarm], get_random_index: int):
    """ Test the get for a single alarm using the ID and Alarm """

    expected_1 = alarm_list[get_random_index]
    actual_1 = engine.get_alarm(expected_1.id)

    assert expected_1 == actual_1, f'Failed comparison check for {expected_1} and {actual_1} by id'

    expected_2 = alarm_list[get_random_index]
    actual_2 = engine.get_alarm(expected_2)

    assert expected_2 == actual_2, (f'Failed comparison check for {expected_2} and '
                                    f'{actual_2} by Alarm')


@pytest.mark.api
@pytest.mark.order(5)
def test_alarm_modify(engine: OmniEngine, alarm_list: List[Alarm], get_random_index: int):
    """ Test the modification of an alarm in the list """

    expected_name = 'Pytest Modified Name'
    found = find_alarm(alarm_list, expected_name, 'name')
    if found:
        print(f'Found alarm: {found.name}')

    assert not found, f'Modified alarm already exists: {expected_name}'

    # Don't make a copy of a subset of alarm_list!
    # Otherwise the random index might be out of range.
    local_list = copy.deepcopy(alarm_list)

    expected = local_list[get_random_index]
    expected.name = expected_name

    engine.modify_alarm(expected)
    actual = engine.get_alarm(expected)

    # To assist in debugging this test.
    if expected.id != actual.id:
        pass

    assert expected == actual, f'Failed comparison check for {expected} and {actual}'


@pytest.mark.api
@pytest.mark.order(6)
def test_alarm_delete(engine: OmniEngine, alarm_list: List[Alarm], get_random_index: int):
    """ Test the deletion of an alarm in the list """

    alarm = alarm_list[get_random_index]

    engine.delete_alarm(alarm)
    found = engine.get_alarm(alarm)

    assert not found, f'Failed to delete alarm {alarm}'
