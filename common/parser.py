from lxml import etree as et

from common.element import Element
from common.svg import SVG
from utils.gen_element import gen_element

TEST_PATH = '../test_img/test.svg'


def create_element(tag: str, attrib: dict, elem) -> 'Element':
    children = [create_element(child.tag, child.attrib, child) for child in elem if not isinstance(child, et._Comment)]
    element = gen_element(tag, attrib)
    element.children = children
    return element


def gen_parser(file_path: str) -> 'Parser':
    with open(file_path, 'r') as f:
        xml_str = f.read()
    return Parser(xml_str)

class Parser:
    """
    Clasa care se ocupa cu parsarea unui XML și generarea obiectului SVG corespunzător

    :param xml_str: string-ul XML care trebuie parsat
    """
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

    def create_svg(self, name: str) -> SVG:
        """
        Creează un obiect SVG pe baza arborelui de elemente XML generat de parser
        :param name: numele fișierului de ieșire
        :return:
        """
        attrib = self.tree.attrib
        children = [create_element(elem.tag, elem.attrib, elem) for elem in self.tree if not isinstance(elem, et._Comment)]
        return SVG(attrib, children, name)


if __name__ == '__main__':
    parser = gen_parser(TEST_PATH)
    svg = parser.create_svg(TEST_PATH)
    svg.print_tree()
    svg.draw()