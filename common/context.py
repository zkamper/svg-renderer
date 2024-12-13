import cairo


class MyContext:
    def __init__(self, ctx: cairo.Context, width: int, height: int):
        self.ctx = ctx
        self.width = width
        self.height = height