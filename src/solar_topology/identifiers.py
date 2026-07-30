"""Canonical hierarchical identifiers for V10 engineering records.

Identifiers are deterministic, human-readable and independent of confidential
project naming. Public exports may use public aliases while restricted source
names remain outside the identifier itself.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
import re


IDENTIFIER_SCHEMA_VERSION = "globalgrid2050.solar-dc.identifiers.v10.1"
_TOKEN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


class EntityLevel(StrEnum):
    PROJECT = "project"
    SITE = "site"
    SYSTEM = "system"
    EQUIPMENT = "equipment"
    CIRCUIT = "circuit"
    OBJECT = "object"


_LEVEL_ORDER = {
    EntityLevel.PROJECT: 0,
    EntityLevel.SITE: 1,
    EntityLevel.SYSTEM: 2,
    EntityLevel.EQUIPMENT: 3,
    EntityLevel.CIRCUIT: 4,
    EntityLevel.OBJECT: 5,
}


@dataclass(frozen=True)
class CanonicalIdentifier:
    level: EntityLevel
    local_id: str
    parent: "CanonicalIdentifier | None" = None
    schema_version: str = IDENTIFIER_SCHEMA_VERSION

    def __post_init__(self) -> None:
        if not isinstance(self.level, EntityLevel):
            raise TypeError("level must be an EntityLevel")
        if not isinstance(self.local_id, str) or not _TOKEN.fullmatch(self.local_id):
            raise ValueError(
                "local_id must be lowercase kebab-case using letters and digits"
            )
        if self.level is EntityLevel.PROJECT:
            if self.parent is not None:
                raise ValueError("project identifiers cannot have a parent")
        else:
            if not isinstance(self.parent, CanonicalIdentifier):
                raise ValueError(f"{self.level} identifiers require a parent")
            expected = _LEVEL_ORDER[self.level] - 1
            actual = _LEVEL_ORDER[self.parent.level]
            if actual != expected:
                raise ValueError(
                    f"{self.level} parent must be the immediately preceding level"
                )

    @property
    def value(self) -> str:
        current: CanonicalIdentifier | None = self
        parts: list[str] = []
        while current is not None:
            parts.append(f"{current.level.value}:{current.local_id}")
            current = current.parent
        return "/".join(reversed(parts))

    def child(self, level: EntityLevel, local_id: str) -> "CanonicalIdentifier":
        return CanonicalIdentifier(level=level, local_id=local_id, parent=self)


def project_id(local_id: str) -> CanonicalIdentifier:
    return CanonicalIdentifier(EntityLevel.PROJECT, local_id)


def parse_identifier(value: str) -> CanonicalIdentifier:
    if not isinstance(value, str) or not value:
        raise ValueError("identifier must be non-empty text")
    parent: CanonicalIdentifier | None = None
    for index, component in enumerate(value.split("/")):
        try:
            level_text, local_id = component.split(":", 1)
            level = EntityLevel(level_text)
        except (ValueError, TypeError) as exc:
            raise ValueError(f"invalid identifier component {component!r}") from exc
        expected_level = list(EntityLevel)[index] if index < len(EntityLevel) else None
        if level is not expected_level:
            raise ValueError("identifier hierarchy must start at project and be contiguous")
        parent = CanonicalIdentifier(level, local_id, parent)
    assert parent is not None
    return parent


def require_unique_identifiers(
    identifiers: tuple[CanonicalIdentifier, ...] | list[CanonicalIdentifier],
) -> None:
    values = [identifier.value for identifier in identifiers]
    if len(values) != len(set(values)):
        raise ValueError("canonical identifiers must be unique")
