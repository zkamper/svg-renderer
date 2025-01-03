import cairo
from utils.conversions import mirrored_point

class Node:
    def __init__(self, relative):
        self.relative = relative
        self.prev_control_x = 0
        self.prev_control_y = 0

    def draw_path(self, ctx: cairo.Context):
        pass

    def set_prev_control_point(self, x, y):
        self.prev_control_x = x
        self.prev_control_y = y

class Move(Node):
    def __init__(self, x, y, relative):
        super().__init__(relative)
        self.x = x
        self.y = y

    def draw_path(self, ctx: cairo.Context):
        if self.relative:
            ctx.rel_move_to(self.x, self.y)
        else:
            ctx.move_to(self.x, self.y)
        return ctx.get_current_point()

class Line(Node):
    def __init__(self, x, y, relative):
        super().__init__(relative)
        self.x = x
        self.y = y

    def draw_path(self, ctx: cairo.Context):
        if self.relative:
            ctx.rel_line_to(self.x, self.y)
        else:
            ctx.line_to(self.x, self.y)
        return ctx.get_current_point()

class VLine(Node):
    def __init__(self, y, relative):
        super().__init__(relative)
        self.y = y

    def draw_path(self, ctx: cairo.Context):
        if self.relative:
            ctx.rel_line_to(0, self.y)
        else:
            curr_x, _ = ctx.get_current_point()
            ctx.line_to(curr_x, self.y)
        return ctx.get_current_point()

class HLine(Node):
    def __init__(self, x, relative):
        super().__init__(relative)
        self.x = x

    def draw_path(self, ctx: cairo.Context):
        if self.relative:
            ctx.rel_line_to(self.x, 0)
        else:
            _, curr_y = ctx.get_current_point()
            ctx.line_to(self.x, curr_y)
        return ctx.get_current_point()

class Z(Node):
    def __init__(self, x, y, relative):
        super().__init__(relative)
        self.x = x
        self.y = y

    def draw_path(self, ctx: cairo.Context):
        ctx.close_path()
        return ctx.get_current_point()

class CubicBezier(Node):
    def __init__(self, x1, y1, x2, y2, x, y, relative):
        super().__init__(relative)
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.x = x
        self.y = y

    def draw_path(self, ctx: cairo.Context):
        if self.relative:
            ctx.rel_curve_to(self.x1, self.y1, self.x2, self.y2, self.x, self.y)
            x, y = ctx.get_current_point()
            return x + self.x2, y + self.y2
        else:
            ctx.curve_to(self.x1, self.y1, self.x2, self.y2, self.x, self.y)
            return self.x2, self.y2

class SmoothCubicBezier(Node):
    def __init__(self, x2, y2, x, y, relative):
        super().__init__(relative)
        self.x2 = x2
        self.y2 = y2
        self.x = x
        self.y = y

    def draw_path(self, ctx: cairo.Context):
        new_control_x, new_control_y = mirrored_point((self.prev_control_x, self.prev_control_y), ctx.get_current_point())
        if self.relative:
            x, y = ctx.get_current_point()
            x1 = new_control_x - x
            y1 = new_control_y - y
            ctx.rel_curve_to(x1, y1, self.x2, self.y2, self.x, self.y)
            return x + self.x2, y + self.y2
        else:
            ctx.curve_to(new_control_x,new_control_y, self.x2, self.y2, self.x, self.y)
            return self.x2, self.y2

class QuadraticBezier(Node):
    def __init__(self, x1, y1, x, y, relative):
        super().__init__(relative)
        self.x1 = x1
        self.y1 = y1
        self.x = x
        self.y = y

    def draw_path(self, ctx: cairo.Context):
        if self.relative:
            ctx.rel_curve_to(self.x1, self.y1, self.x1, self.y1, self.x, self.y)
            x, y = ctx.get_current_point()
            return x + self.x1, y + self.y1
        else:
            ctx.curve_to(self.x1, self.y1, self.x1, self.y1, self.x, self.y)
            return self.x1, self.y1

class SmoothQuadraticBezier(Node):
    def __init__(self, x, y, relative):
        super().__init__(relative)
        self.x = x
        self.y = y

    def draw_path(self, ctx: cairo.Context):
        new_control_x, new_control_y = mirrored_point((self.prev_control_x, self.prev_control_y), ctx.get_current_point())
        if self.relative:
            x, y = ctx.get_current_point()
            x1 = new_control_x - x
            y1 = new_control_y - y
            ctx.rel_curve_to(x1, y1, x1, y1, self.x, self.y)
        else:
            ctx.curve_to(new_control_x,new_control_y, new_control_x, new_control_y, self.x, self.y)
        return new_control_x, new_control_y


class Arc(Node):
    def __init__(self, rx, ry, x_axis_rotation, large_arc_flag, sweep_flag, x, y, relative):
        super().__init__(relative)
        self.rx = rx
        self.ry = ry
        self.x_axis_rotation = x_axis_rotation
        self.large_arc_flag = large_arc_flag
        self.sweep_flag = sweep_flag
        self.x = x
        self.y = y