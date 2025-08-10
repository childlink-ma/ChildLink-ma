# Data contract (not committed)
Place your corpus here (not tracked by git). Expected default file:
- `data/chunks_enriched.json` — list of { content, source_pdf, [org], [year], [topic] }

Fields:
- content: string (required) — chunk text
- source_pdf: string — original document name (used as org/source)
- org/year/topic: optional hints; year may be empty (we won't print “NC”)
