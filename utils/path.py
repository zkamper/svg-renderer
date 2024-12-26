import re


TEST_PATH = "M399.1 680.2c-58.4 0-113.3-22.7-154.6-64s-64-96.2-64-154.6 22.7-113.3 64-154.6 96.2-64 154.6-64 113.3 22.7 154.6 64 64 96.2 64 154.6c0 58.4-22.7 113.3-64 154.6-41.4 41.3-96.3 64-154.6 64z m0-426.2c-114.5 0-207.6 93.1-207.6 207.6s93.1 207.6 207.6 207.6 207.6-93.1 207.6-207.6S513.5 254 399.1 254z m0 307.4c-55 0-99.8-44.8-99.8-99.8s44.8-99.8 99.8-99.8 99.8 44.8 99.8 99.8c-0.1 55-44.8 99.8-99.8 99.8z m0-188.6c-49 0-88.8 39.8-88.8 88.8s39.8 88.8 88.8 88.8 88.8-39.8 88.8-88.8c-0.1-49-39.9-88.8-88.8-88.8z"


TOKEN_LIST = ['M', 'C', 'S', 'Q', 'T', 'A', 'Z', 'L', 'H', 'V']
TOKEN_LIST = TOKEN_LIST + [token.lower() for token in TOKEN_LIST]
TOKEN_LIST = TOKEN_LIST + ['-']


def clean_path(path):
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
    return path


def split_path(path):
    pass


if __name__ == '__main__':
    print(clean_path(TEST_PATH))