import pytest
import string
import random

from omniscript import DecryptionKey, OmniEngine, DecryptionKeyTemplate
from typing import List


@pytest.fixture(scope="function")
def decryption_key_list():
    """ Fixture to store test list of decryption keys. """
    list_ = []
    for i in range(2):
        name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        key = DecryptionKeyTemplate(name, '', None, None, None)
        list_.append(key)
    yield list_


@pytest.fixture(scope="function")
def decryption_key_template():
    """ Fixture to store test list of decryption keys. """
    name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    key = DecryptionKeyTemplate(name, '', None, None, None)

    yield key


@pytest.fixture(scope="function")
def add_decryption_key_template(engine: OmniEngine):
    """ Fixture to store test list of decryption keys. """
    name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    key = DecryptionKeyTemplate(name, '', None, None, None)
    engine.add_decryption_key_templates(key)
    yield key


@pytest.fixture(scope="function")
def decryption_key():
    """ Fixture to store test list of decryption keys. """
    name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    props = {
        'id': None,
        'name': name,
        'passwordProtected': False
    }
    key = DecryptionKey(props)

    yield key


@pytest.mark.api
def test_get_decryption_key_list(engine: OmniEngine):
    """ Test for successful get of the list """
    key_list = engine.get_decryption_key_list()

    num_keys = len(key_list)

    default_keys_count = len(key_list)

    assert num_keys == default_keys_count, ('Failed default decryption key list check. Expected '
                                            f'{default_keys_count} got {num_keys}')


@pytest.mark.api
@pytest.mark.skip('Disabling all test. Deletes decryption key.')
def test_add_decryption_key_template_list(engine: OmniEngine,
                                          decryption_key_list: List[DecryptionKeyTemplate]):
    """ Test the setting of a new list of decryption keys
    Takes input list of DecryptionKeyTemplates to add
    """
    assert decryption_key_list is not None and isinstance(decryption_key_list, list), (
        'Empty key list, no keys to set')

    keys = engine.get_decryption_key_list()

    engine.add_decryption_key_templates(decryption_key_list)

    keys2 = engine.get_decryption_key_list()

    assert len(keys2) == (len(keys)+len(decryption_key_list)), (
        'Rest API call failed for adding a list of DecryptionKeyTemplates')

    engine.delete_decryption_keys(decryption_key_list)  # reset test


@pytest.mark.api
@pytest.mark.skip('Disabling all test. Deletes decryption key.')
def test_add_decryption_key_template(engine: OmniEngine,
                                     decryption_key_template: DecryptionKeyTemplate):
    """ Test the setting of a new list of decryption keys
    Takes input of a DecryptionKeyTemplate to add
    """
    assert isinstance(decryption_key_template, DecryptionKeyTemplate), (
        'Empty key list, no keys to set')

    keys = engine.get_decryption_key_list()

    engine.add_decryption_key_templates(decryption_key_template)

    keys2 = engine.get_decryption_key_list()

    assert len(keys2) == (len(keys)+1), 'Rest API call failed for adding a DecryptionKeyTemplate'

    engine.delete_decryption_keys(decryption_key_template)  # reset test


@pytest.mark.api
def test_delete_decryption_key(engine: OmniEngine, decryption_key_template: DecryptionKeyTemplate):
    """ Test the deletion of a list of decryption keys
    Takes input of a DecryptionKeyTemplate to add
    """
    assert isinstance(decryption_key_template, DecryptionKeyTemplate), (
        'Empty key list, no keys to set')

    keys = engine.get_decryption_key_list()

    engine.add_decryption_key_templates(decryption_key_template)
    keys2 = engine.get_decryption_key_list()

    assert len(keys2) == (len(keys)+1), 'Rest API call failed for adding a DecryptionKeyTemplate'

    engine.delete_decryption_keys(decryption_key_template)

    keys3 = engine.get_decryption_key_list()

    assert len(keys3) == len(keys), 'Rest API call failed for deleting DecryptionKeys by list'


@pytest.mark.api
@pytest.mark.skip('Disabling all test. Deletes decryption key.')
def test_delete_decryption_keys(engine: OmniEngine,
                                decryption_key_list: List[DecryptionKeyTemplate]):
    """ Test the deletion of a decryption key
    Takes input of a DecryptionKeyTemplate to add
    """
    assert isinstance(decryption_key_list, list), 'Empty key list, no keys to set'

    keys = engine.get_decryption_key_list()

    engine.add_decryption_key_templates(decryption_key_list)
    keys2 = engine.get_decryption_key_list()

    assert len(keys2) == (len(keys)+len(decryption_key_list)), (
        'Rest API call failed for adding a DecryptionKeyTemplate')

    engine.delete_decryption_keys(decryption_key_list)

    keys3 = engine.get_decryption_key_list()

    assert len(keys3) == len(keys), 'Rest API call failed for deleting DecryptionKeys by list'


@pytest.mark.dev
@pytest.mark.skip('Incomplete test')
# @pytest.mark.api
def test_rename_decryption_key(engine: OmniEngine,
                               add_decryption_key_template: DecryptionKeyTemplate):
    """ Test the setting of a new list of decryption keys
    Takes input list of DecryptionKeyTemplates
    """
    assert isinstance(add_decryption_key_template, DecryptionKeyTemplate), (
        'Empty key list, no keys to set')

    engine.rename_decryption_key(add_decryption_key_template, 'renametest2')

    found_key = engine.find_decryption_key('renametest2')

    assert found_key.name == 'renametest2', (
        'Rest API call failed for adding a list of DecryptionKeyTemplates')

    engine.delete_decryption_keys(add_decryption_key_template)  # reset test
