from common.context import MyContext
from common.styles import Styles
from common.element import Element
from utils.path import gen_path, clean_path


class Path(Element):
    """
    Element de tip <path>
    """
    def __init__(self, attrib: dict):
        super().__init__('path', attrib)
        self.style = Styles(attrib)
        self.path_nodes = []

    def get_attributes(self):
        d = self.attrib.get('d','')
        if d == '':
            return []
        path = clean_path(d)
        path_nodes = gen_path(path)
        return path_nodes

    def draw_element(self, ctx: MyContext):
        draw_ctx = ctx.ctx
        path_nodes = self.get_attributes()
        draw_ctx.set_source_rgba(*self.style.fill)
        draw_ctx.set_line_width(self.style.stroke_width)
        prev_control_x, prev_control_y = draw_ctx.get_current_point()

        for node in path_nodes:
            if prev_control_x is not None:
                node.set_prev_control_point(prev_control_x, prev_control_y) # salveaza punctul de control anterior în caz ca este necesar
            prev_control_x, prev_control_y = None, None

            prev_control = node.draw_path(draw_ctx)
            if prev_control is not None:
                prev_control_x, prev_control_y = prev_control

        draw_ctx.set_source_rgba(*self.style.fill)
        draw_ctx.fill_preserve()
        draw_ctx.set_source_rgba(*self.style.stroke)
        draw_ctx.stroke()