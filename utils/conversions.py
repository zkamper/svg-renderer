def percent_to_float(value: str, compare_to: float) -> float:
    if '%' in value:
        return float(value.replace('%', '')) / 100 * compare_to
    return float(value)

def points_str_to_corods(points: str) -> list[tuple[float, float]]:
    coords = []
    for point in points.split():
        x, y = point.split(',')
        coords.append((float(x), float(y)))
    return coords

def mirrored_point(point: tuple[float, float], center: tuple[float, float]) -> tuple[float, float]:
    return 2 * center[0] - point[0], 2 * center[1] - point[1]