#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/10 13:18
# @Author  : 马飞
# @File    : t_sql.py
# @Software: PyCharm

import traceback,re
import sqlparse
from web.utils.common           import current_time,format_sql
from web.model.t_ds             import get_ds_by_dsid
from web.model.t_sql_check      import  check_mysql_ddl
from web.utils.common           import get_connection_ds,get_connection,get_connection_dict,get_connection_ds_write_limit
from web.model.t_sql_check      import get_audit_rule

def get_sqlid():
    db = get_connection()
    cr = db.cursor()
    sql="select ifnull(max(id),0)+1 from t_sql_release"
    cr.execute(sql)
    rs = cr.fetchone()
    cr.close()
    db.commit()
    return rs[0]

def get_sql_by_sqlid(p_sql_id):
    db = get_connection()
    cr = db.cursor()
    sql="select sqltext from t_sql_release where id={0}".format(p_sql_id)
    cr.execute(sql)
    rs = cr.fetchone()
    cr.close()
    db.commit()
    return rs[0]

def query_audit(p_name,p_dsid,p_ver,p_userid):
    db = get_connection()
    cr = db.cursor()
    v_where = ''
    if p_name != '':
       v_where = v_where + " and a.sqltext like '%{0}%'\n".format(p_name)

    if p_dsid != '':
        v_where = v_where + " and a.dbid='{0}'\n".format(p_dsid)
    else:
        v_where = v_where + """ and exists(select 1 from t_user_proj_privs x 
                                           where x.proj_id=b.id and x.user_id='{0}' and priv_id='3')""".format(p_userid)

    if p_ver != '':
        v_where = v_where + " and a.version='{0}'\n".format(p_ver)


    sql = """SELECT  a.id, 
                     a.message,
                     CASE a.status WHEN '0' THEN '已发布'
                       WHEN '1' THEN '已审核'
                       WHEN '2' THEN '审核失败'
                       WHEN '3' THEN '已执行'
                       WHEN '4' THEN '执行失败'
                     END  STATUS,
                     c.dmmc AS 'type',
                     b.db_desc,
                     e.dmmc, 
                     d.name AS creator,
                     DATE_FORMAT(a.creation_date,'%Y-%m-%d %h:%i:%s')  creation_date,
                     (SELECT NAME FROM t_user e WHERE e.id=a.auditor) auditor,
                     DATE_FORMAT(a.audit_date,'%y-%m-%d %h:%i:%s')   audit_date   
            FROM t_sql_release a,t_db_source b,t_dmmx c,t_user d,t_dmmx e
            WHERE a.dbid=b.id
              AND a.version=e.dmm
              AND c.dm='13'
              AND e.dm='12'  
              AND a.type=c.dmm
              AND a.creator=d.id
              {0}
            order by creation_date desc
          """.format(v_where)
    print(sql)
    cr.execute(sql)
    v_list = []
    for r in cr.fetchall():
        v_list.append(list(r))
    cr.close()
    db.commit()
    print(v_list)
    return v_list

def query_run(p_name,p_dsid,p_ver,p_userid):
    db = get_connection()
    cr = db.cursor()
    v_where = ''
    if p_name != '':
       v_where = v_where + " and a.sqltext like '%{0}%'\n".format(p_name)

    if p_dsid != '':
        v_where = v_where + " and a.dbid='{0}'\n".format(p_dsid)
    else:
        v_where = v_where + """ and exists(select 1 from t_user_proj_privs x 
                                   where x.proj_id=b.id and x.user_id='{0}' and priv_id='4')""".format(p_userid)

    if p_ver != '':
        v_where = v_where + " and a.version='{0}'\n".format(p_ver)


    sql = """SELECT  a.id, 
                     a.message,
                     CASE a.status WHEN '0' THEN '已发布'
                       WHEN '1' THEN '已审核'
                       WHEN '2' THEN '审核失败'
                       WHEN '3' THEN '已执行'
                       WHEN '4' THEN '执行失败'
                     END  STATUS,
                     c.dmmc AS 'type',
                     b.db_desc,
                     e.dmmc,
                     d.name AS creator,
                     DATE_FORMAT(a.creation_date,'%Y-%m-%d %h:%i:%s')  creation_date,
                     (SELECT NAME FROM t_user e WHERE e.id=a.auditor) auditor,
                     DATE_FORMAT(a.audit_date,'%y-%m-%d %h:%i:%s')   audit_date,
                     error   
            FROM t_sql_release a,t_db_source b,t_dmmx c,t_user d,t_dmmx e
            WHERE a.dbid=b.id
              AND a.version=e.dmm
              AND c.dm='13'
              AND e.dm='12' 
              AND a.type=c.dmm
              AND a.creator=d.id  
              {0}
            order by creation_date desc
          """.format(v_where)
    print('query_run=',sql)
    cr.execute(sql)
    v_list = []
    for r in cr.fetchall():
        v_list.append(list(r))
    cr.close()
    db.commit()
    print(v_list)
    return v_list

def query_order(p_name,p_dsid,p_ver,p_userid):
    db = get_connection()
    cr = db.cursor()
    v_where = "  and ( a.creator='{0}' or a.auditor='{1}' or a.executor='{2}' )".format(p_userid,p_userid,p_userid)
    if p_name != '':
       v_where = v_where + " and a.sqltext like '%{0}%'\n".format(p_name)

    if p_dsid != '':
        v_where = v_where + " and a.dbid='{0}'\n".format(p_dsid)

    if p_ver != '':
        v_where = v_where + " and a.version='{0}'\n".format(p_ver)


    sql = """SELECT  a.id, 
                     a.message,
                     CASE a.status WHEN '0' THEN '已发布'
                       WHEN '1' THEN '已审核'
                       WHEN '2' THEN '审核失败'
                       WHEN '3' THEN '已执行'
                       WHEN '4' THEN '执行失败'
                     END  STATUS,
                     c.dmmc AS 'type',
                     b.db_desc,
                     e.dmmc,
                     d.name AS creator,
                     DATE_FORMAT(a.creation_date,'%Y-%m-%d %h:%i:%s')  creation_date,
                     (SELECT NAME FROM t_user e WHERE e.id=a.auditor) auditor,
                     DATE_FORMAT(a.audit_date,'%y-%m-%d %h:%i:%s')   audit_date,
                     error
            FROM t_sql_release a,t_db_source b,t_dmmx c,t_user d,t_dmmx e
            WHERE a.dbid=b.id
              and a.version=e.dmm
              AND c.dm='13'
              and e.dm='12'
              AND a.type=c.dmm
              AND a.creator=d.id
              {0}
            order by creation_date desc
          """.format(v_where)
    print(sql)
    cr.execute(sql)
    v_list = []
    for r in cr.fetchall():
        v_list.append(list(r))
    cr.close()
    db.commit()
    print(v_list)
    return v_list

def query_wtd(p_userid):
    db  = get_connection()
    cr  = db.cursor()
    sql = """SELECT 
                 order_no,
                 (SELECT db_desc FROM t_db_source WHERE  id=a.order_env) AS order_env,
                 (SELECT dmmc FROM t_dmmx WHERE dm='17' AND dmm=a.order_type) AS order_type,
                 (SELECT dmmc FROM t_dmmx WHERE dm='19' AND dmm=a.order_status) AS order_status,                
                 (SELECT NAME FROM t_user WHERE id=a.creator) AS creator,
                 date_format(a.create_date,'%Y-%m-%d') as  create_date,
                 (SELECT NAME FROM t_user WHERE id=a.order_handler) AS order_handler,
                 date_format(a.handler_date,'%Y-%m-%d') as  handler_date                
           FROM t_wtd a
           where a.creator='{0}' or a.order_handler='{1}'
          """.format(p_userid,p_userid)
    print(sql)
    cr.execute(sql)
    v_list = []
    for r in cr.fetchall():
        v_list.append(list(r))
    cr.close()
    db.commit()
    print(v_list)
    return v_list


def get_order_attachment_number(p_wtd_no):
    db  = get_connection()
    cr  = db.cursor()
    sql = """SELECT  attachment_path FROM t_wtd a where order_no='{0}'""".format(p_wtd_no)
    print(sql)
    cr.execute(sql)
    rs=cr.fetchone()
    cr.close()
    db.commit()
    print(rs)
    if rs is None or rs == (None,) or rs ==('',):
       return 0
    else:
       print('get_order_attachment_number=',rs,rs[0])
       return rs[0].count(',')+1


def query_wtd_detail(p_wtd_no,p_userid):
    db  = get_connection_dict()
    cr  = db.cursor()
    sql = """SELECT 
                 order_no,
                 order_env,
                 order_type,
                 order_status,                
                 creator,
                 date_format(a.create_date,'%Y-%m-%d') as  create_date,
                 order_handler,
                 date_format(a.handler_date,'%Y-%m-%d') as  handler_date,
                 (SELECT db_desc FROM t_db_source WHERE id=a.order_env) AS order_env_name,
                 (SELECT dmmc FROM t_dmmx WHERE dm='17' AND dmm=a.order_type) AS order_type_name,
                 (SELECT dmmc FROM t_dmmx WHERE dm='19' AND dmm=a.order_status) AS order_status_name,                
                 (SELECT NAME FROM t_user WHERE id=a.creator) AS creator_name,
                 (SELECT NAME FROM t_user WHERE id=a.order_handler) AS order_handler_name,             
                 order_desc,
                 attachment_path,
                 attachment_name,
                 '{0}' as curr_user
                FROM t_wtd a where order_no='{1}'
          """.format(p_userid,p_wtd_no)
    print(sql)
    cr.execute(sql)
    rs=cr.fetchone()
    cr.close()
    db.commit()
    print(rs)
    return rs


def query_order_no():
    db = get_connection()
    cr = db.cursor()
    cr.execute('''
                SELECT 
                   CASE WHEN (COUNT(0)+1)<10 THEN 
                      CONCAT('0',CAST(COUNT(0)+1 AS CHAR))
                   ELSE
                      CAST(COUNT(0)+1 AS CHAR)
                   END AS order_no   
               FROM t_wtd FOR UPDATE
               ''')
    rs=cr.fetchone()
    cr.close()
    db.commit()
    return rs[0]


def save_order(order_number,order_env,order_type,order_status,order_handle,order_desc,p_user,p_attachment_path,p_attachment_name):
    result = {}
    try:
        db = get_connection()
        cr = db.cursor()
        sql = '''insert into t_wtd(order_no,order_env,order_type,order_status,order_handler,order_desc,creator,create_date,attachment_path,attachment_name)
                  values('{0}','{1}','{2}','{3}','{4}','{5}','{6}',now(),'{7}','{8}')
              '''.format(order_number,order_env,order_type,order_status,order_handle,order_desc,p_user,p_attachment_path,p_attachment_name)
        print('save_order=',sql)
        cr.execute(sql)
        cr.close()
        db.commit()
        result['code']='0'
        result['message']='保存成功!'
        return result
    except Exception as e:
        print(e)
        result['code'] = '-1'
        result['message'] = '保存失败!'
        return result

def upd_order(order_number, order_env, order_type, order_status,
              order_handler, order_desc, p_attachment_path, p_attachment_name):
    result = {}
    try:
        db = get_connection()
        cr = db.cursor()
        sql = '''update t_wtd set                     
                      order_env          = '{0}',
                      order_type         = '{1}',
                      order_status       = '{2}',
                      order_handler      = '{3}',
                      order_desc         = '{4}',
                      attachment_path    = '{5}',
                      attachment_name    = '{6}'
                 where order_no ='{7}'
              '''.format(order_env, order_type, order_status, order_handler, order_desc,
                         p_attachment_path, p_attachment_name,order_number)
        print('upd_order=', sql)
        cr.execute(sql)
        cr.close()
        db.commit()
        result['code'] = '0'
        result['message'] = '更新成功!'
        return result
    except Exception as e:
        print(traceback.format_exc())
        result['code'] = '-1'
        result['message'] = '更新失败!'
        return result


def delete_order(order_number):
    result = {}
    try:
        db = get_connection()
        cr = db.cursor()
        sql = "delete from t_wtd  where order_no='{0}'".format(order_number)
        print('delete_order=',sql)
        cr.execute(sql)
        cr.close()
        db.commit()
        result['code']='0'
        result['message']='删除成功!'
        return result
    except Exception as e:
        print(traceback.print_exc())
        result['code'] = '-1'
        result['message'] = '删除失败!'
        return result


def release_order(p_order_no):
    result = {}
    try:
        db = get_connection()
        cr = db.cursor()
        sql = """update t_wtd set order_status='2' where order_no='{0}'""".format(p_order_no)
        print('release_order=',sql)
        cr.execute(sql)
        cr.close()
        db.commit()
        result['code']='0'
        result['message']='发布成功!'
        return result
    except Exception as e:
        print(e)
        result['code'] = '-1'
        result['message'] = '发布失败!'
        return result

def query_audit_sql(id):
    db = get_connection()
    cr = db.cursor()
    sql = """select a.sqltext from t_sql_release a  where a.id={0}""".format(id)
    print(sql)
    cr.execute(sql)
    rs=cr.fetchone()
    cr.close()
    db.commit()
    print(rs[0])
    result = {}
    result['code'] = '0'
    result['message'] = rs[0]
    return result


def save_sql(p_dbid,p_sql,desc,logon_user):
    result = {}
    try:
        db   = get_connection()
        cr   = db.cursor()

        #发布校验
        if p_dbid == '':
            result['code'] = '1'
            result['message'] = '请选择数据源!'
            return result

        p_ds = get_ds_by_dsid(p_dbid)
        if p_ds['db_type'] == '0':
            val = check_mysql_ddl(p_dbid, p_sql,logon_user)

        if val['code']!='0':
           return val

        sql="""insert into t_sql_release(id,dbid,sqltext,status,message,creation_date,creator,last_update_date,updator) 
                values('{0}','{1}',"{2}",'{3}','{4}','{5}','{6}','{7}','{8}')""".format(get_sqlid(),p_dbid,p_sql,'0',desc,current_time(),'DBA',current_time(),'DBA');
        print(sql)
        cr.execute(sql)
        cr.close()
        db.commit()
        db.close()
        result={}
        result['code']='0'
        result['message']='发布成功！'
        return result
    except:
        e_str = traceback.format_exc()
        print(e_str)
        result['code'] = '-1'
        result['message'] = '发布失败！'+e_str
    return result


def check_sql(p_dbid,p_cdb,p_sql,desc,logon_user,type):
    result = {}
    result['code'] = '0'
    result['message'] = '发布成功！'
    try:
        if p_dbid == '':
            result['code'] = '1'
            result['message'] = '请选择数据源!'
            return result

        p_ds = get_ds_by_dsid(p_dbid)
        if p_ds['db_type'] == '0':
            val = check_mysql_ddl(p_dbid,p_cdb, p_sql,logon_user,type)

        if val == False:
            result['code'] = '1'
            result['message'] = '发布失败!'
            return result
        return result
    except:
        e_str = traceback.format_exc()
        print(e_str)
        result['code'] = '-1'
        result['message'] = '发布失败！'+e_str
        return result

def save_sql(p_dbid,p_cdb,p_sql,desc,p_user,ver,type):
    result = {}
    try:
        # #get write timeout
        # write_timeout = int(get_audit_rule('switch_ddl_timeout')['rule_value'])
        # print('write_timeout=', write_timeout)

        db   = get_connection()
        cr   = db.cursor()

        if check_validate(p_dbid,p_cdb,p_sql,desc,p_user,type)['code']!='0':
           return  check_validate(p_dbid,p_cdb,p_sql,desc,p_user,ver,type)

        p_ds = get_ds_by_dsid(p_dbid)
        if p_ds['db_type'] == '0':
            val = check_mysql_ddl(p_dbid,p_cdb, p_sql,p_user,type)

        if val == False:
            result['code'] = '1'
            result['message'] = '发布失败!'
            return result

        sql="""insert into t_sql_release(id,dbid,sqltext,status,message,creation_date,creator,last_update_date,updator,version,type) 
                values('{0}','{1}',"{2}",'{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}')
            """.format(get_sqlid(),p_dbid,p_sql,'0',desc,current_time(),p_user['userid'],current_time(),p_user['userid'],ver,type);
        print(sql)

        cr.execute(sql)
        cr.close()
        db.commit()
        db.close()
        result={}
        result['code']='0'
        result['message']='发布成功！'
        return result
    except:
        e_str = traceback.format_exc()
        print(e_str)
        result['code'] = '-1'
        result['message'] = '发布失败！'+e_str
    return result


def upd_sql(p_sqlid,d_user):
    result={}
    try:
        db = get_connection()
        cr = db.cursor()
        sql="""update t_sql_release 
                  set  status ='1' ,
                       last_update_date ='{0}' ,
                       updator='{1}',
                       audit_date ='{2}' ,
                       auditor='{3}'
                where id='{4}'""".format(current_time(),d_user['userid'],current_time(),d_user['userid'],p_sqlid)
        print(sql)
        cr.execute(sql)
        cr.close()
        db.commit()
        result={}
        result['code']='0'
        result['message']='审核成功！'
    except :
        db = get_connection()
        cr = db.cursor()
        sql = """update t_sql_release 
                         set  status ='2' ,
                              last_update_date ='{0}' ,
                              updator='{1}',
                              audit_date ='{2}' ,
                              auditor='{3}'
                       where id='{4}'""".format(current_time(), d_user['userid'], current_time(),
                                                d_user['userid'], p_sqlid)
        print(sql)
        cr.execute(sql)
        cr.close()
        db.commit()
        result['code'] = '-1'
        result['message'] = '审核失败！'
    return result


def upd_run_status(p_sqlid,p_user,p_flag,p_err=None):
    try:
        db = get_connection()
        cr = db.cursor()
        sql= ''
        if p_flag == 'before':
            sql = """update t_sql_release 
                      set  status ='3' ,
                           last_update_date ='{0}' ,
                           executor = '{1}',
                           exec_start ='{2}'                    
                    where id='{3}'""".format(current_time(),p_user['loginname'],current_time(),str(p_sqlid))
        elif p_flag =='after':
            sql = """update t_sql_release 
                        set last_update_date ='{0}' ,
                            exec_end ='{1}'                    
                        where id='{2}'""".format(current_time(), current_time(), str(p_sqlid))
        else:
            sql = """update t_sql_release 
                        set  status ='4' ,
                             last_update_date ='{0}' ,
                             exec_end ='{1}',
                             error = '{2}'                    
                        where id='{3}'""".format(current_time(), current_time(), p_err,str(p_sqlid))
        print('upd_run_status=',sql)
        cr.execute(sql)
        cr.close()
        db.commit()

    except Exception as e:
        print(traceback.format_exc())

# def exe_sql(p_dbid,p_sql):
#     result   ={}
#     try:
#         p_ds = get_ds_by_dsid(p_dbid)
#         db   = get_connection_ds(p_ds)
#         cr = db.cursor()
#         cr.execute(p_sql)
#         db.commit()
#         cr.close()
#         result['code'] = '0'
#         result['message'] = '发布成功！'
#         return result
#     except:
#         result['code'] = '-1'
#         result['message'] = '发布失败！'
#         return result

def exe_sql(p_dbid, p_db_name,p_sql_id,p_user):
    result = {}
    try:
        upd_run_status(p_sql_id,p_user,'before')
        p_ds = get_ds_by_dsid(p_dbid)
        p_ds['service'] = p_db_name
        db  = get_connection_ds(p_ds)
        sql = get_sql_by_sqlid(p_sql_id)
        cr  = db.cursor()
        cr.execute(sql)
        db.commit()
        cr.close()
        upd_run_status(p_sql_id, p_user, 'after')
        result['code'] = '0'
        result['message'] = '执行成功!'
        return result
    except Exception as e:
        error = str(e).split(',')[1][:-1].replace("\\","\\\\").replace("'","\\'").replace('"','')+'!'
        print('exe_sql=',error)
        result['code'] = '-1'
        result['message'] = '执行失败!{}'.format(error)
        upd_run_status(p_sql_id, p_user, 'error', error)
        return result


def check_validate(p_dbid,p_cdb,p_sql,desc,logon_user,type):
    result = {}
    result['code'] = '0'
    result['message'] = '发布成功！'

    if p_dbid == '':
       result['code'] = '1'
       result['message'] = '请选择数据源!'
       return result

    if p_cdb == '':
       result['code'] = '1'
       result['message'] = '当前数据库不能为空!'
       return result

    if desc == '':
       result['code'] = '1'
       result['message'] = '请输入工单描述!'
       return result

    if type == '':
       result['code'] = '1'
       result['message'] = '工单类型不能为空!'
       return result

    return result

def format_sql(p_sql):
    result = {}
    result['code'] = '0'
    v_sql_list=sqlparse.split(p_sql)
    v_ret=''
    for v in v_sql_list:
        v_sql = sqlparse.format(v, reindent=True, keyword_case='upper')

        if v_sql.upper().count('CREATE') > 0 or v_sql.upper().count('ALTER') > 0:
            v_tmp = re.sub(' {5,}', '  ', v_sql).strip()
        else:
            v_tmp = re.sub('\n{2,}', '\n\n', v_sql).strip(' ')

        v_ret=v_ret+v_tmp+'\n\n'

    result['message'] = v_ret[0:-2]

    return result