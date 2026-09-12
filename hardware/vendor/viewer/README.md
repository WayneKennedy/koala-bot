# Static viewer dependencies

Vendored so the viewer and its geometry worker also work without CDN access.
Both libraries use the MIT licence, retained alongside the source bundles.

- Three.js r128: [source tag](https://github.com/mrdoob/three.js/tree/r128),
  `three-r128.min.js` from the cdnjs r128 distribution.
- three-mesh-bvh 0.5.23: [source tag and API](https://github.com/gkjohnson/three-mesh-bvh/tree/v0.5.23),
  UMD bundle from the matching npm distribution. Compatible with this Three.js
  generation; used for geometric intersection tests, not visual mesh changes.

The viewer build copies these files to its static output. Node.js runs the
same worker geometry engine to warm caches at build time; no npm install or
JavaScript build service is required on the viewing device.
