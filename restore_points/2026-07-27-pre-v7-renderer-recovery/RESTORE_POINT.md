# Restore point — before V7 renderer recovery

Created before replacing the independent V7 schematic stack renderer with the proven geometry-based array representation.

## Protected working version

The root V6 application is not modified by this change.

## V7 file before change

- Path: `v7-development/index.html`
- Blob SHA: `ef31016a0922a2729d23187ca52c3ded4eb9d09c`
- Last known V7 commit before renderer recovery: `43aa0f60ab857b2637c7f345c507cb5e50a0ef1e`

## Recovery

Restore `v7-development/index.html` from blob `ef31016a0922a2729d23187ca52c3ded4eb9d09c` if the new renderer fails.

## Scope

Only the independent V7 page may change. Root `index.html`, `app.js`, `styles.css`, `physics.generated.js` and `spider-navigation.js` must remain untouched.
