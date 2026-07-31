"""Independent canonical hashing for Build 025B assignment receipts."""

from __future__ import annotations

from hashlib import sha256
import json

from table_string_assignment import TableStringAssignmentReceipt


def assignment_payload(receipt: TableStringAssignmentReceipt) -> dict[str, object]:
    """Return the canonical receipt payload excluding its asserted hash."""

    return {
        "schema_version": receipt.schema_version,
        "table_id": receipt.table_id,
        "geometry_hash": receipt.geometry_hash,
        "string_count": receipt.string_count,
        "modules_per_string": receipt.modules_per_string,
        "strings": [
            {
                "string_id": item.string_id,
                "ordinal": item.ordinal,
                "ordered_module_ids": list(item.ordered_module_ids),
                "order_basis": item.order_basis,
                "positive_free_terminal": {
                    "terminal_id": item.positive_free_terminal.terminal_id,
                    "string_id": item.positive_free_terminal.string_id,
                    "polarity": item.positive_free_terminal.polarity,
                },
                "negative_free_terminal": {
                    "terminal_id": item.negative_free_terminal.terminal_id,
                    "string_id": item.negative_free_terminal.string_id,
                    "polarity": item.negative_free_terminal.polarity,
                },
            }
            for item in receipt.strings
        ],
    }


def calculate_assignment_hash(receipt: TableStringAssignmentReceipt) -> str:
    """Recalculate the deterministic SHA-256 content hash independently."""

    encoded = json.dumps(
        assignment_payload(receipt),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    ).encode("utf-8")
    return f"sha256:{sha256(encoded).hexdigest()}"
