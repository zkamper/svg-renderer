import cairo
from cairo import Context

from common.context import MyContext
from common.styles import Styles
from common.element import Element
from utils.conversions import percent_to_float

class Ellipse(Element):
    def __init__(self, attrib: dict):
        super().__init__('ellipse', attrib)
        self.style = Styles(attrib)

    def get_attributes(self, ctx: MyContext):
        cx = self.attrib.get('cx', '0')
        cy = self.attrib.get('cy', '0')
        rx = self.attrib.get('rx', '0')
        ry = self.attrib.get('ry', '0')
        return percent_to_float(cx, ctx.width), percent_to_float(cy, ctx.height), percent_to_float(rx, ctx.width), percent_to_float(ry, ctx.height)

    def draw_element(self, ctx: MyContext):
        draw_ctx = ctx.ctx
        x, y, rx, ry = self.get_attributes(ctx)
        draw_ctx.set_source_rgb(*self.style.fill)
        draw_ctx.set_line_width(self.style.stroke_width)
        draw_ctx.save()
        draw_ctx.translate(x, y)
        draw_ctx.scale(1, ry / rx)
        draw_ctx.arc(0, 0, rx, 0, 2 * 3.141592)
        draw_ctx.restore()
        draw_ctx.fill_preserve()
        draw_ctx.set_source_rgba(*self.style.stroke)
        if self.style.stroke_width != -1:
            draw_ctx.stroke()