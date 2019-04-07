"""Errors class for project
"""


class WappError(Exception):

    def __init__(self, text):
        WappError.txt = text
