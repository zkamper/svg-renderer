import math

import cairo
from utils.conversions import mirrored_point

class Command:
    """
    Clasă de bază pentru o comandă dintr-un path.

    Fiecare comandă are asociată o literă care indică tipul. Literele mari sunt pentru coordonate absolute, iar cele
    mici pentru coordonate relative la poziția cursorului.
    Comenzile acceptate sunt la https://developer.mozilla.org/en-US/docs/Web/SVG/Tutorial/Paths

    :param x: coordonata x destinație
    :param y: coordonata y destinație
    """
    def __init__(self, x, y, relative):
        self.relative = relative
        self.x = x
        self.y = y
        self.prev_control_x = 0
        self.prev_control_y = 0

    def draw_path(self, ctx: cairo.Context):
        """
        Desenează comanda curentă în contextul dat.

        Unele comenzi au nevoie de punctul de control anterior, de aceea comanda poate returna:
        coordonatele punctului de control precedent
        sau coordonatele unde s-a terminat ultima comandă
        :param ctx: contextul de desenare
        :return:
        """
        pass

    def set_prev_control_point(self, x, y):
        """
        Setează punctul de control precedent.

        Este necesar pentru comenzile chained de tipul `S` sau `T`, care folosesc ultimul punct de control pentru
        a genera punctul de control implicit.
        :param x: coordonata x a punctului de control precedent
        :param y: coordonata y a punctului de control precedent
        :return:
        """
        self.prev_control_x = x
        self.prev_control_y = y

class Move(Command):
    """
    "Move To" - mută cursorul la coordonatele specificate
    `M x y` sau `m dx dy`
    """
    def __init__(self, x, y, relative):
        super().__init__(x, y, relative)

    def draw_path(self, ctx: cairo.Context):
        if self.relative:
            ctx.rel_move_to(self.x, self.y)
        else:
            ctx.move_to(self.x, self.y)
        return ctx.get_current_point()

class Line(Command):
    """
    "Line To" - trasează o linie la coordonatele specificate
    `L x y` sau `l dx dy`
    """
    def __init__(self, x, y, relative):
        super().__init__(x, y, relative)

    def draw_path(self, ctx: cairo.Context):
        if self.relative:
            ctx.rel_line_to(self.x, self.y)
        else:
            ctx.line_to(self.x, self.y)
        return ctx.get_current_point()

class VLine(Command):
    """
    "Vertical Line To" - trasează o linie verticală la coordonata specificată
    `V y` sau `v dy`
    """
    def __init__(self, y, relative):
        super().__init__(0, y, relative)

    def draw_path(self, ctx: cairo.Context):
        if self.relative:
            ctx.rel_line_to(0, self.y)
        else:
            curr_x, _ = ctx.get_current_point()
            ctx.line_to(curr_x, self.y)
        return ctx.get_current_point()

class HLine(Command):
    """
    "Horizontal Line To" - trasează o linie orizontală la coordonata specificată
    `H x` sau `h dx`
    """
    def __init__(self, x, relative):
        super().__init__(x, 0, relative)

    def draw_path(self, ctx: cairo.Context):
        if self.relative:
            ctx.rel_line_to(self.x, 0)
        else:
            _, curr_y = ctx.get_current_point()
            ctx.line_to(self.x, curr_y)
        return ctx.get_current_point()

class Z(Command):
    """
    "Close Path" - închide path-ul curent
    trasează o linie către primul punct din path
    """
    def __init__(self, relative):
        super().__init__(0, 0, relative)

    def draw_path(self, ctx: cairo.Context):
        ctx.close_path()
        return ctx.get_current_point()

class CubicBezier(Command):
    """
    "Cubic Bezier Curve" - trasează o curbă bezier cubică la coordonatele specificate
    `C x1 y1, x2 y2, x y` sau `c dx1 dy1, dx2 dy2, dx dy`
    :param x1: coordonata x a primului punct de control
    :param y1: coordonata y a primului punct de control
    :param x2: coordonata x a celui de-al doilea punct de control
    :param y2: coordonata y a celui de-al doilea punct de control
    """
    def __init__(self, x1, y1, x2, y2, x, y, relative):
        super().__init__(x, y, relative)
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def draw_path(self, ctx: cairo.Context):
        if self.relative:
            x, y = ctx.get_current_point()
            ctx.rel_curve_to(self.x1, self.y1, self.x2, self.y2, self.x, self.y)
            return x + self.x2, y + self.y2
        else:
            ctx.curve_to(self.x1, self.y1, self.x2, self.y2, self.x, self.y)
            return self.x2, self.y2

class SmoothCubicBezier(Command):
    """
    "Smooth Cubic Bezier Curve" - trasează o curbă bezier cubică la coordonatele specificate
    `S x2 y2, x y` sau `s dx2 dy2, dx dy`

    Se folosește ultimul punct de control pentru a genera punctul de control implicit.
    :param x2: coordonata x a celui de-al doilea punct de control
    :param y2: coordonata y a celui de-al doilea punct de
    """
    def __init__(self, x2, y2, x, y, relative):
        super().__init__(x, y, relative)
        self.x2 = x2
        self.y2 = y2

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

class QuadraticBezier(Command):
    """
    "Quadratic Bezier Curve" - trasează o curbă bezier pătratică la coordonatele specificate

    Spre deosebire de Cubic Bezier, punctul de control este același pentru start și finish.
    `Q x1 y1, x y` sau `q dx1 dy1, dx dy`
    :param x1: coordonata x a punctului de control
    :param y1: coordonata y a punctului de control
    """
    def __init__(self, x1, y1, x, y, relative):
        super().__init__(x, y, relative)
        self.x1 = x1
        self.y1 = y1

    def draw_path(self, ctx: cairo.Context):
        if self.relative:
            x, y = ctx.get_current_point()
            ctx.rel_curve_to(self.x1, self.y1, self.x1, self.y1, self.x, self.y)
            return x + self.x1, y + self.y1
        else:
            ctx.curve_to(self.x1, self.y1, self.x1, self.y1, self.x, self.y)
            return self.x1, self.y1

class SmoothQuadraticBezier(Command):
    """
    "Smooth Quadratic Bezier Curve" - trasează o curbă bezier pătratică la coordonatele specificate

    Se folosește ultimul punct de control pentru a genera punctul de control implicit.
    `T x y` sau `t dx dy`
    """
    def __init__(self, x, y, relative):
        super().__init__(x, y, relative)

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


class Arc(Command):
    """
    "Arc" - secțiune de elipsă sau cerc

    Pentru 2 puncte există 4 arcuri care le conectează, fiind necesari mai mulți parametrii pentru a desemna curbele
    :param rx: raza pe axa x
    :param ry: raza pe axa y
    :param x_axis_rotation: unghiul de rotație al axei x
    :param large_arc_flag: 1 dacă arcul este mai mare de 180 de grade
    :param sweep_flag: 1 dacă arcul este desenat în sensul acelor de ceasornic
    """
    def __init__(self, rx, ry, x_axis_rotation, large_arc_flag, sweep_flag, x, y, relative):
        super().__init__(x, y, relative)
        self.rx = rx
        self.ry = ry
        self.x_axis_rotation = x_axis_rotation
        self.large_arc_flag = large_arc_flag
        self.sweep_flag = sweep_flag

    def draw_path(self, ctx: cairo.Context):
        x_axis_rot = math.radians(self.x_axis_rotation)

        curr_x, curr_y = ctx.get_current_point()
        if self.relative:
            x = curr_x + self.x
            y = curr_y + self.y
        else:
            x = self.x
            y = self.y

        # https://www.w3.org/TR/SVG/implnote.html#ArcImplementationNotes
        dx2 = (curr_x - x) / 2
        dy2 = (curr_y - y) / 2

        x1 = math.cos(x_axis_rot) * dx2 + math.sin(x_axis_rot) * dy2
        y1 = -math.sin(x_axis_rot) * dx2 + math.cos(x_axis_rot) * dy2

        radius_scale = math.sqrt(
            max(0, (self.rx ** 2 * self.ry ** 2 - self.rx ** 2 * y1 ** 2 - self.ry ** 2 * x1 ** 2) /
                (self.rx ** 2 * y1 ** 2 + self.ry ** 2 * x1 ** 2))
        )

        if self.large_arc_flag == self.sweep_flag:
            radius_scale = -radius_scale

        cx1 = radius_scale * self.rx * y1 / self.ry
        cy1 = -radius_scale * self.ry * x1 / self.rx

        cx = math.cos(x_axis_rot) * cx1 - math.sin(x_axis_rot) * cy1 + (curr_x + x) / 2
        cy = math.sin(x_axis_rot) * cx1 + math.cos(x_axis_rot) * cy1 + (curr_y + y) / 2

        theta1 = math.atan2((y1 - cy1) / self.ry, (x1 - cx1) / self.rx)
        theta2 = math.atan2((-y1 - cy1) / self.ry, (-x1 - cx1) / self.rx)

        if self.sweep_flag == 0 and theta2 > theta1:
            theta2 -= 2 * math.pi
        elif self.sweep_flag == 1 and theta2 < theta1:
            theta2 += 2 * math.pi

        ctx.save()
        ctx.translate(cx, cy)
        ctx.rotate(x_axis_rot)
        ctx.scale(self.rx, self.ry)
        if self.sweep_flag:
            ctx.arc(0, 0, 1, theta1, theta2)
        else:
            ctx.arc_negative(0, 0, 1, theta1, theta2)
        ctx.restore()
        return x, y