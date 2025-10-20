"""Helpers for constructing and parsing run identifiers."""

from __future__ import annotations

import re
from datetime import datetime, timezone
from typing import Dict, Mapping

_RUN_TS_RE = re.compile(r"^\d{8}T\d{6}Z$")
_OLD_RUN_ID_RE = re.compile(r"^(?P<ts>\d{8}T\d{6}Z)_(?P<name>[a-z0-9_\-]+)$")
_NEW_RUN_ID_RE = re.compile(r"^(?P<name>[a-z0-9_\-]+)_(?P<ts>\d{8}T\d{6}Z)$")


def _coerce_timestamp(ts: datetime | str) -> str:
    if isinstance(ts, datetime):
        ts = ts.astimezone(timezone.utc)
        return ts.strftime("%Y%m%dT%H%M%SZ")

    ts = str(ts).strip()
    if _RUN_TS_RE.fullmatch(ts):
        return ts

    # Attempt ISO 8601 parsing (accepts trailing 'Z')
    normalised = ts.replace("Z", "+00:00")
    try:
        parsed = datetime.fromisoformat(normalised)
    except ValueError as exc:  # pragma: no cover - defensive guard
        raise ValueError(f"Invalid run timestamp: {ts!r}") from exc
    parsed = parsed.astimezone(timezone.utc)
    return parsed.strftime("%Y%m%dT%H%M%SZ")


def slugify_run_name(name: str, *, default: str = "run") -> str:
    """Normalise arbitrary input into a safe run name slug."""

    slug_chars: list[str] = []
    for ch in str(name).lower():
        if ch.isalnum() or ch in {"-", "_"}:
            slug_chars.append(ch)
        else:
            slug_chars.append("-")
    slug = "".join(slug_chars).strip("-_")
    return slug or default


def make_run_id(name: str, ts: datetime | str) -> str:
    """Return the canonical ``<name>_<timestamp>`` run identifier."""

    slug = slugify_run_name(name)
    timestamp = _coerce_timestamp(ts)
    return f"{slug}_{timestamp}"


def parse_run_id(value: str) -> Dict[str, str]:
    """Parse a run identifier in either old or new format."""

    candidate = str(value).strip()
    match = _NEW_RUN_ID_RE.fullmatch(candidate)
    if match is None:
        match = _OLD_RUN_ID_RE.fullmatch(candidate)
    if match is None:
        raise ValueError(f"Unrecognised run identifier: {value!r}")

    groups: Mapping[str, str] = match.groupdict()
    name = groups["name"]
    timestamp = groups["ts"]
    return {"name": name, "timestamp": timestamp, "id": f"{name}_{timestamp}"}


__all__ = ["make_run_id", "parse_run_id", "slugify_run_name"]
