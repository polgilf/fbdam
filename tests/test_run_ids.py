from __future__ import annotations

from datetime import datetime, timezone

import pytest

from fbdam.utils import build_run_dir, make_run_id, parse_run_id, slugify_run_name


def test_make_run_id_from_datetime() -> None:
    ts = datetime(2025, 1, 1, 12, 30, 15, tzinfo=timezone.utc)
    run_id = make_run_id("Demo Run", ts)
    assert run_id == "demo-run_20250101T123015Z"


def test_make_run_id_from_iso_string() -> None:
    run_id = make_run_id("demo", "2025-01-01T01:02:03Z")
    assert run_id == "demo_20250101T010203Z"


def test_parse_run_id_accepts_old_and_new_formats() -> None:
    old_id = "20250101T000000Z_demo_ok"
    new_id = "demo_ok_20250101T000000Z"

    parsed_old = parse_run_id(old_id)
    parsed_new = parse_run_id(new_id)

    assert parsed_old == {"name": "demo_ok", "timestamp": "20250101T000000Z", "id": new_id}
    assert parsed_new == parsed_old


def test_parse_run_id_rejects_invalid_values() -> None:
    with pytest.raises(ValueError):
        parse_run_id("not-a-run-id")


def test_slugify_run_name_preserves_safe_characters() -> None:
    assert slugify_run_name("Hello World!") == "hello-world"
    assert slugify_run_name("\u2603") == "run"


def test_build_run_dir_normalises_segments(tmp_path) -> None:
    run_dir = build_run_dir(tmp_path, "Dataset A", "Config B", "run_20250101T000000Z")
    assert run_dir.exists()
    assert run_dir.parent.name == "config-b"
    assert run_dir.parent.parent.name == "dataset-a"
