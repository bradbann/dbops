#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/5/9 10:19
# @Author : 马飞
# @File : db_inst.py.py
# @Software: PyCharm

import tornado.web
import json
from  web.utils.basehandler   import basehandler
from  web.model.t_db_inst     import query_inst,save_db_inst,upd_db_inst,query_inst_by_id
from  web.model.t_dmmx        import get_dmm_from_dm


class dbinstquery(basehandler):
    @tornado.web.authenticated
    def get(self):
        self.render("./db_inst_query.html",
                    dm_inst_type=get_dmm_from_dm('02'),)

class db_inst_query(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        inst_name  = self.get_argument("inst_name")
        v_list = query_inst(inst_name)
        v_json = json.dumps(v_list)
        self.write(v_json)

class db_inst_query_by_id(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        inst_id  = self.get_argument("inst_id")
        v_list   = query_inst_by_id(inst_id)
        v_json   = json.dumps(v_list)
        self.write(v_json)

class db_inst_save(basehandler):
    @tornado.web.authenticated
    def post(self):
        d_inst = {}
        d_inst['inst_name']         = self.get_argument("inst_name")
        d_inst['inst_ip']           = self.get_argument("inst_ip")
        d_inst['inst_port']         = self.get_argument("inst_port")
        d_inst['inst_type']         = self.get_argument("inst_type")
        d_inst['inst_type']         = self.get_argument("inst_type")
        d_inst['mgr_user']          = self.get_argument("mgr_user")
        d_inst['mgr_pass']          = self.get_argument("mgr_pass")
        d_inst['start_script']      = self.get_argument("start_script")
        d_inst['stop_script']       = self.get_argument("stop_script")
        d_inst['restart_script']    = self.get_argument("restart_script")
        d_inst['auto_start_script'] = self.get_argument("auto_start_script")
        print('inst_add_save=',d_inst)
        result = save_db_inst(d_inst)
        self.write({"code": result['code'], "message": result['message']})


class db_inst_update(basehandler):
    @tornado.web.authenticated
    def post(self):
        d_inst = {}
        d_inst['inst_id']           = self.get_argument("inst_id")
        d_inst['inst_name']         = self.get_argument("inst_name")
        d_inst['inst_ip']           = self.get_argument("inst_ip")
        d_inst['inst_port']         = self.get_argument("inst_port")
        d_inst['inst_type']         = self.get_argument("inst_type")
        d_inst['inst_type']         = self.get_argument("inst_type")
        d_inst['mgr_user']          = self.get_argument("mgr_user")
        d_inst['mgr_pass']          = self.get_argument("mgr_pass")
        d_inst['start_script']      = self.get_argument("start_script")
        d_inst['stop_script']       = self.get_argument("stop_script")
        d_inst['restart_script']    = self.get_argument("restart_script")
        d_inst['auto_start_script'] = self.get_argument("auto_start_script")
        print('db_inst_update=',d_inst)
        result = upd_db_inst(d_inst)
        self.write({"code": result['code'], "message": result['message']})


