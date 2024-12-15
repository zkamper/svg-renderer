import cairo

from common.context import MyContext
from common.styles import Styles
from common.element import Element
from utils.conversions import percent_to_float

def draw_rounded_rectangle(context: cairo.Context, x: float, y: float, width: float, height: float, rx: float, ry: float):
    context.move_to(x + rx, y)

    context.line_to(x + width - rx, y)
    context.curve_to(x + width - rx / 2, y, x + width, y + ry / 2, x + width, y + ry)

    context.line_to(x + width, y + height - ry)
    context.curve_to(x + width, y + height - ry / 2, x + width - rx / 2, y + height, x + width - rx, y + height)

    context.line_to(x + rx, y + height)
    context.curve_to(x + rx / 2, y + height, x, y + height - ry / 2, x, y + height - ry)

    context.line_to(x, y + ry)
    context.curve_to(x, y + ry / 2, x + rx / 2, y, x + rx, y)

    context.close_path()


class Rect(Element):
    def __init__(self, attrib: dict):
        super().__init__('rect', attrib)
        self.style = Styles(attrib)

    def get_attributes(self, ctx: MyContext):
        x = self.attrib.get('x', '0')
        y = self.attrib.get('y', '0')
        x, y = percent_to_float(x, ctx.width), percent_to_float(y, ctx.height)
        width = self.attrib.get('width', '0')
        height = self.attrib.get('height', '0')
        width, height = percent_to_float(width, ctx.width), percent_to_float(height, ctx.height)
        rx = self.attrib.get('rx', '0')
        ry = self.attrib.get('ry', rx)
        rx, ry = percent_to_float(rx, x), percent_to_float(ry, y)
        return x, y, width, height, rx, ry

    def draw_element(self, ctx: MyContext):
        draw_ctx = ctx.ctx
        x, y, width, height, rx, ry = self.get_attributes(ctx)
        draw_ctx.set_source_rgb(*self.style.fill)
        draw_ctx.set_line_width(self.style.stroke_width)
        if rx == 0 and ry == 0:
            draw_ctx.rectangle(x, y, width, height)
        else:
            draw_rounded_rectangle(draw_ctx, x, y, width, height, rx, ry)
        draw_ctx.fill_preserve()
        draw_ctx.set_source_rgba(*self.style.stroke)
        if self.style.stroke_width != -1:
            draw_ctx.stroke()