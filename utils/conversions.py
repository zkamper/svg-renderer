def percent_to_float(value: str, compare_to: float) -> float:
    if '%' in value:
        return float(value.replace('%', '')) / 100 * compare_to
    return float(value)