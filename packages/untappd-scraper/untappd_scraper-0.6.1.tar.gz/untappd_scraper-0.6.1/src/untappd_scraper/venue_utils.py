"""Utilities for Untappd Venue processing."""
from __future__ import annotations


def url_of(venue_id: int) -> str:
    """Return the URL for a venue's main page.

    Args:
        venue_id (int): venue ID

    Returns:
        str: url to load to get venue's main page
    """
    return f"https://untappd.com/venue/{venue_id}"
