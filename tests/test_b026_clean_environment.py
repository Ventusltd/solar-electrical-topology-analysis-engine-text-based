from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import tomllib


ROOT = Path(__file__).resolve().parents[1]
DISTRIBUTION = "solar-electrical-topology-engine"


def venv_python(environment: Path) -> Path:
    if os.name == "nt":
        return environment / "Scripts" / "python.exe"
    return environment / "bin" / "python"


def run(command: list[str], *, cwd: Path, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=cwd,
        env=env,
        check=True,
        text=True,
        capture_output=True,
    )


def test_b026_clean_environment_provisioning() -> None:
    project = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    expected_version = project["project"]["version"]

    with tempfile.TemporaryDirectory(prefix="b026-clean-environment-") as raw:
        workspace = Path(raw).resolve()
        environment = workspace / "venv"
        probe_dir = workspace / "probe"
        probe_dir.mkdir()

        run([sys.executable, "-m", "venv", str(environment)], cwd=workspace)
        python = venv_python(environment)
        run(
            [
                str(python),
                "-m",
                "pip",
                "install",
                "--disable-pip-version-check",
                str(ROOT),
            ],
            cwd=workspace,
        )

        probe = run(
            [
                str(python),
                "-c",
                (
                    "import importlib.metadata, json, pathlib, solar_topology; "
                    "print(json.dumps({"
                    "'version': importlib.metadata.version('solar-electrical-topology-engine'),"
                    "'module_path': str(pathlib.Path(solar_topology.__file__).resolve())"
                    "}, sort_keys=True))"
                ),
            ],
            cwd=probe_dir,
            env={
                **{key: value for key, value in os.environ.items() if key != "PYTHONPATH"},
                "PYTHONNOUSERSITE": "1",
            },
        )
        payload = json.loads(probe.stdout.strip())

        assert payload["version"] == expected_version
        assert not Path(payload["module_path"]).is_relative_to(ROOT)
