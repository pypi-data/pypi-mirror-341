import pytest
import omniscript

from tests.Utils import exists


@pytest.mark.skipif(not exists.data_directory_exists(),
                    reason='Cannot access non existent directory in repo -> src/data')
@pytest.mark.smoke
@pytest.mark.skip('Disabling all test.')
def test_expert_names():
    """ Test the expert names """
    id_expert_names = omniscript.get_id_expert_names()
    id_stat_names = omniscript.get_id_stat_names()

    for k, v in id_expert_names.items():
        assert k in id_stat_names, 'Failure in id_expert_names'
