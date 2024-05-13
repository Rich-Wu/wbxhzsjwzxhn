import os
from chinese import ChineseAnalyzer

DICTIONARY_FILE = "cedict_ts.u8"

class ChineseInfo:
    def __init__(self, traditional = True, dict_path = None):
        self.traditional = traditional
        self._engine = ChineseAnalyzer()
    def lookup(self, string):
        return self._engine.parse(string, traditional = self.traditional)