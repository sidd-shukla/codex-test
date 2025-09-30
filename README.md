# codex-test

This repository hosts a simple static web page that welcomes visitors and displays the current local time on demand.

## Project structure

- `index.html` – A self-contained HTML page that shows a "Welcome" heading and a button. Clicking the button displays the visitor's current date and time using their device's locale and timezone settings.

## Getting started

1. Start a lightweight web server from the repository root (for example, using Python):
   ```bash
   python -m http.server 8000
   ```
2. Open your browser and navigate to [http://localhost:8000/](http://localhost:8000/).
3. Click **Show Current Time** to see the date and time formatted for your locale.

No build steps are required; the page runs entirely in the browser.
