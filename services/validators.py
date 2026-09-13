ALLOWED_SORT_COLUMNS = ("name", "created_at", "status")


def normalize_column(col: str) -> str:
    """Whitelist the ORDER BY column; it cannot be parameterized."""
    if col not in ALLOWED_SORT_COLUMNS:
        raise ValueError("invalid sort column")
    return col
