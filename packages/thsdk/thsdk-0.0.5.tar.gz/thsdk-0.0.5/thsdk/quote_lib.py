#!/usr/bin/env python
# -*- coding:utf-8 -*-


import ctypes
import os
import platform
import json


class QuoteLib:
    def __init__(self, ops: dict = ()):
        self.__lib_path = self._get_lib_path()

        self._lib = ctypes.CDLL(self.__lib_path)
        self._lib.NewQuote.argtypes = [ctypes.c_char_p]
        self._lib.NewQuote.restype = None
        self._lib.Connect.restype = ctypes.c_char_p
        self._lib.DisConnect.restype = ctypes.c_char_p
        self._lib.QueryData.argtypes = [ctypes.c_char_p]
        self._lib.QueryData.restype = ctypes.c_char_p
        self._lib.About.restype = ctypes.c_char_p
        self._lib.NewQuote(json.dumps(ops).encode('utf-8'))

    def _get_lib_path(self):
        # todo M芯片暂未支持
        system = platform.system()
        arch = platform.machine()
        if system == 'Linux':
            lib_path = os.path.join(os.path.dirname(__file__), 'libquote.so')
        elif system == 'Darwin':  # intel
            lib_path = os.path.join(os.path.dirname(__file__), 'libquote.dylib')
        elif system == 'Windows':
            lib_path = os.path.join(os.path.dirname(__file__), 'libquote.dll')
        else:
            raise OSError('Unsupported operating system')
        return lib_path

    def connect(self):
        return self._lib.Connect()

    def disconnect(self):
        return self._lib.DisConnect()

    def query_data(self, req: str):
        return self._lib.QueryData(req.encode('utf-8'))

    def about(self):
        # 版本信息 About
        return self._lib.About()
