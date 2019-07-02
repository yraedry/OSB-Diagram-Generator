import os


def create_dirs(path):
    os.mkdir(path)


def check_dirs(path):
    return os.path.exists(path)
