# codex-test

This repository hosts a simple static web page that welcomes visitors, displays an inspirational thought of the day, and shows the current local time on demand. It now also includes a command-line helper that calls DHL's public tracking API to look up shipment statuses.

## Project structure

- `index.html` – A self-contained HTML page that fetches and renders a random inspirational quote, and provides a button that reveals the visitor's current date and time using their device's locale and timezone settings.

## Getting started

1. Start a lightweight web server from the repository root (for example, using Python):
   ```bash
   python -m http.server 8000
   ```
2. Open your browser and navigate to [http://localhost:8000/](http://localhost:8000/).
3. Review the thought of the day automatically loaded from the internet. The page first tries to fetch a quote from [DummyJSON's quote API](https://dummyjson.com/quotes/random) and, if that is unavailable, from [ZenQuotes](https://zenquotes.io/api/random). When both networks fail, an on-device quote is shown so the page still surfaces an uplifting thought.
4. Click **Show Current Time** to see the date and time formatted for your locale.
No build steps are required; the page runs entirely in the browser.

## DHL shipment tracking helper

- `track_dhl.py` – Prompts for a DHL tracking number, calls the public tracking API, and prints the latest shipment status description.
- `test_track_dhl.py` – Unit tests that exercise the core tracking logic without calling the external API.

### Running the tracker

1. Create a free DHL Developer account:
   1. Visit the [Shipment Tracking API product page](https://developer.dhl.com/api-reference/shipment-tracking#get-started-section) and click **Get Access**.
   2. Sign in with an existing DHL developer account or choose **Register now** to create one. Complete the required profile details and confirm your email address if prompted.
2. Request credentials for the *Shipment Tracking – Unified* API:
   1. From the product page, select **Subscribe** (or **View Subscriptions** if you have already subscribed).
   2. Choose the **Sandbox** environment, accept the terms, and submit the form. The portal displays your newly generated **API Key** (sometimes labelled *Client ID*).
   3. Copy the key—the script calls the Shipment Tracking – Unified endpoint directly with this value.
3. Export the key so the script can authenticate requests in your current shell session:
   ```bash
   export DHL_API_KEY="your_api_key"
   ```
   On Windows PowerShell, run `setx DHL_API_KEY "your_api_key"`, then open a new terminal for the change to take effect.
4. Execute the helper and enter a tracking number when prompted:
   ```bash
   python track_dhl.py
   ```
   The script sends the tracking number to DHL using your API key. If a shipment is found, the latest status description is written to standard output. Any API or network issues are reported on standard error so you can troubleshoot quickly.

### Running the tests

Follow these steps to execute the mocked test suite locally and confirm the helper behaves as expected without contacting DHL:

1. **Ensure Python 3.9+ is available.**
   ```bash
   python --version
   ```
   If this prints a Python version lower than 3.9, install a newer Python release before continuing.
2. **(Optional) Create and activate a virtual environment** so the tooling does not affect your global site-packages:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows PowerShell: .venv\Scripts\Activate.ps1
   ```
3. **Install the testing dependency** listed in `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```
4. **Run the tests** from the repository root:
   ```bash
   pytest
   ```
   All three mocked scenarios—successful lookup, missing shipment data, and HTTP error handling—should report `PASSED`.
5. **Deactivate the virtual environment** when you are finished (skip this if you did not activate one):
   ```bash
   deactivate
   ```
