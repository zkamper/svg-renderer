from common.context import MyContext
from common.styles import Styles
from common.element import Element
from utils.conversions import percent_to_float

class Line(Element):
    def __init__(self, attrib: dict):
        super().__init__('line', attrib)
        self.style = Styles(attrib)

    def get_attributes(self, ctx: MyContext):
        x1 = self.attrib.get('x1', '0')
        y1 = self.attrib.get('y1', '0')
        x1, y1 = percent_to_float(x1, ctx.width), percent_to_float(y1, ctx.height)
        x2 = self.attrib.get('x2', '0')
        y2 = self.attrib.get('y2', '0')
        x2, y2 = percent_to_float(x2, ctx.width), percent_to_float(y2, ctx.height)
        return x1, y1, x2, y2

    def draw_element(self, ctx: MyContext):
        draw_ctx = ctx.ctx
        x1, y1, x2, y2 = self.get_attributes(ctx)
        draw_ctx.set_source_rgba(*self.style.fill)
        draw_ctx.set_line_width(self.style.stroke_width)
        draw_ctx.move_to(x1, y1)
        draw_ctx.line_to(x2, y2)
        draw_ctx.set_source_rgba(*self.style.stroke[:3], 1)
        draw_ctx.stroke()