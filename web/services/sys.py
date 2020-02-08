#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2018/9/19 16:14
# @Author : 马飞
# @File : initialize.py
# @Software: PyCharm

######################################################################################
#                                                                                    #
#                                   系统设置                                          #
#                                                                                    #
######################################################################################

import json
import tornado.web
from web.model.t_ds   import get_dss_sql_query
from web.model.t_sys  import save_audit_rule,query_dm

class audit_rule(tornado.web.RequestHandler):
   def get(self):
       logon_name = str(self.get_secure_cookie("username"), encoding="utf-8")
       self.render("./audit_rule.html", dss=get_dss_sql_query(logon_name))

class audit_rule_save(tornado.web.RequestHandler):
   def post(self):
       self.set_header("Content-Type", "application/json; charset=UTF-8")
       rule={}
       rule['switch_check_ddl']               = self.get_argument("switch_check_ddl")
       rule['switch_tab_not_exists_pk']       = self.get_argument("switch_tab_not_exists_pk")
       rule['switch_tab_pk_id']               = self.get_argument("switch_tab_pk_id")
       rule['switch_tab_pk_auto_incr']        = self.get_argument("switch_tab_pk_auto_incr")
       rule['switch_tab_pk_autoincrement_1']  = self.get_argument("switch_tab_pk_autoincrement_1")

       rule['switch_pk_not_int_bigint']       = self.get_argument("switch_pk_not_int_bigint")
       rule['switch_tab_comment']             = self.get_argument("switch_tab_comment")
       rule['switch_col_comment']             = self.get_argument("switch_col_comment")
       rule['switch_col_not_null']            = self.get_argument("switch_col_not_null")

       rule['switch_col_default_value']       = self.get_argument("switch_col_default_value")
       rule['switch_tcol_default_value']      = self.get_argument("switch_tcol_default_value")
       rule['switch_char_max_len']            = self.get_argument("switch_char_max_len")
       rule['switch_tab_has_time_fields']     = self.get_argument("switch_tab_has_time_fields")

       rule['switch_tab_tcol_datetime']       = self.get_argument("switch_tab_tcol_datetime")
       rule['switch_tab_char_total_len']      = self.get_argument("switch_tab_char_total_len")
       rule['switch_check_ddl']               = self.get_argument("switch_check_ddl")
       rule['switch_virtual_col']             = self.get_argument("switch_virtual_col")

       rule['switch_tab_max_len']             = self.get_argument("switch_tab_max_len")

       print('audit_rule_save=',rule)
       result = save_audit_rule(rule)
       self.write({"code": result['code'], "message": result['message']})


class sys_setting(tornado.web.RequestHandler):
   def get(self):
       logon_name = str(self.get_secure_cookie("username"), encoding="utf-8")
       self.render("./sys_setting.html")

class sys_code(tornado.web.RequestHandler):
   def get(self):
       logon_name = str(self.get_secure_cookie("username"), encoding="utf-8")
       self.render("./sys_code.html")

class sys_code_query(tornado.web.RequestHandler):
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        code     = self.get_argument("code")
        v_list   = query_dm(code)
        v_json   = json.dumps(v_list)
        self.write(v_json)

class sys_test(tornado.web.RequestHandler):
   def get(self):
       logon_name = str(self.get_secure_cookie("username"), encoding="utf-8")
       self.render("./his/backup_log_analyze.bak.html")
