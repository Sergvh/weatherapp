import os

path = input('Enter directory path please(blank for current):')


def ls(path):
    """
    :param path: path to directory for list
    :return:     prints list of files and directories
    """
    for name in os.listdir(path):
        print(name)


if path == '':
    ls('.')
else:
    ls(path)
