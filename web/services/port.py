#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/9/5 16:08
# @Author : 马飞
# @File : ds.py
# @Software: PyCharm
######################################################################################
#                                                                                    #
#                                   数据库备份管理                                        #
#                                                                                    #
######################################################################################

import json
import tornado.web
from  web.model.t_user import get_users
from   web.model.t_port import query_port,save_port,get_port_by_portid,upd_port,del_port
from   web.model.t_transfer import query_transfer_log,push_transfer_task,run_transfer_task,stop_transfer_task,query_transfer_detail
from   web.model.t_dmmx import get_dmm_from_dm,get_sync_server,get_sync_db_server
from   web.utils.common import current_rq2


class portquery(tornado.web.RequestHandler):
    def get(self):
        self.render("./port_query.html" )

class port_query(tornado.web.RequestHandler):
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        app_name  = self.get_argument("app_name")
        v_list    = query_port(app_name)
        v_json    = json.dumps(v_list)
        self.write(v_json)

class portadd(tornado.web.RequestHandler):
    def get(self):
        self.render("./port_add.html",developer=get_users('01'))

class portadd_save(tornado.web.RequestHandler):
    def post(self):
        d_port = {}
        d_port['app_name']    = self.get_argument("app_name")
        d_port['app_port']    = self.get_argument("app_port")
        d_port['app_dev']     = self.get_argument("app_dev")
        d_port['app_desc']    = self.get_argument("app_desc")
        d_port['app_ext']     = self.get_argument("app_ext")
        print('portadd_save=',d_port)
        result=save_port(d_port)
        self.write({"code": result['code'], "message": result['message']})

class portchange(tornado.web.RequestHandler):
    def get(self):
        self.render("./port_change.html")

class portedit(tornado.web.RequestHandler):
    def get(self):
        port_id   = self.get_argument("port_id")
        d_transfer    = get_port_by_portid(port_id)
        self.render("./port_edit.html")

class portedit_save(tornado.web.RequestHandler):
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        d_transfer = {}
        d_transfer['transfer_id']     = self.get_argument("transfer_id")
        d_transfer['transfer_tag']    = self.get_argument("transfer_tag")
        d_transfer['task_desc']       = self.get_argument("task_desc")
        d_transfer['transfer_server'] = self.get_argument("transfer_server")
        d_transfer['transfer_type']   = self.get_argument("transfer_type")
        d_transfer['sour_db_server']  = self.get_argument("sour_db_server")
        d_transfer['sour_db_name']    = self.get_argument("sour_db_name")
        d_transfer['sour_tab_name']   = self.get_argument("sour_tab_name")
        d_transfer['sour_tab_where']  = self.get_argument("sour_tab_where")
        d_transfer['dest_db_server']  = self.get_argument("dest_db_server")
        d_transfer['dest_db_name']    = self.get_argument("dest_db_name")
        d_transfer['python3_home']    = self.get_argument("python3_home")
        d_transfer['script_base']     = self.get_argument("script_base")
        d_transfer['script_name']     = self.get_argument("script_name")
        d_transfer['batch_size']      = self.get_argument("batch_size")
        d_transfer['api_server']      = self.get_argument("api_server")
        d_transfer['status']          = self.get_argument("status")
        print(d_transfer)
        result=upd_port(d_transfer)
        self.write({"code": result['code'], "message": result['message']})

class portedit_del(tornado.web.RequestHandler):
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        transfer_id  = self.get_argument("transferid")
        result=del_port(transfer_id)
        self.write({"code": result['code'], "message": result['message']})
