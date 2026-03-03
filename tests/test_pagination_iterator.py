"""Tests for PaginatedIterator."""

from __future__ import annotations

import responses

from acmeeh_admin._http import HttpSession
from acmeeh_admin._pagination import PaginatedIterator

BASE = "https://acme.test"


def _http():
    return HttpSession(BASE, token="tok", verify_ssl=False, api_prefix="")


def _add_dummy_root(rsps):
    """Register a mock for the dummy GET to base_url that PaginatedIterator makes first."""
    rsps.add(responses.GET, BASE, json=[])


class TestPaginatedIterator:
    @responses.activate
    def test_single_page(self):
        _add_dummy_root(responses)
        responses.add(
            responses.GET,
            f"{BASE}/items",
            json=[{"id": 1}, {"id": 2}],
        )
        paginator = PaginatedIterator(_http(), "/items")
        items = paginator.collect()
        assert items == [{"id": 1}, {"id": 2}]

    @responses.activate
    def test_multiple_pages(self):
        _add_dummy_root(responses)
        responses.add(
            responses.GET,
            f"{BASE}/items",
            json=[{"id": 1}],
            headers={"Link": f'<{BASE}/items?cursor=abc>;rel="next"'},
        )
        responses.add(
            responses.GET,
            f"{BASE}/items?cursor=abc",
            json=[{"id": 2}],
        )
        paginator = PaginatedIterator(_http(), "/items")
        items = paginator.collect()
        assert items == [{"id": 1}, {"id": 2}]

    @responses.activate
    def test_empty_first_page(self):
        _add_dummy_root(responses)
        responses.add(
            responses.GET,
            f"{BASE}/items",
            json=[],
        )
        paginator = PaginatedIterator(_http(), "/items")
        items = paginator.collect()
        assert items == []

    @responses.activate
    def test_with_params(self):
        # The dummy GET also receives the params
        responses.add(responses.GET, BASE, json=[])
        responses.add(
            responses.GET,
            f"{BASE}/items",
            json=[{"id": 1}],
        )
        paginator = PaginatedIterator(_http(), "/items", params={"limit": 10})
        items = paginator.collect()
        assert items == [{"id": 1}]

    @responses.activate
    def test_iter_protocol(self):
        _add_dummy_root(responses)
        responses.add(
            responses.GET,
            f"{BASE}/items",
            json=[{"id": 1}],
        )
        paginator = PaginatedIterator(_http(), "/items")
        assert iter(paginator) is paginator
        page = next(paginator)
        assert page == [{"id": 1}]

    @responses.activate
    def test_three_pages(self):
        _add_dummy_root(responses)
        responses.add(
            responses.GET,
            f"{BASE}/items",
            json=[{"id": 1}],
            headers={"Link": f'<{BASE}/items?cursor=p2>;rel="next"'},
        )
        responses.add(
            responses.GET,
            f"{BASE}/items?cursor=p2",
            json=[{"id": 2}],
            headers={"Link": f'<{BASE}/items?cursor=p3>;rel="next"'},
        )
        responses.add(
            responses.GET,
            f"{BASE}/items?cursor=p3",
            json=[{"id": 3}],
        )
        paginator = PaginatedIterator(_http(), "/items")
        items = paginator.collect()
        assert len(items) == 3
        assert [i["id"] for i in items] == [1, 2, 3]
