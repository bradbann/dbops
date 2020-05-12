#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/5/9 10:19
# @Author : 马飞
# @File : db_inst.py.py
# @Software: PyCharm

import tornado.web
import json
from  web.utils.basehandler   import basehandler
from  web.model.t_db_inst     import query_inst_list
from  web.model.t_db_user     import query_db_user,save_db_user
from  web.model.t_dmmx        import get_dmm_from_dm


class dbuserquery(basehandler):
    @tornado.web.authenticated
    def get(self):
        self.render("./db_user_query.html",
                    dm_inst_list  = query_inst_list(),
                    dm_user_status= get_dmm_from_dm('25'),)

class db_user_query(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        user_name  = self.get_argument("user_name")
        v_list = query_db_user(user_name)
        v_json = json.dumps(v_list)
        self.write(v_json)

class db_user_save(basehandler):
    @tornado.web.authenticated
    def post(self):
        d_db_user = {}
        d_db_user['inst_id']     = self.get_argument("add_inst_id")
        d_db_user['db_user']     = self.get_argument("add_db_user")
        d_db_user['db_pass']     = self.get_argument("add_db_pass")
        d_db_user['statement']   = self.get_argument("add_statement")
        d_db_user['status']      = self.get_argument("add_status")
        d_db_user['desc']        = self.get_argument("add_desc")
        print('db_user_save=',d_db_user)
        result = save_db_user(d_db_user)
        self.write({"code": result['code'], "message": result['message']})
