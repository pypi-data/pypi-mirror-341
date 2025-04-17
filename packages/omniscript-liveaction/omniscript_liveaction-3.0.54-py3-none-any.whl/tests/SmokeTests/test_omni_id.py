import pytest
import omniscript


@pytest.mark.smoke
def test_omni_id():
    """ Testing OmniId """
    id0 = omniscript.OmniId()
    id0.new()

    id1 = omniscript.OmniId()
    id1.new()

    assert id0 != id1, 'OmniId new/parse failure'
