

BUILD THIS PRODUCT USING PYTHON + STREAMLIT ONLY (NO SQL DATABASE)

STACK (MANDATORY)

UI + App: Streamlit only.

No Node.js, no REST API, no PostgreSQL, no SQLite, no ORM, no migrations.

Data source: in-memory Python dictionaries (seeded from a Python module). Optionally load from a JSON file at startup, but canonical format remains a Python dict.

DATA STORAGE RULES

Recipe & Item database

Must live as Python dictionaries in code.

Provide a single source of truth file:

data/satisfactory_db.py

Structure must include:

Items: id, name, category, stackSize, isRawResource

Recipes: id, name, category, unlockTier, machineType, powerConsumption, craftingSpeed, alternateRecipe, inputs, outputs

Use stable IDs (string UUID-like or slug IDs). Do not generate IDs at runtime.

User configuration (unlocked recipes)

Must persist in browser localStorage (primary).

Implement localStorage read/write via:

Streamlit custom component (components/local_storage/)

Or st.components.v1.html with JS postMessage bridge.

Fallback if localStorage is blocked:

Allow Export/Import of unlocked recipe set as JSON.

Saved calculations

Stored as downloadable JSON files only (no server-side persistence).

Optional: allow “save to browser localStorage” as well (same component).

CORE ALGORITHM REQUIREMENTS

Input: target item, target rate (items/min), unlocked recipes set, optimization priority.

Output:

Machine nodes with counts, inputs/min, outputs/min, power/machine, total power

Connections with item flow rates

Raw resource totals

Status: success | insufficient_recipes | impossible_rate | resource_warning

Must handle:

Multiple recipe options per item (choose best per objective; optionally show top 2–3 variants)

Missing recipes -> clear error + list missing recipes + “temporarily enable locked recipes” preview

Large diagrams (50+ machines): provide collapse by stage/category + search/filter

Circular dependencies: detect and mark as recycling loop edges

VISUALIZATION + EXPORT

Diagram rendering:

Use Graphviz to generate SVG (preferred) and PNG.

Provide zoom/pan by embedding SVG in HTML with a lightweight pan/zoom script.

Tooltips:

Implement via SVG <title> per node for hover tooltips (works natively).

On click: show details panel in Streamlit (selected node data).

Export:

SVG (download)

PNG (download)

JSON (download) including: inputs, unlocked recipes, chosen recipes, nodes, edges, totals, timestamp

FILES TO GENERATE (REQUIRED)

/app
streamlit_app.py # main UI
optimizer/solver.py # chain computation + optimization
optimizer/models.py # dataclasses/types for nodes/edges/results
optimizer/objectives.py # scoring functions for priorities
viz/graphviz_render.py # build DOT + render SVG/PNG
storage/local_storage_component.py # JS bridge for localStorage
storage/import_export.py # JSON import/export helpers
data/satisfactory_db.py # Python dict DB (items, recipes)
utils/validation.py # input validation + error messages
README.md

IMPLEMENTATION ORDER (KEEP)

P0:

Target item select + rate input + priority select

LocalStorage recipe unlock config UI (checkbox list)

Compute chain (at least for a meaningful subset of recipes) and show nodes/edges summary

Render diagram SVG with hover tooltips

Errors for insufficient recipes

P1:

Optimization objective improvements (machine/power/waste)

Auto-recalc on input change

50+ machines handling: collapse groups + search/filter

Export SVG/PNG/JSON

P2:

Variant comparison (show alternate solutions)

Recycling loop styling + explicit loop labeling

Import JSON to restore a previous calculation

DEFAULTS (IF TBD)

Start with a curated subset of Satisfactory recipes (enough to demonstrate multi-stage chains: iron/copper/steel + a few advanced items). No placeholders; include real values you provide.