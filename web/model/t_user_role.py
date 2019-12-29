#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/3 15:46
# @Author  : 马飞
# @File    : t_user.py
# @Software: PyCharm

import traceback
from web.utils.common import current_rq
from web.utils.common import get_connection

def get_roles_by_userid(p_userid):
    db = get_connection()
    cr = db.cursor()
    sql="select cast(role_id as char) as role_id from t_user_role where user_id={0}".format(p_userid)
    cr.execute(sql)
    rs = cr.fetchall()
    cr.close()
    db.commit()
    return rs

def save_user_role(p_userid,p_roles):
    result = {}
    try:
        db = get_connection()
        cr = db.cursor()
        for role in range(len(p_roles)):
          sql="insert into t_user_role(user_id,role_id) values({0},{1})".format(p_userid,p_roles[role]);
          print(sql)
          cr.execute(sql)
        cr.close()
        db.commit()
        result['code']='0'
        result['message']='保存成功！'
        return result
    except:
        result['code'] = '-1'
        result['message'] = '保存失败！'
    return result


def upd_user_role(p_userid,p_roles):
    result={}
    try:
        db = get_connection()
        cr = db.cursor()
        del_user_roles(p_userid);
        save_user_role(p_userid,p_roles)
        result['code']='0'
        result['message']='更新成功！'
    except :
        result['code'] = '-1'
        result['message'] = '更新失败！'
    return result


def del_user_roles(p_userid):
    result = {}
    try:
        db = get_connection()
        cr = db.cursor()
        sql = "delete from t_user_role where user_id='{0}'".format(p_userid);
        print(sql)
        cr.execute(sql)
        cr.close()
        db.commit()
        result = {}
        result['code'] = '0'
        result['message'] = '删除成功！'
        return result
    except:
        result['code'] = '-1'
        result['message'] = '删除失败！'
    return result

