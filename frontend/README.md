# frontend/

This folder contains the standalone HTML frontends served by the Flask app or embedded as iframes.

| File | Description |
|---|---|
| `assistant.html` | Main standalone assistant UI (voice + text, 6 languages, EN language button) |
| `widget_voice.html` | Full-width split layout — Assistant orb (left) + Training link (right) |

## Deployment

Both files are served statically. In production they are hosted on Azure Web App alongside `app.py`.
For WordPress, use the blocks in `../wp-blocks/` which embed these as iframes.

## Language Support

EN · FR · AR · ES · PT · SW — auto-detected from browser, switchable via button.

## ENV dependency

`assistant.html` calls `/ask` on the same origin. No hardcoded API endpoint.
If you change the backend URL, update the `API_URL` constant at the top of each file.
