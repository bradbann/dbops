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
from   web.model.t_slow      import save_slow,check_slow,query_slow,upd_slow,del_slow,query_slow_by_id,push_slow
from   web.utils.basehandler import basehandler
from   web.model.t_dmmx      import get_dmm_from_dm,get_inst_names,get_gather_server


class slowquery(basehandler):
    @tornado.web.authenticated
    def get(self):
        self.render("./slow_query.html",
                    dm_env_type  = get_dmm_from_dm('03'),
                    dm_inst_names = get_inst_names(''),
                    )

class slow_query(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        inst_id  = self.get_argument("inst_id")
        inst_env = self.get_argument("inst_env")
        v_list = query_slow(inst_id,inst_env)
        v_json = json.dumps(v_list)
        self.write(v_json)

class slowadd(basehandler):
    @tornado.web.authenticated
    def get(self):
        self.render("./slow_add.html",
                    dm_inst_names=get_inst_names(''),
                    dm_db_server=get_gather_server(),
                    )

class slowadd_save(basehandler):
    @tornado.web.authenticated
    def post(self):
        d_slow={}
        d_slow['inst_id']        = self.get_argument("inst_id")
        d_slow['slow_time']      = self.get_argument("slow_time")
        d_slow['slow_log_name']  = self.get_argument("slow_log_name")
        d_slow['python3_home']   = self.get_argument("python3_home")
        d_slow['script_path']    = self.get_argument("script_path")
        d_slow['script_file']    = self.get_argument("script_file")
        d_slow['api_server']     = self.get_argument("api_server")
        d_slow['slow_status']    = self.get_argument("slow_status")
        print('slowadd_save=',d_slow)
        result = save_slow(d_slow)
        self.write({"code": result['code'], "message": result['message']})

class slow_check(basehandler):
    @tornado.web.authenticated
    def post(self):
        d_slow = {}
        d_slow['inst_id']      = self.get_argument("inst_id")
        d_slow['slow_status'] = self.get_argument("slow_status")
        result = check_slow(d_slow)
        self.write({"code": result['code'], "message": result['message']})

class slowchange(basehandler):
    @tornado.web.authenticated
    def get(self):
        self.render("./slow_change.html",
                    dm_env_type  = get_dmm_from_dm('03'),
                    dm_inst_names = get_inst_names(''),)

class slow_query_by_id(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        slow_id  = self.get_argument("slow_id")
        v_list   = query_slow_by_id(slow_id)
        v_json   = json.dumps(v_list)
        self.write(v_json)


class slowedit_save(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        d_slow={}
        d_slow['slow_id']       = self.get_argument("slow_id")
        d_slow['inst_id']       = self.get_argument("inst_id")
        d_slow['slow_time']     = self.get_argument("slow_time")
        d_slow['slow_log_name'] = self.get_argument("slow_log_name")
        d_slow['python3_home']  = self.get_argument("python3_home")
        d_slow['script_path']   = self.get_argument("script_path")
        d_slow['script_file']   = self.get_argument("script_file")
        d_slow['api_server']    = self.get_argument("api_server")
        d_slow['slow_status']   = self.get_argument("slow_status")
        print('slowedit_save=',slowedit_save)
        result=upd_slow(d_slow)
        self.write({"code": result['code'], "message": result['message']})

class slowedit_del(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        slow_id  = self.get_argument("slow_id")
        result=del_slow(slow_id)
        self.write({"code": result['code'], "message": result['message']})


class slowedit_push(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        slow_id    = self.get_argument("slow_id")
        api_server = self.get_argument("api_server")
        result=push_slow(api_server,slow_id)
        self.write({"code": result['code'], "message": result['message']})

