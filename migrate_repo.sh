#!/usr/bin/env bash
# ============================================================
# migrate_repo.sh
# Run this locally ONCE to restructure childlink-ma/ChildLink-ma
# into the new ChildLink-assistant layout.
#
# Prerequisites:
#   - git clone https://github.com/childlink-ma/ChildLink-ma
#   - cd ChildLink-ma
#   - Then run this script from the repo root
# ============================================================

set -e

echo "=== Step 1: Create new folders ==="
mkdir -p frontend wp-blocks .github/workflows

echo "=== Step 2: Move widget.html → frontend/assistant.html ==="
# widget.html is the current assistant frontend
git mv widget.html frontend/assistant.html

echo "=== Step 3: Add new files from this pack ==="
# Copy the following files from the pack you downloaded:
#   .env.example         → repo root
#   .gitignore           → repo root (replace existing)
#   README.md            → repo root (replace existing)
#   CONTRIBUTING.md      → repo root (replace existing)
#   SECURITY.md          → repo root (replace existing)
#   frontend/README.md   → frontend/
#   wp-blocks/README.md  → wp-blocks/
#   tests/test_ask.py    → tests/
#   .github/workflows/docker-build.yml → .github/workflows/
#
# Then add your actual HTML files:
#   cp /path/to/assistant.html    frontend/assistant.html    (overwrites)
#   cp /path/to/widget_voice.html frontend/widget_voice.html
#   cp /path/to/wp_privacy_block.html    wp-blocks/
#   cp /path/to/wp_cgu_block.html        wp-blocks/
#   cp /path/to/wp_guidelines_scroll.html wp-blocks/

echo "=== Step 4: Update app.py — serve frontend/assistant.html ==="
# In app.py, the route /widget.html currently serves widget.html from root.
# After migration it should serve frontend/assistant.html.
# Change this line in app.py:
#   path = os.path.join(app.root_path, "widget.html")
# To:
#   path = os.path.join(app.root_path, "frontend", "assistant.html")
#
# Also add a route for widget_voice.html:
#   @app.route("/widget_voice.html")
#   def serve_widget_voice():
#       path = os.path.join(app.root_path, "frontend", "widget_voice.html")
#       return send_file(path, mimetype="text/html")

echo "=== Step 5: Add GitHub secrets ==="
# In GitHub repo Settings → Secrets and variables → Actions, add:
#   DOCKERHUB_USERNAME
#   DOCKERHUB_TOKEN

echo "=== Step 6: Commit and push ==="
# git add -A
# git commit -m "refactor: restructure into assistant repo layout v0.4"
# git push origin main

echo ""
echo "Done. Checklist:"
echo "  [ ] .env.example in root"
echo "  [ ] frontend/assistant.html"
echo "  [ ] frontend/widget_voice.html"
echo "  [ ] wp-blocks/ (3 files)"
echo "  [ ] app.py updated (2 route paths)"
echo "  [ ] .github/workflows/docker-build.yml"
echo "  [ ] GitHub secrets: DOCKERHUB_USERNAME, DOCKERHUB_TOKEN"
echo "  [ ] Optionally rename repo to ChildLink-assistant in GitHub Settings"
