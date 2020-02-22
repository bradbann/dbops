#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/30 15:46
# @Author  : 马飞
# @File    : t_user.py
# @Software: PyCharm

from web.utils.common     import exception_info,current_rq,aes_encrypt,aes_decrypt,format_sql
from web.utils.common     import get_connection,get_connection_ds,get_connection_ds_sqlserver,get_connection_ds_oracle,get_connection_ds_pg
from web.model.t_ds       import get_ds_by_dsid
from web.model.t_user     import get_user_by_loginame
import re
import os,json
import traceback

def query_port(app_name):
    db = get_connection()
    cr = db.cursor()
    v_where =''
    if app_name != '':
        v_where = " where a.app_name like '%{0}%'\n".format(app_name)

    sql = """SELECT  a.id,
                 a.app_name,
                 a.app_port,
                 a.app_dev,
                 a.app_desc,
                 a.app_ext
            FROM  t_port a
              {0}
          """.format(v_where)
    print(sql)
    cr.execute(sql)
    v_list = []
    for r in cr.fetchall():
        v_list.append(list(r))
    cr.close()
    db.commit()
    return v_list

def save_port(p_port):
    result = {}

    val=check_port(p_port)
    if val['code']=='-1':
        return val
    try:
        db               = get_connection()
        cr               = db.cursor()
        result           = {}
        app_name         = p_port['app_name']
        app_port         = p_port['app_port']
        app_dev          = p_port['app_dev']
        app_desc         = p_port['app_desc']
        app_ext          = p_port['app_ext']

        sql="""insert into t_port(app_name,app_port,app_dev,app_desc,app_ext) values('{0}','{1}','{2}','{3}','{4}')
            """.format(app_name,app_port,app_dev,app_desc,app_ext)
        print(sql)
        cr.execute(sql)
        cr.close()
        db.commit()
        result['code']='0'
        result['message']='保存成功！'
        return result
    except:
        e_str = exception_info()
        print(e_str)
        result['code'] = '-1'
        result['message'] = '保存失败！'
    return result

def upd_port(p_transfer):
    result={}
    val = check_port(p_transfer)
    if  val['code'] == '-1':
        return val
    try:
        db              = get_connection()
        cr              = db.cursor()
        transfer_id     = p_transfer['transfer_id']
        transfer_tag    = p_transfer['transfer_tag']
        task_desc       = p_transfer['task_desc']
        transfer_server = p_transfer['transfer_server']
        transfer_type   = p_transfer['transfer_type']
        sour_db_server  = p_transfer['sour_db_server']
        sour_db_name    = p_transfer['sour_db_name']
        sour_tab_name   = p_transfer['sour_tab_name']
        sour_tab_where  = p_transfer['sour_tab_where']
        dest_db_server  = p_transfer['dest_db_server']
        dest_db_name    = p_transfer['dest_db_name']
        script_base     = p_transfer['script_base']
        script_name     = p_transfer['script_name']
        python3_home    = p_transfer['python3_home']
        batch_size      = p_transfer['batch_size']
        api_server      = p_transfer['api_server']
        status          = p_transfer['status']

        sql="""update t_db_transfer_config 
                  set  
                      transfer_tag      ='{0}',
                      server_id         ='{1}', 
                      comments          ='{2}', 
                      sour_db_id        ='{3}', 
                      sour_schema       ='{4}',
                      sour_table        ='{5}',
                      sour_where        ='{6}',
                      dest_db_id        ='{7}',
                      dest_schema       ='{8}',                    
                      script_path       ='{9}',
                      script_file       ='{10}',
                      python3_home      ='{11}',
                      api_server        ='{12}',                   
                      status            ='{13}',
                      batch_size        ='{14}',
                      transfer_type     ='{15}'
                where id={16}""".format(transfer_tag,transfer_server,task_desc,sour_db_server,sour_db_name,
                                        sour_tab_name,format_sql(sour_tab_where),dest_db_server,dest_db_name,script_base,
                                        script_name,python3_home,api_server,status,batch_size,transfer_type,transfer_id)
        print(sql)
        cr.execute(sql)
        cr.close()
        db.commit()
        result={}
        result['code']='0'
        result['message']='更新成功！'
    except :
        print(traceback.format_exc())
        result['code'] = '-1'
        result['message'] = '更新失败！'
    return result

def del_port(p_transferid):
    result={}
    try:
        db = get_connection()
        cr = db.cursor()
        sql="delete from t_db_transfer_config  where id='{0}'".format(p_transferid)
        print(sql)
        cr.execute(sql)
        cr.close()
        db.commit()
        result={}
        result['code']='0'
        result['message']='删除成功！'
    except :
        result['code'] = '-1'
        result['message'] = '删除失败！'
    return result

def check_port(p_port):
    result = {}

    if p_port["app_name"]=="":
        result['code']='-1'
        result['message']='应用名不能为空！'
        return result

    if p_port["app_port"] == "":
        result['code'] = '-1'
        result['message'] = '端口号不能为空！'
        return result

    if p_port["app_dev"]=="":
        result['code']='-1'
        result['message']='开发者不能为空！'
        return result

    if p_port["app_desc"]=="":
        result['code']='-1'
        result['message']='应用描述不能为空！'
        return result


    result['code'] = '0'
    result['message'] = '验证通过'
    return result

def get_port_by_portid(p_transferid):
    db = get_connection()
    cr = db.cursor()
    sql = """select   id,transfer_tag,server_id,comments,sour_db_id,sour_schema,
                      sour_table,sour_where,dest_db_id,dest_schema,script_path,
                      script_file,python3_home,api_server,status,batch_size,transfer_type
             from t_db_transfer_config where id={0}
          """.format(p_transferid)
    cr.execute(sql)
    rs = cr.fetchall()
    d_port = {}
    d_port['server_id']      = rs[0][0]
    d_port['transfer_tag']   = rs[0][1]
    d_port['server_id']      = rs[0][2]
    d_port['task_desc']      = rs[0][3]
    d_port['sour_db_id']     = rs[0][4]
    d_port['sour_schema']    = rs[0][5]
    d_port['sour_table']     = rs[0][6]
    cr.close()
    db.commit()
    print(d_port)
    return d_port