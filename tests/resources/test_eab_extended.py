"""Extended tests for EAB resource — identifier and profile linkage."""

from __future__ import annotations

import responses

from tests.conftest import ADMIN_PREFIX

EAB_ID = "550e8400-e29b-41d4-a716-446655440001"
IDENT_ID = "ident-001"
PROFILE_ID = "prof-001"


class TestAddIdentifier:
    @responses.activate
    def test_add_identifier(self, client):
        responses.add(
            responses.PUT,
            f"{ADMIN_PREFIX}/eab/{EAB_ID}/allowed-identifiers/{IDENT_ID}",
            status=204,
        )
        client.eab.add_identifier(EAB_ID, IDENT_ID)
        assert responses.calls[0].request.method == "PUT"


class TestRemoveIdentifier:
    @responses.activate
    def test_remove_identifier(self, client):
        responses.add(
            responses.DELETE,
            f"{ADMIN_PREFIX}/eab/{EAB_ID}/allowed-identifiers/{IDENT_ID}",
            status=204,
        )
        client.eab.remove_identifier(EAB_ID, IDENT_ID)
        assert responses.calls[0].request.method == "DELETE"


class TestListIdentifiers:
    @responses.activate
    def test_list_identifiers(self, client):
        responses.add(
            responses.GET,
            f"{ADMIN_PREFIX}/eab/{EAB_ID}/allowed-identifiers",
            json=[
                {
                    "id": IDENT_ID,
                    "identifier_type": "dns",
                    "identifier_value": "example.com",
                }
            ],
        )
        result = client.eab.list_identifiers(EAB_ID)
        assert len(result) == 1
        assert result[0]["identifier_type"] == "dns"


class TestAssignCsrProfile:
    @responses.activate
    def test_assign(self, client):
        responses.add(
            responses.PUT,
            f"{ADMIN_PREFIX}/eab/{EAB_ID}/csr-profile/{PROFILE_ID}",
            status=204,
        )
        client.eab.assign_csr_profile(EAB_ID, PROFILE_ID)
        assert responses.calls[0].request.method == "PUT"


class TestUnassignCsrProfile:
    @responses.activate
    def test_unassign(self, client):
        responses.add(
            responses.DELETE,
            f"{ADMIN_PREFIX}/eab/{EAB_ID}/csr-profile/{PROFILE_ID}",
            status=204,
        )
        client.eab.unassign_csr_profile(EAB_ID, PROFILE_ID)
        assert responses.calls[0].request.method == "DELETE"


class TestGetCsrProfile:
    @responses.activate
    def test_get(self, client):
        responses.add(
            responses.GET,
            f"{ADMIN_PREFIX}/eab/{EAB_ID}/csr-profile",
            json={"id": PROFILE_ID, "name": "default"},
        )
        result = client.eab.get_csr_profile(EAB_ID)
        assert result["id"] == PROFILE_ID
