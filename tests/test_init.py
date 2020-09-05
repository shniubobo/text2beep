import text2beep
from text2beep.version import get_version


def test_version():
    assert text2beep.__version__ == get_version()
