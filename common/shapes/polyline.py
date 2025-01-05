from common.context import MyContext
from common.styles import Styles
from common.element import Element
from utils.conversions import points_str_to_corods


class Polyline(Element):
    """
    Element de tip <polyline>
    """
    def __init__(self, attrib: dict):
        super().__init__('polyline', attrib)
        self.style = Styles(attrib)

    def get_attributes(self):
        """
        Returnează coordonatele punctelor
        :return:
        """
        points = self.attrib.get('points', '')
        coords = points_str_to_corods(points)
        return coords

    def draw_element(self, ctx: MyContext):
        draw_ctx = ctx.ctx
        coords = self.get_attributes()

        draw_ctx.set_line_width(self.style.stroke_width)
        draw_ctx.move_to(*coords[0])

        for coord in coords[1:]:
            draw_ctx.line_to(*coord)

        draw_ctx.set_source_rgba(*self.style.fill)
        draw_ctx.fill_preserve()
        draw_ctx.set_source_rgba(*self.style.stroke[:3], 1)
        draw_ctx.stroke()