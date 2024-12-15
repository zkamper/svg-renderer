import cairo
from cairo import Context

from common.context import MyContext
from common.styles import Styles
from common.element import Element
from utils.conversions import percent_to_float

class Circle(Element):
    def __init__(self, attrib: dict):
        super().__init__('circle', attrib)
        self.style = Styles(attrib)

    def get_attributes(self, ctx: MyContext):
        cx = self.attrib.get('cx', '0')
        cy = self.attrib.get('cy', '0')
        r = self.attrib.get('r', '0')
        return percent_to_float(cx, ctx.width), percent_to_float(cy, ctx.height), percent_to_float(r, ctx.width)

    def draw_element(self, ctx: MyContext):
        draw_ctx = ctx.ctx
        x, y, r = self.get_attributes(ctx)
        draw_ctx.set_source_rgba(*self.style.fill)
        draw_ctx.set_line_width(self.style.stroke_width)
        draw_ctx.arc(x, y, r, 0, 2 * 3.141592)
        draw_ctx.fill_preserve()
        draw_ctx.set_source_rgba(*self.style.stroke)
        draw_ctx.stroke()
