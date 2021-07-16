"""
Misc. utilities.
"""


def list_alloc(rows: int, columns: int):
    return [[None for _ in range(columns)] for _ in range(rows)]
