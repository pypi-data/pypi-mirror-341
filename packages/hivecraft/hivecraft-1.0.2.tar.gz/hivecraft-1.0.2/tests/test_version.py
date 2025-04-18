"""Tests for version information."""
import re
import hivecraft
from hivecraft.version import __version__

def test_version_format():
    """Test that the version follows semantic versioning."""
    pattern = r"^\d+\.\d+\.\d+([\-\+].+)?$"
    assert re.match(pattern, __version__) is not None

def test_version_consistency():
    """Test that the version is consistent between module and version.py."""
    assert hivecraft.__version__ == __version__
