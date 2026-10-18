"""Synthetic domain seam for API/MCP adapters. No network, SDK or durable-store claim."""
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from typing import Mapping


class ContractError(ValueError):
    """Safe invalid-input error."""


class AccessDenied(PermissionError):
    """Safe missing-scope error."""


class Conflict(ValueError):
    """An idempotency key was reused for different content."""


@dataclass(frozen=True)
class Principal:
    tenant: str
    scopes: frozenset[str]


@dataclass(frozen=True)
class JobRequest:
    job_type: str
    items: tuple[str, ...]

    @classmethod
    def from_external(cls, raw: object) -> JobRequest:
        if not isinstance(raw, dict) or set(raw) != {"job_type", "items"}:
            raise ContractError("Invalid job fields")
        kind, items = raw["job_type"], raw["items"]
        if kind not in ("report", "index"):
            raise ContractError("Invalid job type")
        if not isinstance(items, list) or not 1 <= len(items) <= 100:
            raise ContractError("Invalid item count")
        if any(not isinstance(item, str) or not 1 <= len(item) <= 128 for item in items):
            raise ContractError("Invalid item")
        return cls(kind, tuple(items))


class JobService:
    """Single-process synthetic fixture; not thread-safe or durable."""
    def __init__(self) -> None:
        self._records: dict[tuple[str, str], tuple[str, str]] = {}

    def submit(self, principal: Principal, key: str, raw: object) -> Mapping[str, str]:
        if "jobs:write" not in principal.scopes:
            raise AccessDenied("Forbidden")
        if not isinstance(key, str) or not 1 <= len(key) <= 64:
            raise ContractError("Invalid idempotency key")
        request = JobRequest.from_external(raw)
        encoded = json.dumps([request.job_type, request.items], separators=(",", ":")).encode()
        digest = sha256(encoded).hexdigest()
        slot = (principal.tenant, key)
        prior = self._records.get(slot)
        if prior:
            if prior[0] != digest:
                raise Conflict("Conflicting request")
            return {"job_id": prior[1], "status": "accepted"}
        job_id = str(len(self._records) + 1)
        self._records[slot] = (digest, job_id)
        return {"job_id": job_id, "status": "accepted"}

    def read(self, principal: Principal, key: str) -> Mapping[str, str] | None:
        if "jobs:read" not in principal.scopes:
            raise AccessDenied("Forbidden")
        record = self._records.get((principal.tenant, key))
        return None if record is None else {"job_id": record[1], "status": "accepted"}
