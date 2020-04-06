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
from   web.model.t_role   import save_role,check_role,query_role,upd_role,del_role,get_role_by_roleid
from   web.model.t_xtqx   import get_privs,get_privs_role,get_privs_sys,get_func_privs,get_privs_func,get_privs_func_role
from   web.utils.common   import get_url_root
from   web.utils.basehandler import basehandler


class rolequery(basehandler):
    @tornado.web.authenticated
    def get(self):
        self.render("./role_query.html")

class roleadd(basehandler):
    @tornado.web.authenticated
    def get(self):
        self.render("./role_add.html",
                    privs=get_privs(),func_privs=get_func_privs())

class roleadd_save(basehandler):
    @tornado.web.authenticated
    def post(self):
        d_role={}
        d_role['name']   =self.get_argument("name")
        d_role['status'] = self.get_argument("status")
        d_role['privs']  = self.get_argument("privs").split(",")
        d_role['func_privs'] = self.get_argument("func_privs").split(",")
        result = save_role(d_role)
        self.write({"code": result['code'], "message": result['message']})

class role_check(basehandler):
    @tornado.web.authenticated
    def post(self):
        d_role = {}
        d_role['name']   = self.get_argument("name")
        d_role['status'] = self.get_argument("status")
        d_role['privs']  = self.get_argument("privs").split(",")
        result = check_role(d_role)
        self.write({"code": result['code'], "message": result['message']})

class role_query(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        qname  = self.get_argument("qname")
        v_list = query_role(qname)
        v_json = json.dumps(v_list)
        self.write(v_json)

class rolechange(basehandler):
    @tornado.web.authenticated
    def get(self):
        self.render("./role_change.html", url=get_url_root())

class roleedit(basehandler):
    @tornado.web.authenticated
    def get(self):
        roleid=self.get_argument("roleid")
        d_role=get_role_by_roleid(roleid)
        self.render("./role_edit.html",
                     roleid    = d_role['roleid'],
                     name      = d_role['name'],
                     status    = d_role['status'],
                     priv_sys  =get_privs_sys(roleid),
                     priv_role = get_privs_role(roleid),
                     func_privs= get_privs_func(roleid),
                     func_privs_role  = get_privs_func_role(roleid),
                     url=get_url_root()
                    )

class roleedit_save(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        d_role={}
        d_role['roleid']   = self.get_argument("roleid")
        d_role['name']     = self.get_argument("name")
        d_role['status']   = self.get_argument("status")
        d_role['privs']    = self.get_argument("privs").split(",")
        d_role['func_privs'] = self.get_argument("func_privs").split(",")
        print('roleedit_save=',roleedit_save)
        result=upd_role(d_role)
        self.write({"code": result['code'], "message": result['message']})

class roleedit_del(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        roleid  = self.get_argument("roleid")
        result=del_role(roleid)
        self.write({"code": result['code'], "message": result['message']})
