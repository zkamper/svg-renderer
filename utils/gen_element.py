from common.shapes.circle import Circle
from common.element import Element
from common.shapes.ellipse import Ellipse
from common.shapes.line import Line
from common.shapes.path import Path
from common.shapes.polyline import Polyline
from common.shapes.rect import Rect


def gen_element(tag: str, attrib: dict) -> 'Element':
    element = Element(tag, attrib)
    if 'rect' in tag:
        element = Rect(attrib)
    elif 'circle' in tag:
        element = Circle(attrib)
    elif 'ellipse' in tag:
        element = Ellipse(attrib)
    elif 'polyline' in tag:
        element = Polyline(attrib)
    elif 'line' in tag:
        element = Line(attrib)
    elif 'path' in tag:
        element = Path(attrib)
    return element