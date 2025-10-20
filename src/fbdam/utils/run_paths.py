"""Run directory helpers for FBDAM experiments."""

from __future__ import annotations

from pathlib import Path

from .run_ids import slugify_run_name


def build_run_dir(
    outputs_root: Path | str,
    dataset_id: str,
    config_id: str,
    run_id: str,
    *,
    create: bool = True,
) -> Path:
    """Return the canonical run directory for a dataset/config/run tuple.

    The new experiment layout nests runs by dataset id and configuration id::

        <outputs_root>/<dataset_id>/<config_id>/<run_id>

    Args:
        outputs_root: Base directory that contains the ``runs`` tree.
        dataset_id: Identifier of the dataset used for the run.
        config_id: Identifier of the model configuration.
        run_id: Timestamped run identifier (typically produced by
            :func:`fbdam.utils.make_run_id`).
        create: When ``True`` (default) the directory hierarchy is created
            automatically.

    Returns:
        :class:`pathlib.Path` pointing to the run directory.
    """

    base = Path(outputs_root).expanduser()
    dataset_slug = slugify_run_name(dataset_id, default="dataset")
    config_slug = slugify_run_name(config_id, default="config")
    run_segment = str(run_id).strip()

    run_path = base / dataset_slug / config_slug / run_segment
    if create:
        run_path.mkdir(parents=True, exist_ok=True)
    return run_path


__all__ = ["build_run_dir"]
