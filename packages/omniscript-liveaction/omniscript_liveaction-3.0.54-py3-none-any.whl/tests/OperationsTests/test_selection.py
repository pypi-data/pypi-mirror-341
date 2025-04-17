import pytest
import os
import time

from tests.Utils import exists
from typing import Generator, Union, List
from omniscript import (
    OmniEngine, ForensicSearch, ForensicTemplate, Selection, Filter, find_filter)


@pytest.fixture(scope="module")
def pcap(engine: OmniEngine, filesdir: str) -> Generator:
    """ Upload a pcap file and then delete when module is over """
    filename = 'fortworth101.pkt'
    path = os.path.abspath(os.path.join(exists.get_data_directory(), filename))

    assert os.path.exists(path), f'Test file {path} does not exist.'

    engine.send_file(path)
    yield filename

    engine.delete_file(filename)


@pytest.fixture(scope="module")
def forensic_search(engine: OmniEngine, pcap: str) -> Generator:
    """ Create a forensic search and then delete when module is over """

    # Use the pcap to start a forensic search
    template = ForensicTemplate()
    template.name = 'Pytest Forensic Search'
    template.option_packets = True
    template.option_indexing = True
    template.filename = pcap

    search = engine.create_forensic_search(template)

    # Minimum delay needed to finish creation of forensic search
    # To be removed once progress check is implemented within create forensic search
    time.sleep(0.5)

    yield search

    engine.delete_all_forensic_searches()


@pytest.fixture(scope="module")
def select_related(engine: OmniEngine, forensic_search: ForensicSearch) -> Union[Selection, None]:
    """ Start the select related """
    if forensic_search.id is not None:
        selection = engine.start_select_related(
            forensic_search.id, packets=[1], prefer_logical_addr=True,
            select_related_by=Selection.Select.Source)
        return selection


@pytest.fixture(scope="module")
def select_expert_related(engine: OmniEngine,
                          forensic_search: ForensicSearch) -> Union[Selection, None]:
    """ Start the expert select related """


@pytest.fixture(scope="module")
def filter_select_related(engine: OmniEngine,
                          forensic_search: ForensicSearch) -> Union[Selection, None]:
    """ Start the filtered select related """


@pytest.fixture(scope="module")
def select_related_filter_config(engine: OmniEngine, forensic_search: ForensicSearch,
                                 default_filter_list: List[Filter]) -> Union[Selection, None]:
    """ Start the select related with predefined filters """
    if forensic_search.id is not None:
        filter = find_filter(default_filter_list, 'HTTP', 'name')
        if filter is not None:
            selection = engine.start_select_related_filter_config(
                forensic_search.id, filters=[filter], mode=Selection.Mode.AcceptAll,
                first_packet_number=1, last_packet_number=2000
            )
            return selection


@pytest.fixture(scope="module")
def web_select_related(engine: OmniEngine,
                       forensic_search: ForensicSearch) -> Union[Selection, None]:
    """ Start the web select related """


@pytest.mark.dev
@pytest.mark.skip('Incomplete test')
# @pytest.mark.api
def test_select_related(engine: OmniEngine, select_related: Union[Selection, None]):
    """ Test for a select related operation """
    assert select_related is not None, 'Failed to start select related'

    select_related.results = engine.get_select_related_packets(
        select_related.task_id)

    assert select_related.packets, 'Failed due to empty list'


@pytest.mark.dev
@pytest.mark.skip('Incomplete test')
def test_expert_select_related(engine: OmniEngine, forensic_search):
    """ Test for an expert select related operation """


@pytest.mark.dev
@pytest.mark.skip('Incomplete test')
def test_filtered_select_related(engine: OmniEngine, forensic_search):
    """ Test for a filtered select related operation"""


@pytest.mark.dev
@pytest.mark.skip('Incomplete test')
# @pytest.mark.api
def test_select_related_filter_config(engine: OmniEngine,
                                      select_related_filter_config: Union[Selection, None]):
    """ Test for a select related with predefined filters operation"""
    assert select_related_filter_config is not None, (
        'Failed to start select related for filter config')

    select_related_filter_config.results = engine.get_select_related_filter_config_packets(
        select_related_filter_config.task_id)

    assert select_related_filter_config.packets, 'Failed due to empty list'


@pytest.mark.dev
@pytest.mark.skip('Incomplete test')
def test_web_select_related(engine: OmniEngine, forensic_search):
    """ Test for a web select related operation"""
