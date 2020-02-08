#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/10 13:18
# @Author  : 马飞
# @File    : t_sql.py
# @Software: PyCharm

import traceback,re
import sqlparse
from web.utils.common           import current_time
from web.model.t_ds             import get_ds_by_dsid
from web.model.t_sql_check      import  check_mysql_ddl
from web.utils.common           import get_connection_ds,get_connection


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

def query_audit(p_name):
    db = get_connection()
    cr = db.cursor()
    v_where = ' and  1=1 '
    if p_name != '':
        v_where = v_where + " a.sqltext like '%{0}%'\n".format(p_name)

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
                     d.name AS creator,
                     DATE_FORMAT(a.creation_date,'%Y-%m-%d %h:%i:%s')  creation_date,
                     (SELECT NAME FROM t_user e WHERE e.login_name=a.auditor) auditor,
                     DATE_FORMAT(a.audit_date,'%y-%m-%d %h:%i:%s')   audit_date   
            FROM t_sql_release a,t_db_source b,t_dmmx c,t_user d
            WHERE a.dbid=b.id
              AND c.dm='13'
              AND a.type=c.dmm
              AND a.creator=d.login_name
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
            val = check_mysql_ddl(p_dbid,p_cdb, p_sql,logon_user)

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
        db   = get_connection()
        cr   = db.cursor()

        if check_validate(p_dbid,p_cdb,p_sql,desc,p_user,type)['code']!='0':
           return  check_validate(p_dbid,p_cdb,p_sql,desc,p_user,ver,type)

        p_ds = get_ds_by_dsid(p_dbid)
        if p_ds['db_type'] == '0':
            val = check_mysql_ddl(p_dbid,p_cdb, p_sql,p_user)

        if val == False:
            result['code'] = '1'
            result['message'] = '发布失败!'
            return result

        sql="""insert into t_sql_release(id,dbid,sqltext,status,message,creation_date,creator,last_update_date,updator,version,type) 
                values('{0}','{1}',"{2}",'{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}')
            """.format(get_sqlid(),p_dbid,p_sql,'0',desc,current_time(),p_user['loginname'],current_time(),p_user['loginname'],ver,type);
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
                where id='{4}'""".format(current_time(),d_user['loginname'],current_time(),d_user['loginname'],p_sqlid)
        print(sql)
        cr.execute(sql)
        cr.close()
        db.commit()
        result={}
        result['code']='0'
        result['message']='审核成功！'
    except :
        result['code'] = '-1'
        result['message'] = '审核失败！'
    return result


def run_sql(p_sqlid):
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
                where id='{4}'""".format(current_time(),'DBA',current_time(),'DBA',p_sqlid)
        print(sql)
        cr.execute(sql)
        cr.close()
        db.commit()
        result={}
        result['code']='0'
        result['message']='审核成功！'
    except :
        result['code'] = '-1'
        result['message'] = '审核失败！'
    return result


def exe_sql(p_dbid,p_sql):
    result   ={}
    try:
        p_ds = get_ds_by_dsid(p_dbid)
        db   = get_connection_ds(p_ds)
        cr = db.cursor()
        cr.execute(p_sql)
        db.commit()
        cr.close()
        result['code'] = '0'
        result['message'] = '发布成功！'
        return result
    except:
        result['code'] = '-1'
        result['message'] = '发布失败！'
        return result

def exe_sql(p_dbid, p_db_name, p_sql_id):
    result = {}
    try:
        p_ds = get_ds_by_dsid(p_dbid)
        p_ds['service'] = p_db_name
        db = get_connection_ds(p_ds)
        sql = get_sql_by_sqlid(p_sql_id)
        cr = db.cursor()
        cr.execute(sql)
        db.commit()
        cr.close()
        result['code'] = '0'
        result['message'] = '执行成功！'
        return result
    except Exception as e:
        result['code'] = '-1'
        result['message'] = '执行失败！ {}'.format(str(e).split(',')[1][:-1])
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