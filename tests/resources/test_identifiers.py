"""Tests for identifiers resource."""

from __future__ import annotations

import responses

from tests.conftest import ADMIN_PREFIX

IDENT = {
    "id": "550e8400-e29b-41d4-a716-446655440002",
    "type": "dns",
    "value": "example.com",
    "account_ids": [],
}


class TestListIdentifiers:
    @responses.activate
    def test_list(self, client):
        responses.add(
            responses.GET,
            f"{ADMIN_PREFIX}/allowed-identifiers",
            json=[IDENT],
        )
        result = client.identifiers.list()
        assert len(result) == 1


class TestCreateIdentifier:
    @responses.activate
    def test_create(self, client):
        responses.add(
            responses.POST,
            f"{ADMIN_PREFIX}/allowed-identifiers",
            json=IDENT,
            status=201,
        )
        result = client.identifiers.create("dns", "example.com")
        assert result["value"] == "example.com"


class TestGetIdentifier:
    @responses.activate
    def test_get(self, client):
        iid = IDENT["id"]
        responses.add(
            responses.GET,
            f"{ADMIN_PREFIX}/allowed-identifiers/{iid}",
            json=IDENT,
        )
        result = client.identifiers.get(iid)
        assert result["type"] == "dns"


class TestDeleteIdentifier:
    @responses.activate
    def test_delete(self, client):
        iid = IDENT["id"]
        responses.add(
            responses.DELETE,
            f"{ADMIN_PREFIX}/allowed-identifiers/{iid}",
            status=204,
        )
        client.identifiers.delete(iid)


class TestAddAccount:
    @responses.activate
    def test_add(self, client):
        iid = IDENT["id"]
        aid = "550e8400-e29b-41d4-a716-446655440099"
        responses.add(
            responses.PUT,
            f"{ADMIN_PREFIX}/allowed-identifiers/{iid}/accounts/{aid}",
            status=204,
        )
        client.identifiers.add_account(iid, aid)


class TestRemoveAccount:
    @responses.activate
    def test_remove(self, client):
        iid = IDENT["id"]
        aid = "550e8400-e29b-41d4-a716-446655440099"
        responses.add(
            responses.DELETE,
            f"{ADMIN_PREFIX}/allowed-identifiers/{iid}/accounts/{aid}",
            status=204,
        )
        client.identifiers.remove_account(iid, aid)


class TestListForAccount:
    @responses.activate
    def test_list_for_account(self, client):
        aid = "550e8400-e29b-41d4-a716-446655440099"
        responses.add(
            responses.GET,
            f"{ADMIN_PREFIX}/accounts/{aid}/allowed-identifiers",
            json=[IDENT],
        )
        result = client.identifiers.list_for_account(aid)
        assert len(result) == 1
