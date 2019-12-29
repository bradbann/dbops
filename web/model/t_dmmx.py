#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2018/7/17 9:35
# @Author : 马飞
# @File : t_dmmx.py
# @Software: PyCharm

from web.utils.common import get_connection,get_connection_ds
#from web.model.t_ds import get_ds_by_dsid

def get_dmm_from_dm(p_dm):
    db = get_connection()
    cr = db.cursor()
    sql = "select dmm,dmmc from t_dmmx where dm='{0}'".format(p_dm)
    print(sql)
    cr.execute(sql)
    v_list = []
    for r in cr.fetchall():
        v_list.append(list(r))
    cr.close()
    return v_list

def get_dmmc_from_dm(p_dm,p_dmm):
    db = get_connection()
    cr = db.cursor()
    sql = "select dmmc from t_dmmx where dm='{0}' and dmm={1}".format(p_dm,p_dmm)
    print(sql)
    cr.execute(sql)
    rs=cr.fetchone()
    cr.close()
    return rs[0]


def get_backup_server():
    db = get_connection()
    cr = db.cursor()
    sql = "select id,server_desc from t_server WHERE server_type=1 order by market_id"
    print(sql)
    cr.execute(sql)
    v_list = []
    for r in cr.fetchall():
        v_list.append(list(r))
    cr.close()
    return v_list

def get_sync_server():
    db = get_connection()
    cr = db.cursor()
    sql = "select id,server_desc from t_server WHERE server_type=2 order by market_id"
    print(sql)
    cr.execute(sql)
    v_list = []
    for r in cr.fetchall():
        v_list.append(list(r))
    cr.close()
    return v_list

def get_db_server():
    db = get_connection()
    cr = db.cursor()
    sql = "SELECT id,db_desc FROM t_db_source WHERE  db_type in(0,4,5,6) AND STATUS=1 ORDER BY id"
    print(sql)
    cr.execute(sql)
    v_list = []
    for r in cr.fetchall():
        v_list.append(list(r))
    cr.close()
    return v_list

def get_db_backup_server():
    db = get_connection()
    cr = db.cursor()
    sql = """SELECT id,db_desc FROM t_db_source 
             WHERE  (db_type in(0)  and user in('puppet','easylife') or db_type not in (0,2))
                and STATUS=1 ORDER BY db_desc,db_type
          """
    print(sql)
    cr.execute(sql)
    v_list = []
    for r in cr.fetchall():
        v_list.append(list(r))
    cr.close()
    return v_list

def get_db_backup_tags():
    db = get_connection()
    cr = db.cursor()
    sql = """SELECT db_tag,comments FROM t_db_config  WHERE STATUS=1  ORDER BY db_type,db_id 
          """
    print(sql)
    cr.execute(sql)
    v_list = []
    for r in cr.fetchall():
        v_list.append(list(r))
    cr.close()
    return v_list

def get_db_sync_tags():
    db = get_connection()
    cr = db.cursor()
    sql = """SELECT sync_tag,comments FROM t_db_sync_config  WHERE STATUS=1  ORDER BY sync_col_val,comments 
          """
    print(sql)
    cr.execute(sql)
    v_list = []
    for r in cr.fetchall():
        v_list.append(list(r))
    cr.close()
    return v_list


def get_db_sync_tags_by_market_id(market_id):
    db = get_connection()
    cr = db.cursor()
    if market_id=='':
        sql = """SELECT sync_tag,comments FROM t_db_sync_config  WHERE STATUS=1   ORDER BY sync_col_val,comments"""
    else:
        sql = """SELECT sync_tag,comments FROM t_db_sync_config  WHERE STATUS=1  and sync_col_val='{0}' ORDER BY sync_col_val,comments 
              """.format(market_id)
    print(sql)
    cr.execute(sql)
    v_list = []
    for r in cr.fetchall():
        v_list.append(list(r))
    cr.close()
    return v_list

def get_db_sync_ywlx_by_market_id(market_id):
    db = get_connection()
    cr = db.cursor()
    if market_id=='':
        sql = """SELECT dmm,dmmc FROM t_dmmx WHERE dm='08' ORDER BY dmm """
    else:
        sql = """SELECT a.dmm,a.dmmc FROM t_dmmx a 
                 WHERE dm='08' 
                   AND EXISTS(SELECT 1 FROM t_db_sync_config b
                               WHERE b.status='1'
                                 AND b.sync_ywlx=a.dmm
                                 AND b.sync_col_val='{0}')
                 ORDER BY a.dmm 
              """.format(market_id)
    print(sql)
    cr.execute(sql)
    v_list = []
    for r in cr.fetchall():
        v_list.append(list(r))
    cr.close()
    return v_list


def get_db_sync_ywlx():
    db = get_connection()
    cr = db.cursor()
    sql = """SELECT dmm,dmmc FROM t_dmmx WHERE dm='08' ORDER BY dmm 
          """
    print(sql)
    cr.execute(sql)
    v_list = []
    for r in cr.fetchall():
        v_list.append(list(r))
    cr.close()
    return v_list


def get_db_backup_tags_by_env_type(p_env,p_type):
    db = get_connection()
    cr = db.cursor()
    v_where = ''
    if p_type != '':
        v_where=v_where+" and c.db_type='{0}'\n".format(p_type)

    if p_env != '':
        v_where=v_where+" and c.db_env='{0}'\n".format(p_env)

    sql = """SELECT a.db_tag,a.comments
             FROM t_db_config a ,t_server b,t_db_source c
               WHERE a.STATUS=1 AND a.server_id=b.id AND a.db_id=c.id
               {0}
             ORDER BY c.db_type,a.db_id
          """.format(v_where)
    print(sql)
    cr.execute(sql)
    v_list = []
    for r in cr.fetchall():
        v_list.append(list(r))
    cr.close()
    return v_list


def get_sync_db_server():
    db = get_connection()
    cr = db.cursor()
    sql = """SELECT id,db_desc
              FROM t_db_source 
            WHERE  db_type in(0,2,6) and db_env in(1,2,3,4) 
                and STATUS=1 
                and user!='puppet'
              ORDER BY db_desc,db_type"""
    print(sql)
    cr.execute(sql)
    v_list = []
    for r in cr.fetchall():
        v_list.append(list(r))
    cr.close()
    return v_list