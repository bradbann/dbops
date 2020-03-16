#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/1/15 9:02
# @Author : 马飞
# @File : basehandler.py
# @Software: PyCharm

import tornado.web
from web.model.t_xtqx  import check_url
class basehandler(tornado.web.RequestHandler):
    def get_current_user(self):
        userid = ''
        if self.get_secure_cookie("userid") is not None:
            userid = str(self.get_secure_cookie("userid"), encoding="utf-8")

        print('basehandler=',userid,self.request.uri)
        if self.request.uri!='/':
           if userid == '':
              print('已退出系统，无法访问!')
              return None
           if check_url(userid,self.request.uri.split('?')[0]):
               return self.get_secure_cookie("userid")
           else:
               print("basehandler=>用户:{0}无访问'{1}'权限!".format(userid,self.request.uri))
               return None
        else:
            return self.get_secure_cookie("userid")
