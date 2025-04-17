import pytest

from typing import List

from omniscript import OmniEngine, License, LicenseSettings

# NOTE! Cannot test setting of license without causing a restart to the device. Should not
# be included in pytest framework. Needs to be a standalone test


@pytest.fixture(scope="module")
def flags(virtual: bool) -> List[int]:
    """ Get the acceptable list of flags to work with """
    return [flag.value for flag in License.Flags if virtual and flag !=
            License.Flags.HD_SERIAL_NUMBER]


@pytest.mark.api
def test_get_license(engine: OmniEngine):
    """ Test retrieval of license information """
    assert engine.get_license() is not None, 'Failed due to missing license information '


@pytest.mark.api
def test_get_license_locking_code(engine: OmniEngine, flags: List[int]):
    """ Test retrieval of the license locking code """
    for flag in flags:
        assert engine.get_license_locking_code(
            flag) is not None, 'Failed to get license locking code'


@pytest.mark.api
def test_get_license_locking_code_using_list(engine: OmniEngine, flags: List[int]):
    for flag0 in flags:
        for flag1 in flags:
            if flag0 != flag1:
                assert engine.get_license_locking_code(
                    [flag0, flag1]) is not None, 'Failed to get license locking code'


@pytest.mark.api
def test_get_license_settings(engine: OmniEngine):
    """ Test retrieval of the license settings """
    assert engine.get_license_settings(
    ) is not None, 'Failed due to missing license settings'


@pytest.mark.api
def test_set_of_license_settings(engine: OmniEngine):
    """ Test the setting of the license settings """
    settings = engine.get_license_settings()

    assert isinstance(settings, LicenseSettings), 'Failed to get license settings'

    engine.set_license_settings(settings._format())

    assert settings == engine.get_license_settings()
