# Restore point — before fixed physical module geometry

Created before replacing the V8 browser renderer.

The exact pre-change `v8-leapfrog/app.js` is recoverable from Git blob:

`6df4d476d682a34b2ec30408a94bb7d9cdf04a65`

The pre-change V8 index blob is:

`9243abf8cd1c6c7f0cdb79f32c5443ca45beb945`

The pre-change V8 stylesheet blob is:

`8347d3261a3665a30e13e7518bca18df2d29ca11`

Reason for change: the old diagram did not make the invariant physical order of modules sufficiently explicit. The replacement must keep M1 through M30 in fixed left-to-right positions in both sequential and leapfrog views, changing only the electrical connection order and external cable routes.
