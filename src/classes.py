import os
from chinese import ChineseAnalyzer

DICTIONARY_FILE = "cedict_ts.u8"
# test = '領證的前一晚我問他：「你是什麼時候開始喜歡我的？」'

class ChineseInfo:
    def __init__(self, traditional = True, dict_path = None):
        self.traditional = traditional
        self._engine = ChineseAnalyzer()
    def lookup(self, string):
        return self._engine.parse(string, traditional = self.traditional)

# # # TODO: Find way to discern simplified and traditional dynamically
# chinese_info = ChineseInfo(traditional=True)
# parsed = chinese_info.lookup(test)
# # print(parsed)
# # print(parsed.tokens(details=True))
# print(parsed.pinyin_list())