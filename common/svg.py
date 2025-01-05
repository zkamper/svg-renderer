from common.context import MyContext
from common.element import Element
import cairo

class SVG(Element):
    """
    Clasa de bază pentru un element SVG.

    Rădăcina pentru un SVG, conține atribute precum dimensiunea, viewbox-ul
    și o listă de copii.
    Copiii sunt forme geometrice primitive (cerc, rect, path, etc.)

    :param attrib: atributele elementului
    :param children: lista de copii ai elementului
    :param name: numele fișierului de ieșire
    """
    def __init__(self, attrib: dict, children: list[Element], name: str):
        super().__init__('svg', attrib)
        self.name = name.rsplit('.', 1)[0] + '.png'

        if 'width' not in attrib or 'height' not in attrib:
            raise ValueError('attribute \'width\' or \'height\' not found')
        self.width = int(attrib['width'].replace('px', ''))
        self.height = int(attrib['height'].replace('px', ''))

        if 'viewBox' in attrib:
            self.viewBox = attrib['viewBox']
            self.width = int(self.viewBox.split(' ')[2])
            self.height = int(self.viewBox.split(' ')[3])

        self.surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, self.width, self.height)
        self.ctx = MyContext(cairo.Context(self.surface), self.width, self.height)

        for child in children:
            self.add_child(child)

    def draw(self):
        """
        Desenează toți copii elementului SVG în ordinea în care apar în arbore.
        La final salvează imaginea în PNG
        :return:
        """
        for child in self.children:
            child.draw_element(self.ctx)
        self.surface.write_to_png(self.name)