import pytest
import time
from omniscript import omniscript, PeekTime


@pytest.fixture(scope='module')
def peek_time_iso():
    """ Peek time strings ISO function fixture """
    peek_time_str_arr = [
        '2022-08-30T00:08:18.105796123Z',
        '2022-08-30T00:08:18.105796123',
        '2022-08-30T00:08:18.105796Z',
        '2022-08-30T00:08:18.105796',
        '2022-08-30T00:08:18.105796987Z',
        '2022-08-30T00:08:18.105796987-0700',
        '2022-08-30T00:08:18.105796987-07:00',
        '2022-08-30T00:08:18.105796987-07',
        '2022-08-30T08:08:18.105796987+0800',
        '2022-08-30T08:08:18.105796987+08:00',
        '2022-08-30T08:08:18.105796987+08'
    ]
    peek_time_iso_str_arr = [
        '2022-08-30T00:08:18.105796123Z',
        '2022-08-30T00:08:18.105796123Z',
        '2022-08-30T00:08:18.105796000Z',
        '2022-08-30T00:08:18.105796000Z',
        '2022-08-30T00:08:18.105796987Z',
        '2022-08-30T07:08:18.105796987Z',
        '2022-08-30T07:08:18.105796987Z',
        '2022-08-30T07:08:18.105796987Z',
        '2022-08-30T00:08:18.105796987Z',
        '2022-08-30T00:08:18.105796987Z',
        '2022-08-30T00:08:18.105796987Z'
    ]
    yield peek_time_str_arr, peek_time_iso_str_arr


@pytest.mark.smoke
def test_peek_time():
    """ Testing the PeekTime """
    peek_time0 = omniscript.PeekTime()
    time.sleep(2)
    peek_time1 = omniscript.PeekTime()
    time_diff = peek_time1 - peek_time0

    assert time_diff.value <= 10 * 1000000000, 'Failure in PeekTime subtraction'


@pytest.mark.smoke
def test_peek_time_iso(peek_time_iso):
    """ Testing the PeekTime ISO """
    peek_str_arr, iso_str_arr = peek_time_iso
    for (peek_str, iso_str) in zip(peek_str_arr, iso_str_arr):
        try:
            peek_time0 = PeekTime(peek_str)
            peek_time_iso = peek_time0.iso_time()

            assert peek_time_iso == iso_str, f'Failure to match peek time for {peek_str}'
        except Exception:
            assert False, f'PeekTime failed to parse: {peek_str}'
