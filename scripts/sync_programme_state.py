#!/usr/bin/env python3
"""Validate programme-state.json and keep public status projections in sync."""

from __future__ import annotations

import argparse
from decimal import Decimal
import html
import json
from pathlib import Path
import re
import sys
import tomllib
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "programme-state.json"
SCHEMA_PATH = ROOT / "schemas" / "programme-state.schema.json"
README_PATH = ROOT / "README.md"
DASHBOARD_PATH = ROOT / "progress-dashboard.html"
README_START = "<!-- PROGRAMME-STATE:START -->"
README_END = "<!-- PROGRAMME-STATE:END -->"
SCHEMA_VERSION = "globalgrid2050.solar-dc.programme-state.v1"
SHA40 = re.compile(r"^[0-9a-f]{40}$")
SHA256 = re.compile(r"^sha256:[0-9a-f]{64}$")


def load_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path.name} must contain one JSON object")
    return payload


def decimal(value: object) -> Decimal:
    return Decimal(str(value))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def validate_state(state: dict[str, Any]) -> None:
    """Validate semantic invariants not expressible as simple field types."""

    schema = load_json(SCHEMA_PATH)
    require(
        schema.get("$schema") == "https://json-schema.org/draft/2020-12/schema",
        "programme-state schema must declare JSON Schema 2020-12",
    )
    require(state.get("schema_version") == SCHEMA_VERSION, "wrong schema_version")

    required = tuple(schema.get("required", ()))
    missing = [name for name in required if name not in state]
    require(not missing, f"programme state missing required fields: {missing}")
    allowed = set(schema.get("properties", {}))
    unexpected = sorted(set(state) - allowed)
    require(not unexpected, f"programme state has unexpected fields: {unexpected}")

    require(SHA40.fullmatch(str(state["validated_commit"])) is not None, "invalid validated_commit")
    validation = state["validation"]
    require(isinstance(validation, dict), "validation must be an object")
    require(SHA40.fullmatch(str(validation["merge_test_sha"])) is not None, "invalid merge_test_sha")
    require(SHA256.fullmatch(str(validation["comparison_hash"])) is not None, "invalid comparison_hash")

    suites = validation["suites"]
    require(isinstance(suites, list) and suites, "validation suites must be non-empty")
    names = [str(item["name"]) for item in suites]
    require(len(names) == len(set(names)), "validation suite names must be unique")
    for item in suites:
        passed = int(item["passed"])
        total = int(item["total"])
        require(total > 0, f"suite total must be positive: {item['name']}")
        require(passed == total, f"current manifest may declare only passing suites: {item['name']}")

    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    package_version = pyproject["project"]["version"]
    require(state["package_version"] == package_version, "package_version differs from pyproject.toml")

    block = state["reference_inverter_block"]
    modules_per_string = int(block["modules_per_string"])
    strings = int(block["strings"])
    module_power_wp = decimal(block["module_rated_power_wp"])
    inverter_kva = decimal(block["inverter_apparent_power_kva"])
    expected_modules = modules_per_string * strings
    expected_string_kwp = module_power_wp * modules_per_string / Decimal(1000)
    expected_dc_kwp = expected_string_kwp * strings
    expected_ratio = expected_dc_kwp / inverter_kva
    require(int(block["module_count"]) == expected_modules, "reference module_count arithmetic failed")
    require(decimal(block["string_rated_power_kwp"]) == expected_string_kwp, "reference string power arithmetic failed")
    require(decimal(block["dc_nameplate_power_kwp"]) == expected_dc_kwp, "reference DC power arithmetic failed")
    require(decimal(block["dc_ac_nameplate_ratio"]) == expected_ratio, "reference DC/AC ratio arithmetic failed")
    require(block["module_technology"] == "bifacial", "reference module technology must be bifacial")
    require(expected_modules == 720, "reference fixture must contain 720 modules")
    require(expected_dc_kwp == Decimal("475.2"), "reference fixture must equal 475.2 kWp DC")
    require(inverter_kva == Decimal("352"), "reference inverter must equal 352 kVA")

    capability_groups = state["capabilities"]
    seen: set[str] = set()
    for group_name in ("canonical", "provisional", "historical"):
        group = capability_groups[group_name]
        require(isinstance(group, list) and group, f"capability group {group_name} must be non-empty")
        overlap = seen.intersection(group)
        require(not overlap, f"capability classifications overlap: {sorted(overlap)}")
        seen.update(group)

    require("percentage" in state["progress_policy"].lower(), "progress policy must address numerical percentage claims")
    prohibited = {"weighted_programme_progress", "progress_percent", "completion_percentage"}
    require(not prohibited.intersection(state), "manual progress percentage field is prohibited")
    require((ROOT / state["current_quantum_spawn"]).is_file(), "current Quantum Spawn path does not exist")
    require((ROOT / state["current_trueself"]).is_file(), "current Trueself path does not exist")
    require(
        state["generated_outputs"] == [
            "README.md programme-state block",
            "progress-dashboard.html",
        ],
        "generated_outputs contract changed",
    )


def suite_rows(state: dict[str, Any]) -> str:
    return "\n".join(
        f"| {item['name']} | {item['passed']} / {item['total']} | PASS |"
        for item in state["validation"]["suites"]
    )


def render_readme_block(state: dict[str, Any]) -> str:
    block = state["reference_inverter_block"]
    return f"""{README_START}
## Current programme state

This block is generated from [`programme-state.json`](programme-state.json). CI fails if the manifest, this status block or [`progress-dashboard.html`](progress-dashboard.html) drift apart.

| Field | Current authority |
|---|---|
| Build | **{state['current_build']}** |
| Stage | {state['programme_stage']} |
| Package | `{state['package_version']}` |
| Last validated engineering commit | `{state['validated_commit']}` |
| Active gate | **{state['active_gate']}** |
| Next single goal | **{state['next_single_goal']}** |

### First complete product boundary

```text
{block['module_rated_power_wp']} Wp bifacial modules × {block['modules_per_string']} modules/string × {block['strings']} strings
= {block['module_count']} modules
= {block['dc_nameplate_power_kwp']} kWp DC
= one {block['inverter_apparent_power_kva']} kVA inverter block
DC/AC nameplate ratio = {block['dc_ac_nameplate_ratio']}
```

### Latest declared validation envelope

| Suite | Result | State |
|---|---:|---|
{suite_rows(state)}

Comparison hash: `{state['validation']['comparison_hash']}`

**Progress policy:** {state['progress_policy']}
{README_END}"""


def sync_readme(existing: str, block: str) -> str:
    if README_START in existing or README_END in existing:
        require(
            existing.count(README_START) == 1 and existing.count(README_END) == 1,
            "README programme-state markers are malformed",
        )
        start = existing.index(README_START)
        end = existing.index(README_END) + len(README_END)
        return existing[:start] + block + existing[end:]

    lines = existing.splitlines()
    require(lines and lines[0].startswith("# "), "README must start with a title")
    return "\n".join([lines[0], "", block, "", *lines[1:]]).rstrip() + "\n"


def list_items(items: list[str], css_class: str = "") -> str:
    class_attr = f' class="{css_class}"' if css_class else ""
    return "\n".join(f"<li{class_attr}>{html.escape(item)}</li>" for item in items)


def render_dashboard(state: dict[str, Any]) -> str:
    block = state["reference_inverter_block"]
    validation = state["validation"]
    suites = "\n".join(
        "<article class=\"card\"><span>{}</span><strong>{} / {}</strong><small>PASS</small></article>".format(
            html.escape(str(item["name"])), item["passed"], item["total"]
        )
        for item in validation["suites"]
    )
    canonical = list_items(state["capabilities"]["canonical"], "canonical")
    provisional = list_items(state["capabilities"]["provisional"], "provisional")
    historical = list_items(state["capabilities"]["historical"], "historical")
    limitations = list_items(state["known_limitations"], "limitation")

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="Generated engineering programme state for the Solar Electrical Topology Analysis Engine.">
<title>Solar Topology Engine · Programme Truth</title>
<style>
:root{{color-scheme:dark;--bg:#05090d;--panel:#0b151d;--line:#254052;--text:#edf8fd;--muted:#91a9b8;--good:#55dfa0;--active:#43cfff;--warn:#ffc95e;--historic:#a9a1d6}}
*{{box-sizing:border-box}}body{{margin:0;background:radial-gradient(circle at 12% 0,#14364d 0,var(--bg) 42%);color:var(--text);font:15px/1.55 system-ui,-apple-system,"Segoe UI",sans-serif}}header,main,footer{{max-width:1180px;margin:auto;padding:24px}}header{{padding-top:42px}}h1{{font-size:clamp(34px,7vw,68px);line-height:1;margin:.16em 0}}h2{{margin:32px 0 10px}}.kicker{{color:var(--active);font-weight:900;letter-spacing:.15em;font-size:12px}}.muted,small{{color:var(--muted)}}.pills,.grid,.columns{{display:grid;gap:12px}}.pills{{grid-template-columns:repeat(auto-fit,minmax(180px,1fr));margin:22px 0}}.pill,.card,.panel{{border:1px solid var(--line);background:linear-gradient(180deg,#0e1d27,var(--panel));border-radius:14px}}.pill{{padding:12px 14px}}.pill strong{{display:block;color:var(--active)}}.grid{{grid-template-columns:repeat(auto-fit,minmax(180px,1fr))}}.card{{padding:17px}}.card span,.card small{{display:block}}.card strong{{display:block;font-size:27px;margin:4px 0;color:var(--good)}}.panel{{padding:20px}}.boundary{{font:700 16px/1.7 ui-monospace,SFMono-Regular,Consolas,monospace;white-space:pre-wrap}}.columns{{grid-template-columns:repeat(3,1fr)}}ul{{margin:8px 0;padding-left:22px}}li{{margin:7px 0}}.canonical::marker{{color:var(--good)}}.provisional::marker,.limitation::marker{{color:var(--warn)}}.historical::marker{{color:var(--historic)}}code{{color:#bdeeff;word-break:break-all}}a{{color:var(--active)}}.policy{{border-left:4px solid var(--warn)}}@media(max-width:760px){{.columns{{grid-template-columns:1fr}}header,main,footer{{padding:18px}}}}
</style>
</head>
<body>
<header>
<div class="kicker">GLOBALGRID2050 · GENERATED PROGRAMME STATE</div>
<h1>Solar Topology Engine</h1>
<p class="muted">This page is generated from <a href="./programme-state.json">programme-state.json</a>. It contains no manually maintained completion percentage.</p>
<div class="pills">
<div class="pill"><small>Current build</small><strong>{html.escape(state['current_build'])}</strong></div>
<div class="pill"><small>Package</small><strong>{html.escape(state['package_version'])}</strong></div>
<div class="pill"><small>Active gate</small><strong>{html.escape(state['active_gate'])}</strong></div>
<div class="pill"><small>Next single goal</small><strong>{html.escape(state['next_single_goal'])}</strong></div>
</div>
</header>
<main>
<h2>First complete product boundary</h2>
<section class="panel boundary">{block['module_rated_power_wp']} Wp bifacial modules × {block['modules_per_string']} modules/string × {block['strings']} strings
= {block['module_count']} modules
= {block['dc_nameplate_power_kwp']} kWp DC
= one {block['inverter_apparent_power_kva']} kVA inverter block
DC/AC nameplate ratio = {block['dc_ac_nameplate_ratio']}</section>

<h2>Latest declared validation envelope</h2>
<section class="grid">{suites}</section>
<p class="muted">Workflow run <code>{validation['run_id']}</code> · artefact <code>{validation['artifact_id']}</code> · validated engineering commit <code>{state['validated_commit']}</code></p>
<p class="muted">Comparison hash <code>{validation['comparison_hash']}</code></p>

<h2>Capability authority</h2>
<section class="columns">
<div class="panel"><h3>Canonical</h3><ul>{canonical}</ul></div>
<div class="panel"><h3>Provisional</h3><ul>{provisional}</ul></div>
<div class="panel"><h3>Historical workbenches</h3><ul>{historical}</ul></div>
</section>

<h2>Known limitations</h2>
<section class="panel"><ul>{limitations}</ul></section>

<h2>Progress policy</h2>
<section class="panel policy">{html.escape(state['progress_policy'])}</section>

<h2>Continuity</h2>
<section class="panel">
<p>Current Quantum Spawn: <code>{html.escape(state['current_quantum_spawn'])}</code></p>
<p>Current Trueself checkpoint: <code>{html.escape(state['current_trueself'])}</code></p>
<p>Restore point: <code>{html.escape(state['restore_point'])}</code></p>
</section>
</main>
<footer>Generated deterministically by <code>scripts/sync_programme_state.py</code>. Engineering outputs remain evidence-qualified and are not a project-specific approval or compliance certificate.</footer>
</body>
</html>
"""


def expected_outputs(state: dict[str, Any]) -> tuple[str, str]:
    readme = README_PATH.read_text(encoding="utf-8")
    expected_readme = sync_readme(readme, render_readme_block(state))
    expected_dashboard = render_dashboard(state)
    return expected_readme, expected_dashboard


def write_outputs(state: dict[str, Any]) -> None:
    expected_readme, expected_dashboard = expected_outputs(state)
    README_PATH.write_text(expected_readme, encoding="utf-8")
    DASHBOARD_PATH.write_text(expected_dashboard, encoding="utf-8")


def check_outputs(state: dict[str, Any]) -> None:
    current_readme = README_PATH.read_text(encoding="utf-8")
    current_dashboard = DASHBOARD_PATH.read_text(encoding="utf-8")
    expected_readme, expected_dashboard = expected_outputs(state)
    failures = []
    if current_readme != expected_readme:
        failures.append("README.md programme-state block")
    if current_dashboard != expected_dashboard:
        failures.append("progress-dashboard.html")
    if failures:
        raise ValueError(
            "programme-state drift detected in: " + ", ".join(failures)
            + "; run python scripts/sync_programme_state.py --write"
        )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="fail when generated outputs drift")
    mode.add_argument("--write", action="store_true", help="rewrite generated outputs")
    args = parser.parse_args(argv)

    state = load_json(MANIFEST_PATH)
    validate_state(state)
    if args.write:
        write_outputs(state)
        print("programme state validated and generated outputs written")
    else:
        check_outputs(state)
        print("programme state validated; generated outputs are in sync")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ValueError as exc:
        print(f"programme-state error: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
