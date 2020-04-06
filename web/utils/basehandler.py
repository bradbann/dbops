#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/1/15 9:02
# @Author : 马飞
# @File : basehandler.py
# @Software: PyCharm

import tornado.web
import time
from tornado.web import HTTPError
from web.model.t_xtqx  import check_url

class basehandler(tornado.web.RequestHandler):
    def get_current_user(self):
        userid = ''
        if self.get_secure_cookie("userid") is not None:
            userid = str(self.get_secure_cookie("userid"), encoding="utf-8")

        print('basehandler=',userid,self.request.uri)

        if self.request.uri!='/':
           self.set_secure_cookie("view_url", self.request.uri, expires=time.time() + 60)

           if userid  is None or userid == '':
               if self.request.method in ("GET", "HEAD"):
                   return self.get_secure_cookie("userid")
               else:
                   raise HTTPError(403,'登陆信息已过期，请重新登陆!')

           if check_url(userid,self.request.uri.split('?')[0]):
              return self.get_secure_cookie("userid")
           else:
              raise HTTPError(502,"basehandler=>用户:{0}无访问'{1}'权限!".format(userid,self.request.uri))

        else:
            self.set_secure_cookie("view_url", '/main', expires=time.time() + 60)
            return self.get_secure_cookie("userid")
