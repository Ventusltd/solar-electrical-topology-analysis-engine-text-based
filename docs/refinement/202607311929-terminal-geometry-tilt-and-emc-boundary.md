# Refinement 04 — Terminal Geometry, Tilt and EMC Boundary

Timestamp: 2026-07-31 19:29 +0100

## Current authority boundary

Build 025 has correctly replaced the former one-dimensional representation with explicit two-dimensional plan geometry. It can now calculate routed conductor length, crossings, conductor separation, signed loop area and absolute winding area from deterministic polylines.

The current reference result remains conditional because:

- positive and negative module-terminal offsets default to the same unresolved point;
- terminal evidence is `generic_unresolved`;
- pole and interconnect separation are introduced by routing constants;
- geometry is expressed in plan coordinates without explicit table tilt, terrain elevation or vertical route transitions.

Therefore, the current sequential-versus-leapfrog percentages are valid for the declared Build 025 fixture. They shall not be presented as universal module or site values.

## Terminal geometry refinement

Every module product or geometry case shall support independently evidenced local terminal coordinates:

```text
negative terminal u, v, w
positive terminal u, v, w
terminal exit direction
factory lead length by polarity
factory lead routing constraint
junction-box arrangement
module orientation applicability
source reference
source revision
evidence class
```

The engine shall distinguish:

- one central junction box;
- split junction boxes;
- terminals near opposite long-edge positions;
- asymmetric positive and negative lead lengths;
- custom manufacturer lead geometry;
- unresolved generic geometry.

Changing terminal coordinates or lead routing shall change the route and receipt hashes even when module centres and electrical membership remain unchanged.

## Geometry dimensionality

Every geometry receipt shall declare its dimensionality:

```text
plan_2d
table_plane_2d
site_3d
```

`plan_2d` means all reported lengths and areas are plan projections unless explicitly identified otherwise.

`table_plane_2d` means geometry is solved in the inclined module or table plane and can be transformed into site coordinates.

`site_3d` means every route vertex has authoritative `x`, `y` and `z` coordinates, including table elevation, terrain, drops, risers, trench depth, inverter-entry height and service loops where represented.

## Tilt and coordinate transform

A table-plane coordinate shall be transformed into site coordinates using an evidenced origin, azimuth, tilt and local basis. The exact convention must be versioned and tested.

Route length shall be calculated segment by segment as:

```text
length = sqrt(dx² + dy² + dz²)
```

A universal multiplication of every plan route by `1 / cos(tilt)` is prohibited. That factor is valid only for a component whose horizontal projection lies wholly along the tilt direction on a planar surface. Transverse and vertical route components require their own geometry.

For a planar loop whose scalar area was calculated as a horizontal projection, the table-plane area may scale by `1 / cos(tilt)`. The receipt must state which plane each area inhabits rather than applying this correction invisibly.

## Area quantities

The engine shall expose distinct geometric quantities:

```text
signed area in declared loop plane
absolute winding area in declared loop plane
oriented signed area vector for planar three-dimensional loops
projected area normal to a declared field direction
```

For a simple or self-crossing planar loop, signed area preserves winding sign and absolute winding area integrates `|winding number|`.

Mean pole separation multiplied by parallel-run distance is not an area decomposition. It may be reported as a route-pairing diagnostic but shall not be used to assert what percentage of total winding area is paired or unpaired.

## Electromagnetic interpretation

For a spatially uniform magnetic field, flux linkage is governed by the oriented signed area:

```text
Phi(t) = B(t) dot A_signed_vector
```

Counter-wound lobes can cancel in this case.

For a spatially varying field, including a nearby lightning channel, the required quantity is:

```text
Phi(t) = integral over A of w(x, y) × B(x, y, t) dot n(x, y) dA
```

The winding sign, field magnitude, field direction and spatial variation all matter.

Absolute winding area is not by itself the close-strike flux. It supports a conservative geometric bound such as:

```text
|Phi| <= B_normal_max × absolute_winding_area
```

only when `B_normal_max` is a defensible bound over the represented surface.

Induced voltage then requires:

```text
v_induced(t) = -dPhi/dt
```

No induced-voltage value shall be calculated from loop area alone without a declared field or source model and its spatial relationship to the routed loop.

## Build 027 source models

Build 027 shall define separate source cases rather than one generic loop-area multiplier:

1. uniform-field screening case;
2. distant lightning-channel approximation;
3. finite-distance channel with spatially varying field;
4. bounded worst-case normal-field envelope;
5. measured or imported field map;
6. common-mode coupling against frame, structure and earth.

Every source case shall preserve geometry, rise time or waveform, channel or source location, field orientation, applicability range and evidence provenance.

## Sensitivity requirements

The reference 24 by 30 comparison shall be rerun across controlled geometry cases including:

- unresolved coincident terminals;
- central split terminals;
- realistic separated terminal positions;
- asymmetric lead lengths;
- multiple interconnect lane offsets;
- multiple pole separations;
- tilt angles including 0, 10, 20 and 30 degrees;
- inverter positions on more than one side of the table;
- plan-only and full three-dimensional route representations.

The output shall identify which conclusions are stable and which are sensitive to unresolved geometry.

## Acceptance gate

This refinement is complete only when:

1. terminal coordinates are replaceable, evidenced and included in deterministic hashes;
2. geometry receipts state whether values are plan, table-plane or site-three-dimensional;
3. true route lengths are derived from three-dimensional vertices where tilt or elevation is claimed;
4. signed area, absolute winding area and oriented area vector are not conflated;
5. Build 027 flux and induced-voltage calculations use a declared field model;
6. reports identify current Build 025 percentages as fixture-specific until the terminal and tilt evidence is resolved.
