from cairo import Context

class Element:
    def __init__(self, tag: str, attrib: dict):
        self.tag = tag
        self.attrib = attrib
        self.children = []

    def add_child(self, child: 'Element'):
        self.children.append(child)

    def draw_element(self, ctx: Context):
        for child in self.children:
            child.draw_element(ctx)

    def print_tree(self):
        print(self.tag, self.attrib)
        for child in self.children:
            child.print_tree()