"""Tests for pagination helpers."""

from __future__ import annotations

from acmeeh_admin._pagination import parse_link_next


class TestParseLinkNext:
    def test_extracts_next_url(self):
        header = '<https://acme.test/admin/audit-log?cursor=abc&limit=50>;rel="next"'
        assert (
            parse_link_next(header)
            == "https://acme.test/admin/audit-log?cursor=abc&limit=50"
        )

    def test_returns_none_for_no_next(self):
        header = '<https://acme.test/prev>;rel="prev"'
        assert parse_link_next(header) is None

    def test_returns_none_for_empty(self):
        assert parse_link_next(None) is None
        assert parse_link_next("") is None

    def test_handles_spaces_in_rel(self):
        header = '<https://acme.test/next>; rel="next"'
        assert parse_link_next(header) == "https://acme.test/next"
