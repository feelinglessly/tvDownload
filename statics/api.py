import os


def get_file_path(name):
    return os.path.dirname(os.path.abspath(__file__)) + os.sep + name
