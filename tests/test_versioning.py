"""Regression tests for version-check helpers (run with pytest)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "polyconnect_bridge"))

from versioning import parse_min_version, is_newer, is_trusted_app_origin


def test_min_version():
    assert parse_min_version('window.APP_CONFIG = { theme: "polytropic", minVersion: "9.0" };') == "9.0"
    assert parse_min_version("window.APP_CONFIG = { minVersion: '10.2.1' };") == "10.2.1"
    assert parse_min_version("window.APP_CONFIG = { minVersion: 'x.y' };") is None
    assert parse_min_version("not_a_config = { minVersion: '10.0' };") is None


def test_numeric_comparison():
    assert is_newer("9.10", "9.9")
    assert not is_newer("9.0", "9.0")
    assert not is_newer("8.8", "9.0")


def test_trusted_origin():
    assert is_trusted_app_origin("https://polytropic.user-app.v2.pool.mytech-connect.io")
    assert is_trusted_app_origin("https://polytropic.user-app.pool.mytech-connect.io")
    assert not is_trusted_app_origin("http://polytropic.user-app.v2.pool.mytech-connect.io")
    assert not is_trusted_app_origin("https://polytropic.user-app.v2.pool.mytech-connect.io.evil.example")
    assert not is_trusted_app_origin("https://polytropic.user-app.v2.pool.mytech-connect.io/redirect")
