import os
import pytest

from distutils import dir_util
from typing import List

from omniscript import OmniEngine, Filter


@pytest.fixture(scope="session")
def default_filter_list(engine: OmniEngine) -> List[Filter]:
    """ The default filter list on the engine """
    return engine.get_filter_list()


@pytest.fixture
def filesdir(tmpdir, request):
    filename = request.module.__file__
    test_dir, _ = os.path.splitext(filename)

    if os.path.isdir(test_dir):
        dir_util.copy_tree(test_dir, str(tmpdir))

    return tmpdir
