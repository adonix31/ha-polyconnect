"""Helpers for reading Polyconnect's minimum application version.

This file is intentionally side-effect-free. The bridge must only fetch config.js
from its already authenticated, validated HTTPS application origin.
"""
from __future__ import annotations

import json
import re
from urllib.parse import urlsplit

_VERSION = re.compile(r"^[0-9]{1,3}(?:\.[0-9]{1,3}){1,3}$")
_MIN_VERSION = re.compile(r"\bminVersion\s*:\s*['\"]([0-9.]+)['\"]")


def parse_min_version(config_js: str) -> str | None:
    """Extract a strictly numeric dotted version from APP_CONFIG config.js."""
    if "APP_CONFIG" not in config_js:
        return None
    match = _MIN_VERSION.search(config_js)
    if not match:
        return None
    version = match.group(1)
    return version if _VERSION.fullmatch(version) else None


def is_newer(required: str, current: str) -> bool:
    """Compare numeric dotted versions (9.10 is newer than 9.9)."""
    if not _VERSION.fullmatch(required) or not _VERSION.fullmatch(current):
        raise ValueError("Invalid application version")
    return tuple(map(int, required.split("."))) > tuple(map(int, current.split(".")))


def is_trusted_app_origin(origin: str) -> bool:
    """Allow only HTTPS app hosts under the expected MyTech Connect domain."""
    parsed = urlsplit(origin)
    host = (parsed.hostname or "").lower()
    return (
        parsed.scheme == "https"
        and parsed.username is None
        and parsed.password is None
        and parsed.port in (None, 443)
        and host.startswith("polytropic.user-app.")
        and host.endswith(".pool.mytech-connect.io")
        and parsed.path in ("", "/")
        and not parsed.query
        and not parsed.fragment
    )
