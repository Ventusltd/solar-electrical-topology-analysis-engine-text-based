from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WARNING = (
    "Ideal bulk-copper screening calculation using nominal metallic area. "
    "Not a finished-cable declared resistance and not an IEC 60228 "
    "maximum-resistance calculation."
)


def test_v6_exposes_machine_readable_lower_bound_resistance_model() -> None:
    physics = (ROOT / "physics.generated.js").read_text(encoding="utf-8")

    assert "basis: 'ideal_bulk_estimate'" in physics
    assert "valueKind: 'lower_bound_estimate'" in physics
    assert "resistanceModel:RESISTANCE_MODEL" in physics
    assert WARNING in physics
    assert "RHO_CU20 = 1.724e-8" in physics


def test_v6_injects_visible_resistance_authority_warning() -> None:
    physics = (ROOT / "physics.generated.js").read_text(encoding="utf-8")
    index = (ROOT / "index.html").read_text(encoding="utf-8")

    assert "legacyResistanceAuthority" in physics
    assert "RESISTANCE AUTHORITY · HISTORICAL LOWER-BOUND SCREEN" in physics
    assert "./physics.generated.js" in index


def test_v9_displays_and_exports_lower_bound_resistance_model() -> None:
    page = (ROOT / "v9-sandbox" / "index.html").read_text(
        encoding="utf-8"
    )
    app = (ROOT / "v9-sandbox" / "app.js").read_text(encoding="utf-8")
    engine = (
        ROOT / "v9-sandbox" / "debug" / "engine.js"
    ).read_text(encoding="utf-8")

    assert "RESISTANCE AUTHORITY · HISTORICAL LOWER-BOUND SCREEN" in page
    assert "ideal_bulk_estimate" in page
    assert "basis: \"ideal_bulk_estimate\"" in app
    assert "valueKind: \"lower_bound_estimate\"" in app
    assert "resistanceModel: project.resistanceModel" in app
    assert "RESISTANCE_MODEL_LOWER_BOUND" in app
    assert WARNING in app
    assert "COPPER_RESISTIVITY_20C_OHM_MM2_PER_M = 0.017241" in engine


def test_legacy_warnings_do_not_claim_v10_authority() -> None:
    v6 = (ROOT / "physics.generated.js").read_text(encoding="utf-8")
    v9 = (ROOT / "v9-sandbox" / "app.js").read_text(encoding="utf-8")

    assert "authorityStatus: 'historical_reference'" in v6
    assert "authorityStatus: \"historical_reference\"" in v9
