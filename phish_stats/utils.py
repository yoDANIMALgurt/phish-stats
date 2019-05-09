"""Utility functions."""

import json


def generate_query_string(query_params):
    """Generate a query string given kwargs dictionary."""
    query_frags = [str(key) + "=" + str(value)
                   for key, value in query_params.items()]

    query_str = "&".join(query_frags)

    return query_str
