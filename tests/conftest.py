"""Shared test fixtures."""

from __future__ import annotations

import pytest
import responses

from acmeeh_admin import AcmeehAdminClient

BASE_URL = "https://acme.test"
ADMIN_PREFIX = f"{BASE_URL}/api"
TOKEN = "test-token-123"


@pytest.fixture
def mocked_responses():
    """Activate the responses mock for the test."""
    with responses.RequestsMock() as rsps:
        yield rsps


@pytest.fixture
def client():
    """Return a client configured with a test token."""
    return AcmeehAdminClient(BASE_URL, token=TOKEN, verify_ssl=False)
