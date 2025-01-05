import re
from common.path.command import *


TEST_PATH = ("M399.1 680.2c-58.4 0-113.3-22.7-154.6-64"
             "s-64-96.2-64-154.6 22.7-113.3 64-154.6 96.2-64 154.6-64 113.3 22.7 154.6 64 64 96.2 64 154.6"
             "c0 58.4-22.7 113.3-64 154.6-41.4 41.3-96.3 64-154.6 64z m0-426.2c-114.5 0-207.6 93.1-207.6 207.6"
             "s93.1 207.6 207.6 207.6 207.6-93.1 207.6-207.6S513.5 254 399.1 254z m0 307.4c-55 0-99.8-44.8-99.8-99.8"
             "s44.8-99.8 99.8-99.8 99.8 44.8 99.8 99.8c-0.1 55-44.8 99.8-99.8 99.8z m0-188.6c-49 0-88.8 39.8-88.8 88.8"
             "s39.8 88.8 88.8 88.8 88.8-39.8 88.8-88.8c-0.1-49-39.9-88.8-88.8-88.8z") # pentru testare


TOKEN_LIST = ['M', 'C', 'S', 'Q', 'T', 'A', 'Z', 'L', 'H', 'V']
TOKEN_LIST = TOKEN_LIST + [token.lower() for token in TOKEN_LIST]
TOKEN_LIST = TOKEN_LIST + ['-'] #lista cu tokeni pentru spli


def clean_path(path: str) -> list[str]:
    """
    Parseaza `d` și generează o listă de comenzi pentru `path`.

    `d` este un string care conține comenzi pentru a desena un path. Acesta conține comenzi precum M (move), Q (quadratic bezier), etc.
    :param path: element `d` din tag-ul `path`
    :return: lista de comenzi pentru `path
    """
    # adaugă spații între tokeni
    for token in TOKEN_LIST:
        if token != '-':
            path = path.replace(token, ' ' + token + ' ')
        else:
            path = path.replace(token, ' ' + token)

    # elimină spațiile multiple și între tipul de path si coordonatele urmatoare
    path = path.lstrip().rstrip()
    path = re.sub(r'\s+', ' ', path)
    path = re.sub(r'([a-zA-Z])\s+(-?\d)', r'\1\2', path)

    # split dupa componente path
    for _ in range(2):
        path = re.sub(r'([0-9z])\s+([a-zA-Z])', r'\1;\2', path)
    path = path.split(sep=';')
    return path


def gen_path(path: list[str]) -> list[Command]:
    """
    Generează o listă de obiecte Node din `path`.
    :param path: listă de comenzi pentru `path`
    :return: comenzile sub formă de clase Node
    """

    path_nodes = []
    for element in path:
        relative = element[0].islower()
        coords = element[1:].split()

        if element[0] in ['M', 'm']:
            for i in range(0, len(coords), 2):
                node = Move(float(coords[i]), float(coords[i+1]), relative)
                path_nodes.append(node)
        elif element[0] in ['L', 'l']:
            for i in range(0, len(coords), 2):
                node = Line(float(coords[i]), float(coords[i+1]), relative)
                path_nodes.append(node)
        elif element[0] in ['H', 'h']:
            for i in range(0, len(coords)):
                node = HLine(float(coords[i]), relative)
                path_nodes.append(node)
        elif element[0] in ['V', 'v']:
            for i in range(0, len(coords)):
                node = VLine(float(coords[i]), relative)
                path_nodes.append(node)
        elif element[0] in ['C', 'c']:
            for i in range(0, len(coords), 6):
                node = CubicBezier(float(coords[i]), float(coords[i+1]), float(coords[i+2]), float(coords[i+3]), float(coords[i+4]), float(coords[i+5]), relative)
                path_nodes.append(node)
        elif element[0] in ['S', 's']:
            for i in range(0, len(coords), 4):
                node = SmoothCubicBezier(float(coords[i]), float(coords[i+1]), float(coords[i+2]), float(coords[i+3]), relative)
                path_nodes.append(node)
        elif element[0] in ['Q', 'q']:
            for i in range(0, len(coords), 4):
                node = QuadraticBezier(float(coords[i]), float(coords[i+1]), float(coords[i+2]), float(coords[i+3]), relative)
                path_nodes.append(node)
        elif element[0] in ['T', 't']:
            for i in range(0, len(coords), 2):
                node = SmoothQuadraticBezier(float(coords[i]), float(coords[i+1]), relative)
                path_nodes.append(node)
        elif element[0] in ['A', 'a']:
            for i in range(0, len(coords), 7):
                node = Arc(float(coords[i]), float(coords[i+1]), float(coords[i+2]), float(coords[i+3]), float(coords[i+4]), float(coords[i+5]), float(coords[i+6]), relative)
                path_nodes.append(node)
        elif element[0] in ['Z', 'z']:
            node = Z(relative)
            path_nodes.append(node)
    return path_nodes


# if __name__ == '__main__':
#     print(clean_path(TEST_PATH))
#     path = clean_path(TEST_PATH)
#     path_nodes = gen_path(path)
#     for node in path_nodes:
#         print(node)