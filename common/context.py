import cairo


class MyContext:
    """
    Clasă pentru a reține contextul curent + dimensiunile imaginii

    Dimensiunile sunt necesare pentru a putea face calcule relative (de ex `x=15%`).
    :param ctx: contextul cairo
    :param width: lățimea imaginii
    :param height: înălțimea imaginii
    """
    def __init__(self, ctx: cairo.Context, width: int, height: int):
        self.ctx = ctx
        self.width = width
        self.height = height