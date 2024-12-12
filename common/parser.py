from lxml import etree as et

from common.element import Element
from common.svg import SVG


TEST_PATH = '../test.svg'


def create_element(tag: str, attrib: dict, children: list['Element']) -> 'Element':
    if tag == 'svg':
        return SVG(attrib, children)
    return Element(tag, attrib)


class Parser:
    def __init__(self, xml_str: str):
        self.tree = et.fromstring(xml_str)

    def print_tree(self):
        print(self.tree.tag, self.tree.attrib)
        for elem in self.tree:
            if isinstance(elem, et._Comment):
                continue
            if elem.tag == 'g':
                for child in elem:
                    print(child.tag, child.attrib)
            print(elem.tag, elem.attrib)

    def create_svg(self) -> SVG:
        attrib = self.tree.attrib
        children = [create_element(elem.tag, elem.attrib, []) for elem in self.tree]
        return SVG(attrib, children)


if __name__ == '__main__':
    with open(TEST_PATH, 'r') as f:
        xml_str = f.read()
    parser = Parser(xml_str)
    # parser.print_tree()
    svg = parser.create_svg()
    svg.print_tree()