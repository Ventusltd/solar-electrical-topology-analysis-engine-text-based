# Working Root Engine vs Independent V7 Development Engine

## Separation rule

The working root engine at `/` remains the stable live reference. The independent V7 development engine lives entirely under `/v7-development/`. V7 does not import, overwrite or modify the root `index.html`, `styles.css`, `app.js`, `physics.generated.js` or navigation files.

## Browser links

- Working root engine: `https://ventusltd.github.io/solar-electrical-topology-analysis-engine-text-based/`
- Independent V7 engine: `https://ventusltd.github.io/solar-electrical-topology-analysis-engine-text-based/v7-development/`

## Comparison

| Capability | Working root engine | Independent V7 |
|---|---|---|
| Stability role | Live reference | Experimental workspace |
| Deployment isolation | Root application | Self-contained single page |
| Blank-screen failure containment | Root can only be affected by root-file edits | V7 failure cannot alter root |
| Header status | V6 complete circuit | V7 in development / use at own risk |
| Row length | Existing geometry implementation | `N × width + (N−1) × gap` shown explicitly |
| User-entered route length | Existing ruler only | No generated string length input |
| Wiring topology | Existing generated arrangement | Sequential and leapfrog scenarios |
| Plant population | Inverter archetype | 900 inverters / 18,918 strings / 24-input maximum basis |
| Fleet occupancy | Not central | Actual average strings per inverter calculated |
| Module leads | Included | Positive and negative lead lengths separated |
| Cable resistance | Existing general calculation | 6 mm² home-run and 4 mm² module-lead R20 inputs separated |
| Connector model | Contact count | Mated-interface count and resistance basis |
| Inductance | Segmented screening | Low-frequency value with internal L and high-frequency value without internal L |
| Capacitance | Existing placeholder scenario | Dry effective-area and wet full-area scenarios |
| Model selection | Existing rise-time banner | Rise time compared with round-trip time, with margin |
| MPPT allocation | Basic sequential assignment | Pairing review with within-band / forced-cross-band identification |
| Export | Study JSON | Independent V7 JSON with all inputs, strings and MPPT pairs |

## V7 limitations

V7 remains a screening model. It does not yet provide:

- measured installation provenance;
- a PEEC or three-dimensional field solution;
- frequency-dependent conductor losses;
- validated inverter input impedance;
- quantitative SPD selection;
- insulation-monitor certification;
- as-built route verification;
- a full 18,918-string headless site instance generator.

## Acceptance tests before V7 can replace the root engine

1. Root and V7 must produce identical results for a deliberately common V6 case.
2. Row-span golden tests must cover one module, thirty modules and arbitrary gaps.
3. No generated route length may be supplied directly by a user.
4. Conductor diameter, not cable outside diameter, must drive the `acosh` geometry term.
5. Low-frequency loop inductance must include `μ0/(4π)` H/m internal loop inductance.
6. High-frequency inductance must remove internal inductance.
7. Sequential and leapfrog geometry must visibly and numerically diverge.
8. Connector resistance must state whether it is per mated pair, contact half or measured total.
9. Dry and wet capacitance inputs must retain provenance and never be presented as measured by default.
10. V7 must remain operable with the root engine unchanged.
