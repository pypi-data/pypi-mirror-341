import pytest
import random

from typing import List

from omniscript.protocoltranslation import ProtocolTranslation
from omniscript import OmniEngine, get_id_protocol_names
from tests.Utils import exists


@pytest.fixture(scope="function")
def translation_list(engine: OmniEngine):
    """ List of protocol translations"""
    list_ = []
    for _, member in ProtocolTranslation.PortType.__members__.items():
        list_.append(ProtocolTranslation({
            'type': member.value,
            'protospec': random.randint(0, len(get_id_protocol_names())),
            'port': random.randint(1, 65535)
        }))

    yield list_

    engine.set_protocol_translations_list([])


@pytest.mark.skipif(not exists.data_directory_exists(),
                    reason='Cannot access non existent directory in repo -> src/data')
@pytest.mark.api
def test_get_protocol_list(engine: OmniEngine):
    """ Test the REST API call for getting the list of protocols """
    engine_protocol_list = engine.get_protocol_list()
    omni_protocol_list_names = get_id_protocol_names()
    for protocol in engine_protocol_list:
        assert protocol.id in omni_protocol_list_names, (
            f'Protocol {protocol.name} does not exist in expected list ')


@pytest.mark.skipif(not exists.data_directory_exists(),
                    reason='Cannot access non existent directory in repo -> src/data')
@pytest.mark.api
def test_get_protocol_translations_empty_list(engine: OmniEngine):
    """ Test the REST API call for obtaining the list of protocol translations """
    assert not engine.get_protocol_translation_list(
    ), 'A protocol translations list exists. Should be empty'


@pytest.mark.skipif(not exists.data_directory_exists(),
                    reason='Cannot access non existent directory in repo -> src/data')
@pytest.mark.api
def test_set_protocol_translations(engine: OmniEngine,
                                   translation_list: List[ProtocolTranslation]):
    """ Test the REST API call for setting the list of protocol translations """
    engine.set_protocol_translations_list(translation_list)

    list_ = sorted(engine.get_protocol_translation_list(), key=lambda x: x.port_type)

    for received, transmitted in zip(list_, translation_list):
        assert received == transmitted, 'Failed comparison from POST/SET'
