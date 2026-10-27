Resource paths in this reference are relative to the parent skill directory unless a link specifies otherwise.

### Calendar

- Use the bundled compact `<viz-calendar>` for a day schedule. Read [Calendar](../widgets/calendar.md) and start from the [example](../examples/calendar.html). Supply verified dates and events; the component handles durations, overlap lanes, and responsive layout. Short blocks show the title; hover, focus, or tap reveals the full title, time, and detail. Do not stretch the schedule to fit secondary text or wrap the element in another card.

### Interactive explainer or simulation

- Use compact controls or status, one compact dominant visual, and at most one single-line selected-state detail. Default to no summary cards; allow up to three only when changing metrics are central.
- Crop empty space and fit the available inline width. For step-throughs, add only requested step controls and update one current visual; never add parameter controls, formulas, metric cards, or side-by-side steps unless asked.

### Graphs and plots

- Use D3 for data-rich Cartesian or statistical plots and handwritten SVG for simple, directly labeled values. Keep diagrams, simulations, and maps under their existing guidance. Load the version-pinned approved-CDN script `https://cdn.jsdelivr.net/npm/d3@7.9.0/dist/d3.min.js`.
- Render the figure, legend, and subplots directly on the transparent host surface. Frame only the SVG plot area; never wrap charts in `.card`, rounded panels, filled backgrounds, or shadowed containers.
- Give the figure a concise visible title. Render each Cartesian subplot in its own responsive SVG with a matching `viewBox`, a thin frame, and visible `text.axis-title[data-axis="x"]` and `text.axis-title[data-axis="y"]` showing quantities and units.
- Set each SVG `viewBox` from its own container's measured width, redraw with `ResizeObserver`, and reserve at least 64px for the y axis. Never scale down a fixed-width `viewBox`.
- Derive padded domains with `d3.extent(...)` over all observations, uncertainty, and references. Inset scale ranges for marker radii and keep every path inside `rect[data-chart-frame]`; never draw endpoint connectors outside the frame or guess or hard-code the domain.
- After every draw, measure tick, axis, and value-label bounds together. Leave 4px between labels, anchor edge labels inward, and remove optional annotations first. At 360px, show at most four x ticks and stack panels.
- Prefer `--viz-series-1` through `--viz-series-6` for chart series; use `--foreground` and `--border` for neutrals, cycle the six series tokens when more are needed, and never use literal or fallback colors. Give every SVG label `fill: var(--foreground)` and `font-size: 12px`; never shrink labels below 11 screen pixels. Stack subplots when their labels no longer fit.
- Keep observations, trends, and important values visible. Use bands for dense uncertainty, whiskers for isolated estimates, and one compact, wrapping legend. Render one real `<button type="button" aria-pressed="true">` per series with a small swatch and neutral text; toggle its line, markers, and tooltip row together. Keep buttons transparent, borderless, and indistinguishable from inline text; never use `.btn`, pills, badges, rounded borders, or filled and selected backgrounds.
- Share one root-relative, pointer-transparent `<div class="tooltip" role="tooltip">` using `--popover` and `--popover-foreground`. In each multi-series SVG, give the full-plot overlay both `data-chart-hit` and `data-chart-hover-overlay="cross-series"`. Keep the `data-chart-hover-guide` at the exact cursor x, interpolate every visible series there, and show one aligned `data-chart-hover-marker` and tooltip row per visible series; never snap the guide to a nearby sample. Let touch users pin the same cross-series details without requiring hover.
- Find ordered observations with `d3.bisector(d => d.x).center(values, x)`; never pass an accessor to `d3.bisectCenter`.
- Give isolated marks transparent `data-chart-hit` targets at least 32 screen pixels across on fine pointers and about 44px on coarse pointers; use one nearest-point overlay for dense scatter.
- For named numeric data and one-off analyses, start with the plot. Put values and takeaways on its marks, axes, or annotations. Never add a KPI row, controls, cards, or panels unless those UI elements are explicitly requested.
- For sequences or parallel work, use aligned lanes on one time axis. Encode phase and resource in the marks; annotate totals, waits, and bottlenecks on the axis or lanes, not above the plot.
- For distributions or multi-metric comparisons, use shared-scale facets or small multiples. Render every requested dimension simultaneously; never hide one behind a toggle.

### Maps

- Let the map dominate the composition. Use at most one compact selection/detail area and only requested controls.
- Always project published GeoJSON/TopoJSON and sourced longitude/latitude with `d3-geo`; never hard-code or hand-draw geographic outlines. Use schematic maps only when asked.
- For world countries, import `https://esm.sh/@d3-maps/atlas@1.0.0/world/countries/countries-110m` and convert it with `topojson-client@3.1.0` using `feature(world, world.objects.features).features`. Join input ISO3 directly to `feature.properties.id`, which is already ISO3; do not convert it to numbers.
- For US states or counties, use `https://cdn.jsdelivr.net/npm/us-atlas@3/counties-10m.json/+esm`. For ZIP/ZCTA or city boundaries, download official Census or local open-data GeoJSON; do not guess sibling atlas paths or import raw JSON as JavaScript.
- Keep maps geographically legible: for local points, fetch published neighborhood, street, or comparable geometry; a blank field or lone administrative outline is not a basemap. Show the full city or region behind points or partial choropleths, and frame the locations with modest padding.
- Include the verified geometry in the final HTML. Open it before replying and fix blank basemaps, failed imports, missing labels, or unprojected points.

### Dense categorical grid

- Use one compact horizontal selected-item summary, then a grid with exactly one readable identifier per cell, then one small legend. Render only that identifier as visible cell text; put all other metadata in an accessible label or one summary line, not badges or fact grids. Allow only selection unless asked.

### Part-to-whole or time allocation

- Use compact metrics and one stacked chart of category allocation per period. Never substitute totals-only bars or duplicate it as a heatmap and totals chart.

