#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2018/9/19 15:43
# @Author : 马飞
# @File : role.py.py
# @Software: PyCharm

######################################################################################
#                                                                                    #
#                                   角色管理                                          #
#                                                                                    #
######################################################################################
import json
import tornado.web
from   web.model.t_role   import save_role,check_role,init_role,query_role,upd_role,del_role,get_role_by_roleid
from   web.model.t_xtqx   import get_privs,get_privs_role,get_privs_sys
from   web.utils.common   import get_url_root

class rolequery(tornado.web.RequestHandler):
    def get(self):
        self.render("./role_query.html")

class roleadd(tornado.web.RequestHandler):
    def get(self):
        self.render("./role_add.html",
                    privs=get_privs())

class roleadd_save(tornado.web.RequestHandler):
    def post(self):
        d_role={}
        d_role['name']   =self.get_argument("name")
        d_role['status'] = self.get_argument("status")
        d_role['privs']  = self.get_argument("privs").split(",")
        result = check_role(d_role)
        if result['code'] == '0':
            result = save_role(d_role)
            self.write({"code": result['code'], "message": result['message']})
        else:
            self.write({"code": result['code'], "message": result['message']})


class role_check(tornado.web.RequestHandler):
    def post(self):
        d_role = {}
        d_role['name']   = self.get_argument("name")
        d_role['status'] = self.get_argument("status")
        d_role['privs']  = self.get_argument("privs").split(",")
        result = check_role(d_role)
        self.write({"code": result['code'], "message": result['message']})


class role_init(tornado.web.RequestHandler):
    def get(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        v_list = init_role();
        v_dict = {"data": v_list}
        v_json = json.dumps(v_dict)
        self.write(v_json)


class role_query(tornado.web.RequestHandler):
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        qname  = self.get_argument("qname")
        v_list = query_role(qname)
        v_json = json.dumps(v_list)
        self.write(v_json)

class rolechange(tornado.web.RequestHandler):
    def get(self):
        self.render("./role_change.html", url=get_url_root())

class roleedit(tornado.web.RequestHandler):
    def get(self):
        roleid=self.get_argument("roleid")
        d_role=get_role_by_roleid(roleid)
        self.render("./role_edit.html",
                     roleid    = d_role['roleid'],
                     name      = d_role['name'],
                     status    = d_role['status'],
                     priv_role = get_privs_role(roleid),
                     priv_sys  = get_privs_sys(roleid),
                     url=get_url_root()
                    )

class roleedit_save(tornado.web.RequestHandler):
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        d_role={}
        d_role['roleid']   = self.get_argument("roleid")
        d_role['name']     = self.get_argument("name")
        d_role['status']   = self.get_argument("status")
        d_role['privs']    = self.get_argument("privs").split(",")
        result=upd_role(d_role)
        self.write({"code": result['code'], "message": result['message']})

class roleedit_del(tornado.web.RequestHandler):
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        roleid  = self.get_argument("roleid")
        result=del_role(roleid)
        self.write({"code": result['code'], "message": result['message']})
