# wp-blocks/

WordPress-ready HTML blocks for childlink-ma.org.
Each file is a self-contained block to paste into a WordPress **Custom HTML** block.

| File | Page | Description |
|---|---|---|
| `wp_privacy_block.html` | `/privacy/` | GDPR privacy policy — EN/FR/AR, subprocessors, SCC, Art. 30 register |
| `wp_cgu_block.html` | `/cgu/` | Terms of use — 6 languages, auto-detect |
| `wp_guidelines_scroll.html` | `/trusted-resources/` | 13 clinical guidelines, horizontal scroll, ASD/T21 badges, DOI links |

## Usage

1. In WordPress editor, add a **Custom HTML** block
2. Paste the full content of the relevant file
3. Save / update the page

All blocks use `CLM_CONTENT` JS injection and auto-detect browser language.
RNA W941020510 is referenced throughout for legal traceability.
