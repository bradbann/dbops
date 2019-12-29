#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2018/9/19 16:14
# @Author : 马飞
# @File : initialize.py
# @Software: PyCharm

######################################################################################
#                                                                                    #
#                                   数据库操作                                         #
#   1.增加批量发布功能                                                                  #
#                                                                                    #
######################################################################################

import json
import tornado.web
from web.model.t_sql           import exe_query
from web.model.t_sql_check     import query_check_result
from web.model.t_sql_release   import upd_sql,exe_sql,save_sql,query_audit,query_audit_sql,check_sql,format_sql
from web.model.t_ds            import get_dss_sql_query,get_dss2_sql_query,get_dss_sql_release
from web.model.t_user          import get_user_by_loginame
from web.model.t_xtqx          import get_tab_ddl_by_tname,get_tab_idx_by_tname,get_tree_by_dbid,alt_tab_desc,get_db_name,get_tab_name
from web.model.t_dmmx          import get_dmm_from_dm

class sqlquery(tornado.web.RequestHandler):
   def get(self):
       logon_name = str(self.get_secure_cookie("username"), encoding="utf-8")
       self.render("./sql_query.html", dss=get_dss_sql_query(logon_name))

class sql_query(tornado.web.RequestHandler):
   def post(self):
       self.set_header("Content-Type", "application/json; charset=UTF-8")
       dbid   = self.get_argument("dbid")
       sql    = self.get_argument("sql")
       curdb  = self.get_argument("cur_db")
       print('sql_query=',dbid,sql,'curdb=',curdb)
       result = exe_query(dbid,sql,curdb)
       v_dict = {"data": result['data'],"column":result['column'],"status":result['status'],"msg":result['msg']}
       v_json = json.dumps(v_dict)
       self.write(v_json)

class sqlrelease(tornado.web.RequestHandler):
   def get(self):
       logon_name = str(self.get_secure_cookie("username"), encoding="utf-8")
       self.render("./sql_release.html",
                   dss=get_dss_sql_release(logon_name),
                   vers=get_dmm_from_dm('12'),
                   orders=get_dmm_from_dm('13'),
                   )

class sql_release(tornado.web.RequestHandler):
   def post(self):
       self.set_header("Content-Type", "application/json; charset=UTF-8")
       logon_name = str(self.get_secure_cookie("username"), encoding="utf-8")
       user       = get_user_by_loginame(logon_name)
       dbid       = self.get_argument("dbid")
       cdb        = self.get_argument("cur_db")
       sql        = self.get_argument("sql")
       desc       = self.get_argument("desc")
       ver        = self.get_argument("ver")
       type       = self.get_argument("type")

       print('sql_release.user=',user)
       result     = save_sql(dbid,cdb,sql,desc,user,ver,type)
       self.write({"code": result['code'], "message": result['message']})

class sql_check(tornado.web.RequestHandler):
   def post(self):
       self.set_header("Content-Type", "application/json; charset=UTF-8")
       logon_name = str(self.get_secure_cookie("username"), encoding="utf-8")
       user       = get_user_by_loginame(logon_name)
       dbid       = self.get_argument("dbid")
       cdb        = self.get_argument("cur_db")
       sql        = self.get_argument("sql")
       desc       = self.get_argument("desc")
       type       = self.get_argument("type")
       print('sql_release.user=',user)
       result     = check_sql(dbid,cdb,sql,desc,user,type)
       self.write({"code": result['code'], "message": result['message']})

class sql_format(tornado.web.RequestHandler):
   def post(self):
       self.set_header("Content-Type", "application/json; charset=UTF-8")
       sql        = self.get_argument("sql")
       result     = format_sql(sql)
       self.write({"code": result['code'], "message": result['message']})


class sql_check_result(tornado.web.RequestHandler):
   def post(self):
       self.set_header("Content-Type", "application/json; charset=UTF-8")
       logon_name = str(self.get_secure_cookie("username"), encoding="utf-8")
       user   = get_user_by_loginame(logon_name)
       dbid   = self.get_argument("dbid")
       sql    = self.get_argument("sql")
       curdb  = self.get_argument("cur_db")
       print('sql_query=',dbid,sql,'curdb=',curdb)
       v_list = query_check_result(user)
       v_dict = {"data": v_list}
       v_json = json.dumps(v_dict)
       self.write(v_json)


class sqlaudit(tornado.web.RequestHandler):
   def get(self):
       logon_name = str(self.get_secure_cookie("username"), encoding="utf-8")
       self.render("./sql_audit.html",dss=get_dss2_sql_query(logon_name))

class sql_audit(tornado.web.RequestHandler):
   def post(self):
       self.set_header("Content-Type", "application/json; charset=UTF-8")
       sqlid  = self.get_argument("sqlid")
       result = upd_sql(sqlid);
       self.write({"code": result['code'], "message": result['message']})

class sql_run(tornado.web.RequestHandler):
   def post(self):
       self.set_header("Content-Type", "application/json; charset=UTF-8")
       dbid    = self.get_argument("dbid")
       db_name = self.get_argument("db_name")
       sql_id  = self.get_argument("sql_id")
       print('sql_run=',dbid,db_name,sql_id)

       result = exe_sql(dbid,db_name,sql_id)
       self.write({"code": result['code'], "message": result['message']})


class sql_audit_query(tornado.web.RequestHandler):
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        qname  = self.get_argument("qname")
        v_list = query_audit(qname)
        v_json = json.dumps(v_list)
        self.write(v_json)

class sql_audit_detail(tornado.web.RequestHandler):
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        id = self.get_argument("id")
        v_list = query_audit_sql(id)
        v_json = json.dumps(v_list)
        self.write(v_json)

class get_tree_by_sql(tornado.web.RequestHandler):
    def post(self):
        dbid   = self.get_argument("dbid")
        print('get_tree2=',dbid)
        result = get_tree_by_dbid(dbid)
        self.write({"code": result['code'], "message": result['message'], "url": result['db_url'],"desc":result['desc']})

class get_tab_ddl(tornado.web.RequestHandler):
    def post(self):
        dbid  = self.get_argument("dbid")
        tab   = self.get_argument("tab")
        print('get_tab_ddl=',dbid,tab)
        result = get_tab_ddl_by_tname(dbid,tab)
        self.write({"code": result['code'], "message": result['message']})

class get_tab_idx(tornado.web.RequestHandler):
    def post(self):
        dbid  = self.get_argument("dbid")
        tab   = self.get_argument("tab")
        print('get_tab_ddl=',dbid,tab)
        result = get_tab_idx_by_tname(dbid,tab)
        self.write({"code": result['code'], "message": result['message']})

class alt_tab(tornado.web.RequestHandler):
    def post(self):
        dbid  = self.get_argument("dbid")
        tab   = self.get_argument("tab")
        print('get_tab_ddl=',dbid,tab)
        result = alt_tab_desc(dbid,tab)
        self.write({"code": result['code'], "message": result['message']})

class get_database(tornado.web.RequestHandler):
    def post(self):
        dbid  = self.get_argument("dbid")
        print('get_database=',dbid)
        result = get_db_name(dbid)
        self.write({"code": result['code'], "message": result['message']})

class get_tables(tornado.web.RequestHandler):
    def post(self):
        dbid  = self.get_argument("dbid")
        db_name = self.get_argument("db_name")
        print('get_tables=',dbid,db_name)
        result = get_tab_name(dbid,db_name)
        self.write({"code": result['code'], "message": result['message']})

