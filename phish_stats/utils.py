"""Utility functions."""

import json


def generate_query_string(**kwargs):
    """Generate a query string given kwargs dictionary."""

    query_frags = [str(key) + "=" + str(value) for key, value in kwargs.items()]

    query_str = "&".join(query_frags)

    return query_str
