"""Dataset discovery, stable ids, split guards and manifests."""

from __future__ import annotations

import csv
import hashlib
import json
from collections.abc import Iterable, Iterator, Mapping
from dataclasses import dataclass, field
from pathlib import Path

from ..config import AppConfig
from ..errors import DataNotFoundError, DataValidationError, SplitLeakageError
from ..security import AccessPolicy
from .labels import canonical_activity

SPLIT_ALIASES = {
    "train": "train",
    "training": "train",
    "val": "val",
    "valid": "val",
    "validation": "val",
    "test": "test",
    "id": "test",
    "dev": "val",
}

META_FIELDS = {
    "sample_id": ("sample_id", "id", "record_id"),
    "path": ("path", "file", "relative_path", "h5_path"),
    "session_id": ("session_id", "session", "recording_id"),
    "user_id": ("user_id", "user", "subject_id", "participant_id"),
    "environment_id": ("environment_id", "environment", "env", "room_id"),
    "device_id": ("device_id", "device", "hardware_id"),
    "activity": ("activity", "activity_name", "label", "class"),
    "split": ("split", "partition", "set"),
}


@dataclass(frozen=True)
class SampleRecord:
    sample_id: str
    path: Path
    session_id: str
    user_id: str
    environment_id: str
    device_id: str
    activity: str
    split: str = "unknown"
    metadata: Mapping[str, str] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "sample_id": self.sample_id,
            "path": str(self.path),
            "session_id": self.session_id,
            "user_id": self.user_id,
            "environment_id": self.environment_id,
            "device_id": self.device_id,
            "activity": self.activity,
            "split": self.split,
        }


def stable_sample_id(*parts: object) -> str:
    digest = hashlib.blake2b(digest_size=16)
    for part in parts:
        digest.update(str(part).encode("utf-8"))
        digest.update(b"\0")
    return digest.hexdigest()


def _pick(row: Mapping[str, str], names: Iterable[str]) -> str:
    lowered = {str(key).strip().lower(): value for key, value in row.items()}
    for name in names:
        if name in lowered and str(lowered[name]).strip():
            return str(lowered[name]).strip()
    return ""


def _split_name(value: str) -> str:
    return SPLIT_ALIASES.get(value.strip().lower(), "unknown")


def _path_ids(path: Path) -> dict[str, str]:
    ids = {"user_id": "unknown", "environment_id": "unknown", "device_id": "unknown", "session_id": path.stem}
    for part in path.parts:
        lowered = part.lower()
        if lowered.startswith("user_"):
            ids["user_id"] = part[5:] or "unknown"
        elif lowered.startswith("env_"):
            ids["environment_id"] = part[4:] or "unknown"
        elif lowered.startswith("device_"):
            ids["device_id"] = part[7:] or "unknown"
        elif "session" in lowered:
            ids["session_id"] = part
    return ids


def read_metadata(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def discover_records(config: AppConfig, policy: AccessPolicy, *, actor: str = "system") -> list[SampleRecord]:
    if config.task_root is None:
        raise DataNotFoundError("dataset root is not configured", {"env_names": ["HAR_DATA_ROOT", "CSI_DATA_ROOT"]})
    task_root = policy.authorize_read(actor, config.task_root)
    if not task_root.exists():
        raise DataNotFoundError("task directory does not exist", {"path": str(task_root)})
    metadata_path = task_root / config.dataset.metadata_file
    rows = read_metadata(policy.authorize_read(actor, metadata_path)) if metadata_path.exists() else []
    records: list[SampleRecord] = []
    if rows:
        for index, row in enumerate(rows):
            relative = _pick(row, META_FIELDS["path"])
            if not relative:
                continue
            candidate = Path(relative)
            path = policy.authorize_read(actor, task_root / candidate if not candidate.is_absolute() else candidate)
            activity = canonical_activity(_pick(row, META_FIELDS["activity"]), allow_decision_state=False).value
            ids = _path_ids(path.relative_to(task_root))
            record_id = _pick(row, META_FIELDS["sample_id"]) or stable_sample_id(path.relative_to(task_root), index)
            records.append(
                SampleRecord(
                    sample_id=stable_sample_id(record_id, path.relative_to(task_root), index),
                    path=path,
                    session_id=_pick(row, META_FIELDS["session_id"]) or ids["session_id"],
                    user_id=_pick(row, META_FIELDS["user_id"]) or ids["user_id"],
                    environment_id=_pick(row, META_FIELDS["environment_id"]) or ids["environment_id"],
                    device_id=_pick(row, META_FIELDS["device_id"]) or ids["device_id"],
                    activity=activity,
                    split=_split_name(_pick(row, META_FIELDS["split"])),
                    metadata={str(k): str(v) for k, v in row.items()},
                )
            )
    if not records:
        for path in sorted(task_root.glob(config.dataset.h5_glob)):
            resolved = policy.authorize_read(actor, path)
            relative_path = resolved.relative_to(task_root)
            ids = _path_ids(relative_path)
            activity_text = next((part for part in relative_path.parts if part.lower().startswith("act_")), "")
            if not activity_text:
                raise DataValidationError("cannot infer activity from sample path", {"path": str(relative_path)})
            records.append(
                SampleRecord(
                    sample_id=stable_sample_id(relative_path),
                    path=resolved,
                    session_id=ids["session_id"],
                    user_id=ids["user_id"],
                    environment_id=ids["environment_id"],
                    device_id=ids["device_id"],
                    activity=canonical_activity(activity_text[4:], allow_decision_state=False).value,
                    split="unknown",
                    metadata={},
                )
            )
    if not records:
        raise DataNotFoundError("no HDF5 samples were discovered", {"path": str(task_root)})
    return records


def assert_no_split_leakage(
    records: Iterable[SampleRecord],
    *,
    group_fields: tuple[str, ...] = ("user_id", "environment_id", "device_id", "session_id"),
) -> None:
    groups: dict[str, set[str]] = {}
    for record in records:
        if record.split not in {"train", "val", "test"}:
            continue
        for field_name in group_fields:
            key = str(getattr(record, field_name))
            groups.setdefault(f"{field_name}:{key}", set()).add(record.split)
    leaked = {key: sorted(value) for key, value in groups.items() if len(value) > 1}
    if leaked:
        raise SplitLeakageError("group identifiers cross split boundaries", {"leaked": leaked})


def write_manifest(records: Iterable[SampleRecord], path: Path) -> int:
    rows = list(records)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for record in rows:
            handle.write(json.dumps(record.to_dict(), sort_keys=True) + "\n")
    return len(rows)


def iter_train_val_test(records: Iterable[SampleRecord]) -> Iterator[tuple[str, SampleRecord]]:
    for record in records:
        if record.split in {"train", "val", "test"}:
            yield record.split, record
