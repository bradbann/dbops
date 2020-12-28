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
from web.model.t_sql_release   import upd_sql,exe_sql,save_sql,query_audit,query_run,query_order,query_audit_sql,check_sql,format_sql
from web.model.t_sql_release   import query_order_no,save_order,delete_order,query_wtd,query_wtd_detail,release_order,get_order_attachment_number,upd_order
from web.model.t_ds            import get_dss_sql_query,get_dss_sql_run,get_dss_order,get_dss_sql_release,get_dss_sql_audit
from web.model.t_user          import get_user_by_loginame,get_user_by_userid
from web.model.t_xtqx          import get_tab_ddl_by_tname,get_tab_idx_by_tname,get_tree_by_dbid,get_tree_by_dbid_mssql,alt_tab_desc
from web.model.t_xtqx          import get_db_name,get_tab_name,get_tab_columns,get_tab_structure,get_tab_keys,get_tab_incr_col,query_ds
from web.model.t_xtqx          import get_tree_by_dbid_proxy,get_tree_by_dbid_mssql_proxy,get_tree_by_dbid_layui
from web.model.t_dmmx          import get_dmm_from_dm,get_users_from_proj
from web.utils.basehandler     import basehandler
from web.model.t_ds            import get_ds_by_dsid

class sqlquery(basehandler):
   @tornado.web.authenticated
   def get(self):
       logon_name = str(self.get_secure_cookie("username"), encoding="utf-8")
       self.render("./sql_query.html", dss=get_dss_sql_query(logon_name))

class sql_query(basehandler):
   @tornado.web.authenticated
   def post(self):
       self.set_header("Content-Type", "application/json; charset=UTF-8")
       dbid   = self.get_argument("dbid")
       sql    = self.get_argument("sql")
       curdb  = self.get_argument("cur_db")
       result = exe_query(dbid,sql,curdb)
       v_dict = {"data": result['data'],"column":result['column'],"status":result['status'],"msg":result['msg']}
       v_json = json.dumps(v_dict)
       self.write(v_json)

class sqlrelease(basehandler):
    @tornado.web.authenticated
    def get(self):
       logon_name = str(self.get_secure_cookie("username"), encoding="utf-8")
       self.render("./sql_release.html",
                   dss=get_dss_sql_release(logon_name),
                   vers=get_dmm_from_dm('12'),
                   orders=get_dmm_from_dm('13'),
                   )

class sql_release(basehandler):
   @tornado.web.authenticated
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
       result     = save_sql(dbid,cdb,sql,desc,user,ver,type)
       self.write({"code": result['code'], "message": result['message']})

class sql_check(basehandler):
   @tornado.web.authenticated
   def post(self):
       self.set_header("Content-Type", "application/json; charset=UTF-8")
       logon_name = str(self.get_secure_cookie("username"), encoding="utf-8")
       user       = get_user_by_loginame(logon_name)
       dbid       = self.get_argument("dbid")
       cdb        = self.get_argument("cur_db")
       sql        = self.get_argument("sql")
       desc       = self.get_argument("desc")
       type       = self.get_argument("type")
       result     = check_sql(dbid,cdb,sql,desc,user,type)
       self.write({"code": result['code'], "message": result['message']})

class sql_format(basehandler):
   @tornado.web.authenticated
   def post(self):
       self.set_header("Content-Type", "application/json; charset=UTF-8")
       sql        = self.get_argument("sql")
       result     = format_sql(sql)
       self.write({"code": result['code'], "message": result['message']})


class sql_check_result(basehandler):
   @tornado.web.authenticated
   def post(self):
       self.set_header("Content-Type", "application/json; charset=UTF-8")
       logon_name = str(self.get_secure_cookie("username"), encoding="utf-8")
       user   = get_user_by_loginame(logon_name)
       dbid   = self.get_argument("dbid")
       sql    = self.get_argument("sql")
       curdb  = self.get_argument("cur_db")
       v_list = query_check_result(user)
       v_dict = {"data": v_list}
       v_json = json.dumps(v_dict)
       self.write(v_json)


class sqlaudit(basehandler):
   @tornado.web.authenticated
   def get(self):
       logon_name = str(self.get_secure_cookie("username"), encoding="utf-8")
       self.render("./sql_audit.html",
                   audit_dss=get_dss_sql_audit(logon_name),
                   vers=get_dmm_from_dm('12'))

class sql_audit(basehandler):
   @tornado.web.authenticated
   def post(self):
       self.set_header("Content-Type", "application/json; charset=UTF-8")
       userid = str(self.get_secure_cookie("userid"), encoding="utf-8")
       d_user = get_user_by_userid(userid)
       sqlid  = self.get_argument("sqlid")
       result = upd_sql(sqlid,d_user)
       self.write({"code": result['code'], "message": result['message']})

class sqlrun(basehandler):
   @tornado.web.authenticated
   def get(self):
       logon_name = str(self.get_secure_cookie("username"), encoding="utf-8")
       self.render("./sql_run.html",run_dss=get_dss_sql_run(logon_name),vers=get_dmm_from_dm('12'))


class sql_run(basehandler):
   @tornado.web.authenticated
   def post(self):
       self.set_header("Content-Type", "application/json; charset=UTF-8")
       dbid    = self.get_argument("dbid")
       db_name = self.get_argument("db_name")
       sql_id  = self.get_argument("sql_id")
       userid = str(self.get_secure_cookie("userid"), encoding="utf-8")
       d_user = get_user_by_userid(userid)
       result = exe_sql(dbid,db_name,sql_id,d_user)
       self.write({"code": result['code'], "message": result['message']})


class sql_audit_query(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        qname  = self.get_argument("qname")
        dsid   = self.get_argument("dsid")
        ver    = self.get_argument("ver")
        userid = str(self.get_secure_cookie("userid"), encoding="utf-8")
        v_list = query_audit(qname,dsid,ver,userid)
        v_json = json.dumps(v_list)
        self.write(v_json)

class sql_run_query(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        qname  = self.get_argument("qname")
        dsid   = self.get_argument("dsid")
        ver    = self.get_argument("ver")
        userid = str(self.get_secure_cookie("userid"), encoding="utf-8")
        v_list = query_run(qname,dsid,ver,userid)
        v_json = json.dumps(v_list)
        self.write(v_json)


class sql_audit_detail(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        id     = self.get_argument("id")
        v_list = query_audit_sql(id)
        v_json = json.dumps(v_list)
        self.write(v_json)

class get_tree_by_sql(basehandler):
    @tornado.web.authenticated
    def post(self):
        dbid   = self.get_argument("dbid")
        p_ds   = get_ds_by_dsid(dbid)
        result = {}
        if p_ds['db_type'] == '0':
            if p_ds['proxy_status'] == '1':
                result = get_tree_by_dbid_proxy(dbid)
            else:
                result = get_tree_by_dbid(dbid)
                #result = get_tree_by_dbid_layui(dbid)

        elif p_ds['db_type'] == '2':
            if p_ds['proxy_status'] == '1':
                result = get_tree_by_dbid_mssql_proxy(dbid)
            else:
                result = get_tree_by_dbid_mssql(dbid)

        self.write({"code": result['code'], "message": result['message'], "url": result['db_url'],"desc":result['desc']})


class get_tab_ddl(basehandler):
    def post(self):
        dbid    = self.get_argument("dbid")
        cur_db  = self.get_argument("cur_db")
        tab     = self.get_argument("tab")
        result = get_tab_ddl_by_tname(dbid,tab,cur_db)
        self.write({"code": result['code'], "message": result['message']})

class get_tab_idx(basehandler):
    def post(self):
        dbid   = self.get_argument("dbid")
        cur_db = self.get_argument("cur_db")
        tab    = self.get_argument("tab")
        result = get_tab_idx_by_tname(dbid,tab,cur_db)
        self.write({"code": result['code'], "message": result['message']})

class alt_tab(basehandler):
    def post(self):
        dbid   = self.get_argument("dbid")
        cur_db = self.get_argument("cur_db")
        tab    = self.get_argument("tab")
        result = alt_tab_desc(dbid,tab)
        self.write({"code": result['code'], "message": result['message']})

class get_database(basehandler):
    def post(self):
        dbid  = self.get_argument("dbid")
        result = get_db_name(dbid)
        self.write({"code": result['code'], "message": result['message']})

class get_tables(basehandler):
    def post(self):
        dbid   = self.get_argument("dbid")
        db_name = self.get_argument("db_name")
        result = get_tab_name(dbid,db_name)
        self.write({"code": result['code'], "message": result['message']})

class get_dmm_dm(basehandler):
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        dm   = self.get_argument("dm")
        v_list = get_dmm_from_dm(dm)
        v_json = json.dumps(v_list)
        self.write(v_json)


class get_columns(basehandler):
    def post(self):
        dbid     = self.get_argument("dbid")
        db_name  = self.get_argument("db_name")
        tab_name = self.get_argument("tab_name")
        result = get_tab_columns(dbid,db_name,tab_name)
        self.write({"code": result['code'], "message": result['message']})


class get_ds(basehandler):
    def post(self):
        dsid   = self.get_argument("dsid")
        result = query_ds(dsid)
        self.write({"code": result['code'], "message": result['message']})


class get_keys(basehandler):
    def post(self):
        dbid     = self.get_argument("dbid")
        db_name  = self.get_argument("db_name")
        tab_name = self.get_argument("tab_name")
        result = get_tab_keys(dbid,db_name,tab_name)
        self.write({"code": result['code'], "message": result['message']})

class get_incr_col(basehandler):
    def post(self):
        dbid     = self.get_argument("dbid")
        db_name  = self.get_argument("db_name")
        tab_name = self.get_argument("tab_name")
        result = get_tab_incr_col(dbid,db_name,tab_name)
        self.write({"code": result['code'], "message": result['message']})


class get_tab_stru(basehandler):
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        dbid     = self.get_argument("dbid")
        db_name  = self.get_argument("db_name")
        tab_name = self.get_argument("tab_name")
        v_list = get_tab_structure(dbid,db_name,tab_name)
        v_json = json.dumps(v_list)
        self.write(v_json)



class orderquery(basehandler):
    @tornado.web.authenticated
    def get(self):
        logon_name = str(self.get_secure_cookie("username"), encoding="utf-8")
        userid = str(self.get_secure_cookie("userid"), encoding="utf-8")
        self.render("./order_query.html",
                    order_dss=get_dss_order(logon_name),
                    vers=get_dmm_from_dm('12'),
                    order_types=get_dmm_from_dm('17'),
                    order_handles = get_users_from_proj(userid),
                    order_status = get_dmm_from_dm('19')
                    )

class order_query(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        userid = str(self.get_secure_cookie("userid"), encoding="utf-8")
        qname  = self.get_argument("qname")
        dsid   = self.get_argument("dsid")
        ver    = self.get_argument("ver")
        v_list = query_order(qname,dsid,ver,userid)
        v_json = json.dumps(v_list)
        self.write(v_json)

class wtd_query(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        userid = str(self.get_secure_cookie("userid"), encoding="utf-8")
        v_list = query_wtd(userid)
        v_json = json.dumps(v_list)
        self.write(v_json)

class wtd_detail(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        userid = str(self.get_secure_cookie("userid"), encoding="utf-8")
        v_wtd_no = self.get_argument("wtd_no")
        v_list = query_wtd_detail(v_wtd_no,userid)
        v_json = json.dumps(v_list)
        self.write(v_json)


class get_order_no(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "text/plain; charset=UTF-8")
        v_no = query_order_no()
        self.write(v_no)

class get_order_env(basehandler):
    @tornado.web.authenticated
    def post(self):
        logon_name = str(self.get_secure_cookie("username"), encoding="utf-8")
        result = get_dss_order(logon_name)
        self.write({"message": result})


class get_order_type(basehandler):
    @tornado.web.authenticated
    def post(self):
        result = get_dmm_from_dm('17')
        self.write({"message": result})

class get_order_status(basehandler):
    @tornado.web.authenticated
    def post(self):
        result = get_dmm_from_dm('19')
        self.write({"message": result})

class get_order_handler(basehandler):
    @tornado.web.authenticated
    def post(self):
        userid = str(self.get_secure_cookie("userid"), encoding="utf-8")
        result = get_users_from_proj(userid),
        self.write({"message": result})

class wtd_save(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        userid   = str(self.get_secure_cookie("userid"), encoding="utf-8")
        order_number = self.get_argument("order_number")
        order_env    = self.get_argument("order_env")
        order_type   = self.get_argument("order_type")
        order_status = self.get_argument("order_status")
        order_handle = self.get_argument("order_handle")
        order_desc   = self.get_argument("order_desc")
        attachment_path = self.get_argument("attachment_path")
        attachment_name = self.get_argument("attachment_name")
        v_list = save_order(order_number,order_env,order_type,order_status,order_handle,order_desc,userid,attachment_path,attachment_name)
        v_json = json.dumps(v_list)
        self.write(v_json)


class wtd_save_uploadImage(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        static_path  = self.get_template_path().replace("templates", "static")
        file_metas   = self.request.files["file"]
        order_number = self.get_argument("order_number")
        try:
            i_sxh = 1
            v_path = []
            v_name = []
            for meta in file_metas:
                file_path = static_path+'/'+'assets/images/wtd'
                file_name=order_number+'_'+str(i_sxh)+'.'+meta['filename'].split('.')[-1]
                with open(file_path+'/'+file_name, 'wb') as up:
                    up.write(meta['body'])
                v_path.append('/'+'/'.join(file_path.split('/')[11:]))
                v_name.append(file_name)
                i_sxh =i_sxh +1
            self.write({"code": 0, "file_path": ','.join(v_path),"file_name":','.join(v_name)})
        except Exception as e:
            print(e)
            self.write({"code": -1, "message": '保存图片失败'+str(e)})


class wtd_release(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        userid = str(self.get_secure_cookie("userid"), encoding="utf-8")
        wtd_no = self.get_argument("wtd_no")
        v_list = release_order(wtd_no,userid)
        v_json = json.dumps(v_list)
        self.write(v_json)


class wtd_update(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        order_number    = self.get_argument("order_number")
        order_env       = self.get_argument("order_env")
        order_type      = self.get_argument("order_type")
        order_status    = self.get_argument("order_status")
        order_handle    = self.get_argument("order_handle")
        order_desc      = self.get_argument("order_desc")
        attachment_path = self.get_argument("attachment_path")
        attachment_name = self.get_argument("attachment_name")
        v_list = upd_order(order_number,order_env,order_type,order_status,order_handle,order_desc,attachment_path,attachment_name)
        v_json = json.dumps(v_list)
        self.write(v_json)

class wtd_delete(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        wtd_no = self.get_argument("wtd_no")
        v_list = delete_order(wtd_no)
        v_json = json.dumps(v_list)
        self.write(v_json)


class wtd_attachment(basehandler):
    @tornado.web.authenticated
    def get(self):
        self.set_header("Content-Type", "text/html; charset=UTF-8")
        userid = str(self.get_secure_cookie("userid"), encoding="utf-8")
        wtd_no = self.get_argument("wtd_no")
        v_list = query_wtd_detail(wtd_no, userid)
        v_attach = []
        for i in  range(len(v_list['attachment_path'].split(','))):
            v_attach.append([i+1,'http://10.2.39.17:8300'+v_list['attachment_path'].split(',')[i]+'/'+v_list['attachment_name'].split(',')[i]])
        self.render("./order_attachment.html", order_attachments=v_attach)

class wtd_attachment_number(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        wtd_no = self.get_argument("wtd_no")
        v_list = get_order_attachment_number(wtd_no)
        v_json = json.dumps(v_list)
        self.write(v_json)

