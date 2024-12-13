from lxml import etree as et

from common.element import Element
from common.rect import Rect
from common.svg import SVG


TEST_PATH = '../test.svg'


def create_element(tag: str, attrib: dict, elem) -> 'Element':
    children = [create_element(child.tag, child.attrib, child) for child in elem if not isinstance(child, et._Comment)]
    if 'rect' in tag:
        element = Rect(attrib)
    else:
        element = Element(tag, attrib)
    element.children = children
    return element


def gen_parser(file_path: str) -> 'Parser':
    with open(file_path, 'r') as f:
        xml_str = f.read()
    return Parser(xml_str)

class Parser:
    def __init__(self, xml_str: str):
        self.tree = et.fromstring(xml_str)

    # def print_tree(self):
    #     print(self.tree.tag, self.tree.attrib)
    #     for elem in self.tree:
    #         if isinstance(elem, et._Comment):
    #             continue
    #         if elem.tag == 'g':
    #             for child in elem:
    #                 print(child.tag, child.attrib)
    #         print(elem.tag, elem.attrib)

    def create_svg(self) -> SVG:
        attrib = self.tree.attrib
        children = [create_element(elem.tag, elem.attrib, elem) for elem in self.tree if not isinstance(elem, et._Comment)]
        return SVG(attrib, children)


if __name__ == '__main__':
    with open(TEST_PATH, 'r') as f:
        xml_str = f.read()
    parser = Parser(xml_str)
    # parser.print_tree()
    svg = parser.create_svg()
    svg.print_tree()
    svg.draw()