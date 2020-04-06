#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/10 13:18
# @Author  : 马飞
# @File    : t_sql.py
# @Software: PyCharm

from web.model.t_ds   import get_ds_by_dsid
from web.utils.common import get_connection_ds,get_connection_ds_sqlserver,get_connection_ds_read_limit
from web.utils.common import exception_info_mysql,exception_info_sqlserver,format_mysql_error,format_sqlserver_error
from web.model.t_sql_check import get_audit_rule
import traceback
import pymysql

def check_sql(p_dbid,p_sql,curdb):
    result = {}
    result['status'] = '0'
    result['msg']    = ''
    result['data']   = ''
    result['column'] = ''

    if p_dbid == '':
        result['status'] = '1'
        result['msg'] = '请选择数据源!'
        result['data'] = ''
        result['column'] = ''
        return result

    if p_sql =='':
        result['status'] = '1'
        result['msg'] = '请选中查询语句!'
        result['data'] = ''
        result['column'] = ''
        return result

    if p_sql.find('.')==-1 and curdb=='':
        result['status'] = '1'
        result['msg'] = '请选择数据库!'
        result['data'] = ''
        result['column'] = ''
        return result


    if p_sql.upper().count("ALTER") >= 1 or p_sql.upper().count("DROP") >= 1 \
            or p_sql.upper().count("CREATE") >= 1  or  p_sql.upper().count("GRANT") >= 1 \
              or p_sql.upper().count("REVOKE") >= 1 or p_sql.upper().count("TRUNCATE") >= 1 \
               or p_sql.upper().count("UPDATE") >= 1 or p_sql.upper().count("DELETE") >= 1 \
                 or p_sql.upper().count("INSERT") >= 1:
        result['status'] = '1'
        result['msg']    = '不允许进行DDL、DCL、DML操作!'
        result['data']   = ''
        result['column'] = ''
        return result
    return result

def get_sqlserver_result(p_ds,p_sql):
    result  = {}
    columns = []
    data    = []
    p_env   = ''
    if p_ds['db_env']=='1':
        p_env='PROD'
    if p_ds['db_env']=='2':
        p_env='DEV'

    try:
        db = get_connection_ds_sqlserver(p_ds)
        cr = db.cursor()
        cr.execute(p_sql)
        rs = cr.fetchall()
        desc = cr.description
        for i in range(len(desc)):
            columns.append({"title": desc[i][0]})
        for i in rs:
            tmp = []
            for j in range(len(desc)):
                tmp.append(str(i[j]))
            data.append(tmp)

        result['status'] = '0'
        result['msg'] = ''
        result['data'] = data
        result['column'] = columns
        cr.close()
        db.close()
        return result
    except:
        result['status'] = '1'
        result['msg'] = format_sqlserver_error(p_env,exception_info_sqlserver())
        result['data']   = ''
        result['column'] = ''
        return result

def get_mysql_result(p_ds,p_sql,curdb):
    result   = {}
    columns  = []
    data     = []
    p_env    = ''

    #get read timeout
    read_timeout = int(get_audit_rule('switch_timeout')['rule_value'])
    print('read_timeout=',read_timeout)
    if p_ds['db_env']=='1':
        p_env='PROD'
    if p_ds['db_env']=='2':
        p_env='DEV'

    db=''
    cr=''
    rs=''
    if p_sql.find('.') > 0:
        db = get_connection_ds_read_limit(p_ds,read_timeout)
        cr = db.cursor()
    else:
        p_ds['service'] = curdb
        db = get_connection_ds_read_limit(p_ds,read_timeout)
        cr = db.cursor()

    try:
        cr.execute(p_sql)
        rs = cr.fetchall()

        #get sensitive column
        c_sensitive = get_audit_rule('switch_sensitive_columns')['rule_value'].split(',')

        #process desc
        i_sensitive = []

        desc = cr.description
        for i in range(len(desc)):
            if desc[i][0] in c_sensitive:
                i_sensitive.append(i)
            columns.append({"title": desc[i][0]})
        print('i_sensitive=',i_sensitive)

        #check sql rwos
        rule = get_audit_rule('switch_query_rows')
        if len(rs)>int(rule['rule_value']):
            result['status'] = '1'
            result['msg'] = rule['error'].format(rule['rule_value'])
            result['data'] = ''
            result['column'] = ''
            return result

        #process data
        for i in rs:
            tmp = []
            for j in range(len(desc)):
                if i[j] is None:
                   tmp.append('')
                else:
                   if j in  i_sensitive:
                       tmp.append(get_audit_rule('switch_sensitive_columns')['error'])
                   else:
                       tmp.append(str(i[j]))
            data.append(tmp)

        result['status'] = '0'
        result['msg'] = ''
        result['data'] = data
        result['column'] = columns
        cr.close()
        db.close()
        return result
    except pymysql.err.OperationalError as e:
        err= traceback.format_exc()
        print('get_mysql_result=', err)
        if err.find('timed out')>0:
            rule  = get_audit_rule('switch_timeout')
            result['status'] = '1'
            result['msg'] = rule['error'].format(rule['rule_value'])
            result['data'] = ''
            result['column'] = ''
            return result
        else:
            result['status'] = '1'
            result['msg'] = format_mysql_error(p_env, exception_info_mysql())
            result['data'] = ''
            result['column'] = ''
            return result
    except:
        print('get_mysql_result=',traceback.format_exc())
        result['status'] = '1'
        result['msg'] = format_mysql_error(p_env,exception_info_mysql())
        result['data'] = ''
        result['column'] = ''
        return result

def exe_query(p_dbid,p_sql,curdb):
    result = {}

    # 查询校验
    val = check_sql(p_dbid, p_sql,curdb)
    if val['status'] != '0':
        return val

    p_ds  = get_ds_by_dsid(p_dbid)

    #查询MySQL数据源
    if p_ds['db_type']=='0':
        result=get_mysql_result(p_ds,p_sql,curdb)

    # 查询MSQLServer数据源
    if p_ds['db_type'] == '2':
        result = get_sqlserver_result(p_ds,p_sql)

    return result