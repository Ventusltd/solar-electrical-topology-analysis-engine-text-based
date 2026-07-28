# V9 solar DC computation debug mirror

This folder is the canonical V9 engineering logic.

## Files

- `engine.js` — pure computation functions and canonical project report.
- `tests.js` — deterministic unit checks and Claude-readable review questions.
- `CLAUDE.md` — mandatory AI review discipline.

## Governing chain

Input configuration → validated allocation → module objects → electrical order → terminal references → ordered segments → voltage/resistance/loss calculations → warnings → report.

The browser UI is deliberately thin. It imports this folder and displays its output. It must not independently calculate topology, voltage, resistance, cable length or warnings.

## Current trusted scope

- 1–100 MPPT positions.
- 0–4 requested inputs per MPPT.
- 24 active-string development cap.
- 1–30 modules per string.
- Sequential, leapfrog, mirrored sequential, alternating return and validated custom order.
- Corrected open-circuit voltage using a user-supplied cell temperature.
- Copper conductor resistance screening.
- Home-run and provisional module-interconnect extension quantities.

## Explicit limitations

Exact junction-box positions, lead exit directions, connector coordinates, cable routing, support geometry, conductor material choices, contact resistance, mismatch, bypass-diode behaviour, inverter input impedance, capacitance, inductance and transmission-line effects are not yet represented.

The interconnect extension value is only a centre-to-centre screening estimate. It must not be issued as a construction cable schedule.

## Test and review

Open the V9 page and download the JSON report. The report contains the full input, assumptions, objects, segments, calculations, warnings and deterministic test results for review by Claude or another engineering agent.