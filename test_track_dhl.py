from __future__ import annotations

import io
import json
from typing import Any, Dict
from unittest import mock

import pytest
from urllib import error

from track_dhl import API_URL, fetch_shipment_status


class FakeHTTPResponse(io.BytesIO):
    def __init__(self, data: Dict[str, Any]):
        payload = json.dumps(data).encode("utf-8")
        super().__init__(payload)

    def __enter__(self):
        return self

    def __exit__(self, *exc_info):
        self.close()
        return False


def _assert_tracking_request(call_args, expected_tracking_number: str):
    (req,), _ = call_args
    assert req.full_url.startswith(API_URL)
    assert f"trackingNumber={expected_tracking_number}" in req.full_url
    assert "service=express" in req.full_url
    headers = {key.lower(): value for key, value in req.header_items()}
    assert headers.get("dhl-api-key") == "test-key"
    assert headers.get("accept") == "application/json"
    assert headers.get("accept-language") == "en-US"
    assert headers.get("user-agent") == "dhl-tracker-cli/1.0"


def test_fetch_shipment_status_success():
    response = FakeHTTPResponse(
        {"shipments": [{"status": {"description": "Delivered"}}]}
    )

    with mock.patch("track_dhl.request.urlopen", return_value=response) as mocked_urlopen:
        status = fetch_shipment_status("1234567890", "test-key")

    assert status == "Delivered"
    _assert_tracking_request(mocked_urlopen.call_args, "1234567890")


def test_fetch_shipment_status_missing_data():
    response = FakeHTTPResponse({"shipments": []})

    with mock.patch("track_dhl.request.urlopen", return_value=response):
        with pytest.raises(ValueError) as exc_info:
            fetch_shipment_status("1234567890", "test-key")

    assert "No shipment information" in str(exc_info.value)


def test_fetch_shipment_status_http_error():
    http_error = error.HTTPError(
        url=f"{API_URL}?trackingNumber=1234567890",
        code=404,
        msg="Not Found",
        hdrs=None,
        fp=None,
    )

    with mock.patch("track_dhl.request.urlopen", side_effect=http_error):
        with pytest.raises(error.HTTPError):
            fetch_shipment_status("1234567890", "test-key")
