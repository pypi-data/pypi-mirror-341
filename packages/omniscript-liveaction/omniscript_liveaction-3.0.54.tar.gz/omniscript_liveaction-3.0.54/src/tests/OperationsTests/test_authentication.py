import pytest
import time

from omniscript import AuthenticationToken
from omniscript import OmniEngine


@pytest.fixture(scope="module", autouse=True)
def token() -> AuthenticationToken:
    """ Authentication token fixture """

    # Adding a delay to throttle the tests as a result of the API requests being throttled
    time.sleep(1)

    return AuthenticationToken.create(
        label="Pytest Token", authentication=True, client="", enabled=True,
        expiration_time="2030-06-03T20:10:00.123456789Z", user_domain="", user_id="admin",
        user_info_id=0, user_name="admin")


@pytest.fixture(scope="module")
def label() -> str:
    """ Modified label for modification test """
    return "Modified Pytest Token"


@pytest.mark.api
def test_get_token_list(engine: OmniEngine):
    """ Test the retrieval of the authentication token list """
    assert not engine.get_token_list(), 'Failed due to already existing authentication token list'


@pytest.mark.api
@pytest.mark.skip('Disabling all test. Fails on second run.')
def test_create_token(engine: OmniEngine, token: AuthenticationToken):
    """ Test the creation of a token """
    resp = engine.create_token(token)
    assert resp is not None, 'Failed to create a token.'

    token.authentication_token_id = resp[AuthenticationToken._json_authentication_token_id]


@pytest.mark.api
@pytest.mark.skip('Disabling all test. Fails on second run.')
def test_get_token(engine: OmniEngine, token: AuthenticationToken):
    """ Test the get and verify the token matches the token written """
    retrieved_token = engine.get_token(token.authentication_token_id)

    assert retrieved_token is not None, 'Faield to retrive token'
    assert retrieved_token == token, f'Failed token match: {token} vs {retrieved_token}'


@pytest.mark.api
@pytest.mark.skip('Disabling all test. Fails on second run.')
def test_modify_token(engine: OmniEngine, token: AuthenticationToken, label: str):
    """ Test the put which modifies the token"""
    token.label = label

    engine.modify_token(token)

    mod_token = engine.get_token(token.authentication_token_id)

    assert mod_token is not None, 'Faield to get modified token'
    assert mod_token == token, (f'Failed modification comparison check. Expected {label} vs '
                                f'Actual {mod_token.label}')


@pytest.mark.api
@pytest.mark.skip('Disabling all test. Deletes token.')
def test_delete_token(engine: OmniEngine, token: AuthenticationToken):
    """ Test the deletion of token(s) """
    engine.delete_token(token)

    assert not engine.get_token_list(), 'Failed deleting of token'


@pytest.mark.skip('Skipping because an internal 500 server error is thrown')
def test_get_token_when_empty_list(engine: OmniEngine, token: AuthenticationToken):
    assert engine.get_token(
        token.authentication_token_id) is None, 'Failed single token get on empty list'
