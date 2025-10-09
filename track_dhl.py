"""Command-line tool to retrieve DHL shipment status using the public tracking API."""
from __future__ import annotations

import json
import os
import sys
from typing import Any, Dict
from urllib import error, parse, request


API_URL = "https://api-eu.dhl.com/track/shipments"


def fetch_shipment_status(tracking_number: str, api_key: str) -> str:
    """Retrieve the shipment status description for a DHL tracking number.

    Args:
        tracking_number: The DHL tracking number to look up.
        api_key: DHL API key used for authentication.

    Returns:
        A human readable shipment status description.

    Raises:
        ValueError: If the tracking number is empty or the response is missing
            the expected data.
        error.HTTPError: If the HTTP request to DHL fails.
    """

    if not tracking_number:
        raise ValueError("Tracking number must not be empty.")

    if not api_key:
        raise ValueError("DHL API key must not be empty.")

    query = parse.urlencode({"trackingNumber": tracking_number})
    http_request = request.Request(
        url=f"{API_URL}?{query}",
        headers={
            "DHL-API-Key": api_key,
        },
        method="GET",
    )

    with request.urlopen(http_request, timeout=10) as response:
        payload: Dict[str, Any] = json.load(response)

    shipments = payload.get("shipments")
    if not shipments:
        raise ValueError("No shipment information returned for the provided tracking number.")

    shipment = shipments[0]
    status_info = shipment.get("status") if isinstance(shipment, dict) else None
    if not status_info:
        raise ValueError("Shipment status information is unavailable.")

    description = (
        status_info.get("description")
        or status_info.get("status")
        or status_info.get("statusCode")
    )
    if not description:
        raise ValueError("Shipment status description is missing from the API response.")

    return str(description)


def main() -> int:
    api_key = os.getenv("DHL_API_KEY")

    if not api_key:
        print(
            "Environment variable DHL_API_KEY must be set. "
            "Please export your DHL Shipment Tracking – Unified API key before running this script.",
            file=sys.stderr,
        )
        return 1

    try:
        tracking_number = input("Enter DHL tracking number: ").strip()
    except EOFError:
        print("No tracking number provided.", file=sys.stderr)
        return 1

    if not tracking_number:
        print("Tracking number cannot be empty.", file=sys.stderr)
        return 1

    try:
        status = fetch_shipment_status(tracking_number, api_key)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    except error.HTTPError as exc:
        print(
            "Failed to retrieve shipment status from DHL: "
            f"{exc.code} {exc.reason}",
            file=sys.stderr,
        )
        return 1
    except error.URLError as exc:
        print(f"A network error occurred: {exc.reason}", file=sys.stderr)
        return 1

    print(f"Shipment status: {status}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
