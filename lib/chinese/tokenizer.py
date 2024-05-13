#!/usr/bin/env python
# coding: utf-8

from abc import ABC
from abc import abstractmethod
from enum import Enum, auto
import logging
import os

import jieba

import chinese.errors as errors

logging.getLogger("jieba").setLevel(logging.WARNING)

class Engine(Enum):
    jieba = auto()

class Tokenizer:
    jieba = Engine.jieba
    
    def __init__(self):
        self.tokenizer = Engine.jieba
    
    def tokenize(self, string, *, traditional=False, using=Engine.jieba):
        """Returns a list of tokens"""
        if using == Engine.jieba:
            return self.__jieba_tokenize(string, traditional)
        elif isinstance(using, TokenizerInterface):
            return using.tokenize(string)
        else:
            raise errors.InvalidEngineError('InvalidEngineError: {}'.format(using))

    def __jieba_tokenize(self, string, traditional):
        if traditional:
            directory = os.path.abspath(os.path.dirname(__file__))
            dict_path = os.path.join(directory, 'data', 'dict.txt.big')
            jieba.set_dictionary(dict_path)
        return list(jieba.tokenize(string))

class TokenizerInterface(ABC):

    @abstractmethod
    def tokenize(self, string):
        pass