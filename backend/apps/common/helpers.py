"""
Common helper functions
"""


def format_number(value, decimals=2):
    """Format number for display"""
    if value is None:
        return None
    return round(value, decimals)


def format_currency(value):
    """Format as currency"""
    if value is None:
        return None
    return f"₹{value:,.0f}"
