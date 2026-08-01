#!/usr/bin/env python3
"""Validate the reference authority bundle against schema and Python authority."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import re
from typing import Any

try:
    from scripts.build_authority_bundle import (
        AUTHORITY_BUNDLE_PATH,
        authority_response_payload,
        canonical_json,
    )
except ModuleNotFoundError:  # Direct execution from the scripts directory.
    from build_authority_bundle import (
        AUTHORITY_BUNDLE_PATH,
        authority_response_payload,
        canonical_json,
    )


ROOT = Path(__file__).resolve().parents[1]
AUTHORITY_RESPONSE_SCHEMA_PATH = (
    ROOT / "schemas" / "authority-response.schema.json"
)


class AuthorityBundleValidationError(ValueError):
    """The authority response violates its schema or engineering bindings."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AuthorityBundleValidationError(message)


def load_json_object(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(payload, dict), f"{path} must contain one JSON object")
    return payload


def _resolve_ref(root_schema: dict[str, Any], reference: str) -> dict[str, Any]:
    require(reference.startswith("#/$defs/"), f"unsupported schema reference: {reference}")
    name = reference.removeprefix("#/$defs/")
    target = root_schema.get("$defs", {}).get(name)
    require(isinstance(target, dict), f"schema reference does not exist: {reference}")
    return target


def _matches_type(value: object, expected: str) -> bool:
    if expected == "object":
        return isinstance(value, dict)
    if expected == "array":
        return isinstance(value, list)
    if expected == "string":
        return isinstance(value, str)
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if expected == "boolean":
        return isinstance(value, bool)
    if expected == "null":
        return value is None
    raise AuthorityBundleValidationError(f"unsupported schema type: {expected}")


def _validate_schema_node(
    value: object,
    node: dict[str, Any],
    *,
    root_schema: dict[str, Any],
    path: str,
) -> None:
    if "$ref" in node:
        target = _resolve_ref(root_schema, str(node["$ref"]))
        _validate_schema_node(value, target, root_schema=root_schema, path=path)
        return

    if "type" in node:
        expected_type = str(node["type"])
        require(_matches_type(value, expected_type), f"{path} must be {expected_type}")
    if "const" in node:
        require(value == node["const"], f"{path} must equal {node['const']!r}")
    if "enum" in node:
        require(value in node["enum"], f"{path} is outside the allowed values")

    if isinstance(value, str):
        if "minLength" in node:
            require(len(value) >= int(node["minLength"]), f"{path} is too short")
        if "pattern" in node:
            require(
                re.fullmatch(str(node["pattern"]), value) is not None,
                f"{path} does not match the required pattern",
            )

    if isinstance(value, dict):
        properties = node.get("properties", {})
        required = node.get("required", [])
        require(isinstance(properties, dict), f"{path} schema properties are invalid")
        require(isinstance(required, list), f"{path} schema required list is invalid")
        missing = [name for name in required if name not in value]
        require(not missing, f"{path} is missing required fields: {', '.join(missing)}")
        if node.get("additionalProperties") is False:
            extras = sorted(set(value) - set(properties))
            require(not extras, f"{path} contains unexpected fields: {', '.join(extras)}")
        for name, child_schema in properties.items():
            if name in value:
                require(
                    isinstance(child_schema, dict),
                    f"{path}.{name} schema node is invalid",
                )
                _validate_schema_node(
                    value[name],
                    child_schema,
                    root_schema=root_schema,
                    path=f"{path}.{name}",
                )

    if isinstance(value, list):
        if "minItems" in node:
            require(len(value) >= int(node["minItems"]), f"{path} has too few items")
        if "maxItems" in node:
            require(len(value) <= int(node["maxItems"]), f"{path} has too many items")
        if node.get("uniqueItems") is True:
            encoded = [canonical_json(item) for item in value]
            require(len(encoded) == len(set(encoded)), f"{path} contains duplicate items")
        item_schema = node.get("items")
        if item_schema is not None:
            require(isinstance(item_schema, dict), f"{path} item schema is invalid")
            for index, item in enumerate(value):
                _validate_schema_node(
                    item,
                    item_schema,
                    root_schema=root_schema,
                    path=f"{path}[{index}]",
                )


def validate_json_schema(
    payload: dict[str, Any],
    schema: dict[str, Any],
) -> None:
    require(
        schema.get("$schema") == "https://json-schema.org/draft/2020-12/schema",
        "authority response schema must declare JSON Schema 2020-12",
    )
    require(
        schema.get("$id")
        == "https://globalgrid2050.com/schemas/solar-dc/authority-response.v1.json",
        "authority response schema identifier changed",
    )
    _validate_schema_node(payload, schema, root_schema=schema, path="$response")


def _assert_hash(value: object, path: str) -> str:
    require(isinstance(value, str), f"{path} must be text")
    require(
        re.fullmatch(r"sha256:[0-9a-f]{64}", value) is not None,
        f"{path} is not a SHA-256 identifier",
    )
    return value


def validate_authority_bundle_payload(
    payload: dict[str, Any],
    *,
    schema: dict[str, Any] | None = None,
) -> dict[str, object]:
    active_schema = schema or load_json_object(AUTHORITY_RESPONSE_SCHEMA_PATH)
    validate_json_schema(payload, active_schema)

    response_basis = dict(payload)
    observed_response_hash = _assert_hash(
        response_basis.pop("response_hash"),
        "response_hash",
    )
    expected_response_hash = "sha256:" + hashlib.sha256(
        canonical_json(response_basis).encode("utf-8")
    ).hexdigest()
    require(
        observed_response_hash == expected_response_hash,
        "response_hash does not match the canonical response payload",
    )

    block = payload["inverter_block"]
    build025 = payload["build025"]
    require(isinstance(block, dict), "inverter_block must be an object")
    require(isinstance(build025, dict), "build025 must be an object")
    boundary = block["product_boundary"]
    inputs = block["input_authority"]
    evidence = block["equipment_evidence"]
    binding = block["table_receipts"][0]

    require(
        boundary["module_count"]
        == boundary["modules_per_string"] * boundary["string_count"],
        "product boundary module arithmetic is inconsistent",
    )
    require(
        math.isclose(
            boundary["string_rated_power_kwp"],
            boundary["module_rated_power_wp"]
            * boundary["modules_per_string"]
            / 1000.0,
            rel_tol=0.0,
            abs_tol=1e-12,
        ),
        "product boundary string power arithmetic is inconsistent",
    )
    require(
        math.isclose(
            boundary["dc_nameplate_power_kwp"],
            boundary["module_rated_power_wp"]
            * boundary["module_count"]
            / 1000.0,
            rel_tol=0.0,
            abs_tol=1e-12,
        ),
        "product boundary DC power arithmetic is inconsistent",
    )
    require(
        math.isclose(
            boundary["dc_ac_nameplate_ratio"],
            boundary["dc_nameplate_power_kwp"]
            / boundary["inverter_apparent_power_kva"],
            rel_tol=0.0,
            abs_tol=1e-12,
        ),
        "product boundary DC/AC arithmetic is inconsistent",
    )

    require(inputs["mppt_count"] is None, "MPPT count must remain unresolved")
    require(
        inputs["mppt_mapping_verification_states"] == ["unknown"],
        "MPPT mapping evidence must remain unresolved",
    )
    require(
        inputs["internal_dc_topology"] == "unknown",
        "internal DC topology must remain unresolved",
    )
    require(
        inputs["reverse_current_blocking"] == "unknown",
        "reverse-current blocking must remain unresolved",
    )
    require(
        inputs["pce_backfeed_current_a"] is None,
        "PCE backfeed current must remain unresolved",
    )
    require(
        inputs["routing_fixture_mppt_labels_are_equipment_evidence"] is False,
        "routing fixture MPPT labels may not become equipment evidence",
    )
    require(
        evidence["missing_evidence_count"] == len(evidence["missing_evidence"]),
        "equipment missing-evidence count does not match its list",
    )
    for required_gap in (
        "inverter.dc_inputs.dc_input_01.mppt_id",
        "inverter.dc_inputs.dc_input_24.mppt_id",
        "inverter.internal_dc_topology",
        "inverter.reverse_current_blocking",
        "inverter.pce_backfeed_current_a",
    ):
        require(
            required_gap in evidence["missing_evidence"],
            f"required unresolved evidence gap is absent: {required_gap}",
        )

    _assert_hash(block["receipt_hash"], "inverter_block.receipt_hash")
    _assert_hash(build025["receipt_hash"], "build025.receipt_hash")
    require(
        binding["build025_receipt_hash"] == build025["receipt_hash"],
        "child Build 025 receipt hash binding failed",
    )
    require(
        binding["geometry_hash"] == build025["geometry"]["geometry_hash"],
        "child geometry hash binding failed",
    )
    require(
        binding["assignment_hash"]
        == build025["string_allocation"]["assignment_hash"],
        "child assignment hash binding failed",
    )
    require(
        binding["topology_hash"] == build025["topology"]["topology_hash"],
        "child topology hash binding failed",
    )
    require(
        binding["input_allocation_hash"]
        == build025["input_allocation"]["allocation_hash"],
        "child input-allocation hash binding failed",
    )
    require(
        binding["routing_hash"] == build025["routing"]["routing_hash"],
        "child routing hash binding failed",
    )
    require(
        binding["installed_length_hash"]
        == build025["installed_length"]["receipt_hash"],
        "child installed-length hash binding failed",
    )
    require(
        payload["strategy"]
        == binding["strategy"]
        == build025["topology"]["strategy"]
        == build025["routing"]["strategy"],
        "strategy binding failed",
    )

    expected = authority_response_payload(str(payload["strategy"]))
    require(
        payload == expected,
        "bundle does not equal the current Python authority response",
    )

    return {
        "pass": True,
        "schema_version": payload["schema_version"],
        "strategy": payload["strategy"],
        "response_hash": observed_response_hash,
        "inverter_block_receipt_hash": block["receipt_hash"],
        "build025_receipt_hash": build025["receipt_hash"],
        "module_count": boundary["module_count"],
        "string_count": boundary["string_count"],
        "modules_per_string": boundary["modules_per_string"],
        "dc_nameplate_power_kwp": boundary["dc_nameplate_power_kwp"],
        "inverter_apparent_power_kva": boundary["inverter_apparent_power_kva"],
        "evidence_state": evidence["state"],
        "missing_evidence_count": evidence["missing_evidence_count"],
    }


def validate_authority_bundle_file(
    bundle_path: Path = AUTHORITY_BUNDLE_PATH,
    schema_path: Path = AUTHORITY_RESPONSE_SCHEMA_PATH,
) -> dict[str, object]:
    return validate_authority_bundle_payload(
        load_json_object(bundle_path),
        schema=load_json_object(schema_path),
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bundle", type=Path, default=AUTHORITY_BUNDLE_PATH)
    parser.add_argument("--schema", type=Path, default=AUTHORITY_RESPONSE_SCHEMA_PATH)
    args = parser.parse_args()

    try:
        summary = validate_authority_bundle_file(args.bundle, args.schema)
    except (OSError, json.JSONDecodeError, AuthorityBundleValidationError) as exc:
        raise SystemExit(f"authority bundle invalid: {exc}") from exc
    print(canonical_json(summary))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
