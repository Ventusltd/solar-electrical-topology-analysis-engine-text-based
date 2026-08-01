from __future__ import annotations

import importlib.util
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "check_capsule_links.py"
EXPECTED_POINTERS = {
    "202607311620-system-architecture.md": (
        "202607311615-system-architecture.md",
        "System Architecture",
    ),
    "202607311640-geometry-authority.md": (
        "202607311619-geometry-authority.md",
        "Geometry Authority",
    ),
    "202607311700-array-engine.md": (
        "202607311624-array-engine.md",
        "Array Engine and Topology Authority",
    ),
    "202607311720-physics-emc-lightning.md": (
        "202607311627-physics-emc-lightning.md",
        "Physics, EMC and Lightning",
    ),
    "202607311740-standards-validation.md": (
        "202607311628-standards-validation.md",
        "Standards and Validation",
    ),
    "202607311820-respawn-instructions.md": (
        "202607311652-respawn-instructions.md",
        "Respawn Instructions and Operating Protocol",
    ),
}


def load_checker():
    spec = importlib.util.spec_from_file_location("check_capsule_links", SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_title_verified_compatibility_pointer_mapping() -> None:
    checker = load_checker()
    root = ROOT / "docs" / "quantum-spawn"

    for pointer_name, (target_name, expected_title) in EXPECTED_POINTERS.items():
        pointer = root / pointer_name
        target = root / target_name
        assert pointer.is_file()
        assert target.is_file()
        assert expected_title in pointer.read_text(encoding="utf-8")
        assert checker.canonical_title(target) == expected_title
        assert checker.check_compatibility_pointer(
            pointer,
            pointer.read_text(encoding="utf-8"),
        ) == ()

    commercial = root / "202607311640-commercial-strategy.md"
    assert commercial.is_file()
    assert checker.canonical_title(commercial) != "Geometry Authority"


def test_all_quantum_spawn_and_trueself_markdown_links_resolve() -> None:
    checker = load_checker()
    issues = checker.check_capsule_links()
    assert issues == (), "\n".join(issue.message() for issue in issues)


def test_capsule_link_check_command_passes() -> None:
    completed = subprocess.run(
        [sys.executable, str(SCRIPT), "--check"],
        cwd=ROOT,
        check=False,
        text=True,
        capture_output=True,
    )
    assert completed.returncode == 0, completed.stderr
    assert "capsule-link integrity passed" in completed.stdout
