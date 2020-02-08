#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/1/15 9:02
# @Author : 马飞
# @File : basehandler.py
# @Software: PyCharm

import tornado.web

class basehandler(tornado.web.RequestHandler):
    def init(self):
        pass