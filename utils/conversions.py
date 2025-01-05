def percent_to_float(value: str, compare_to: float) -> float:
    if '%' in value:
        return float(value.replace('%', '')) / 100 * compare_to
    return float(value)

def points_str_to_corods(points: str) -> list[tuple[float, float]]:
    """
    Converteste un string de puncte în coordinate
    :param points: string de puncte de forma 'x1 y1,x2 y2,...'
    :return: lista de tupluri de coordonate
    """
    coords = []
    for point in points.split():
        x, y = point.split(',')
        coords.append((float(x), float(y)))
    return coords

def mirrored_point(point: tuple[float, float], center: tuple[float, float]) -> tuple[float, float]:
    return 2 * center[0] - point[0], 2 * center[1] - point[1]