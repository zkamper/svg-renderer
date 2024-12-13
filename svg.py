import os
import sys

from common.parser import Parser, gen_parser


if __name__ == "__main__":
    try:
        if len(sys.argv) != 2:
            raise Exception("Usage: python svg.py <svg_file>")
        svg_file = sys.argv[1]
        if not os.path.exists(svg_file):
            raise Exception(f'File "{svg_file}" not found')
        parser = gen_parser(svg_file)
        svg = parser.create_svg()
        svg.draw()
    except Exception as e:
        print(e)
        sys.exit(1)
