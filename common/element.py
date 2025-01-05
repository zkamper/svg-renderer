from cairo import Context

class Element:
    """
    Clasa de bază pentru un nod din arborele de elemente SVG.
    """
    def __init__(self, tag: str, attrib: dict):
        self.tag = tag
        self.attrib = attrib
        self.children = []

    def add_child(self, child: 'Element'):
        """
        Adaugă un copil la nodul curent
        :param child: nod copil
        :return:
        """
        self.children.append(child)

    def draw_element(self, ctx: Context):
        """
        Desenează elementul curent și toți copiii săi în ordinea în care apar în arbore.
        :param ctx: contextul de desenare
        :return:
        """
        for child in self.children:
            child.draw_element(ctx)

    def print_tree(self):
        """
        Afișează arborele de elemente SVG
        :return:
        """
        print(self.tag, self.attrib)
        for child in self.children:
            child.print_tree()