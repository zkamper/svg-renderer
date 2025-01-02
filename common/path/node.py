import cairo


class Node:
    def __init__(self, relative):
        self.relative = relative

    def draw_path(self, ctx: cairo.Context):
        pass

class Move(Node):
    def __init__(self, x, y, relative):
        super().__init__(relative)
        self.x = x
        self.y = y

class Line(Node):
    def __init__(self, x, y, relative):
        super().__init__(relative)
        self.x = x
        self.y = y

class VLine(Node):
    def __init__(self, y, relative):
        super().__init__(relative)
        self.y = y

class HLine(Node):
    def __init__(self, x, relative):
        super().__init__(relative)
        self.x = x

class Z(Node):
    def __init__(self, x, y, relative):
        super().__init__(relative)
        self.x = x
        self.y = y

class CubicBezier(Node):
    def __init__(self, x1, y1, x2, y2, x, y, relative):
        super().__init__(relative)
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.x = x
        self.y = y

class SmoothCubicBezier(Node):
    def __init__(self, x2, y2, x, y, relative):
        super().__init__(relative)
        self.x2 = x2
        self.y2 = y2
        self.x = x
        self.y = y

class QuadraticBezier(Node):
    def __init__(self, x1, y1, x, y, relative):
        super().__init__(relative)
        self.x1 = x1
        self.y1 = y1
        self.x = x
        self.y = y

class SmoothQuadraticBezier(Node):
    def __init__(self, x, y, relative):
        super().__init__(relative)
        self.x = x
        self.y = y

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






