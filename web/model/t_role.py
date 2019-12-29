#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/30 15:46
# @Author  : 马飞
# @File    : t_user.py
# @Software: PyCharm

import traceback
from web.utils.common import current_rq
from web.utils.common import get_connection
from web.model.t_role_privs import save_role_privs,upd_role_privs,del_role_privs

def init_role():
    db = get_connection()
    cr = db.cursor()
    sql = """select id,name,
                 case status when '1' then '是'
                             when '0' then '否'
                 end  status,
                 creator,date_format(creation_date,'%Y-%m-%d')    creation_date,
                 updator,date_format(last_update_date,'%Y-%m-%d') last_update_date           
              from t_role  order by name"""
    cr.execute(sql)
    print('查询成功！')
    v_list = []
    for r in cr.fetchall():
        v_list.append(list(r))
    cr.close()
    cr.close()
    db.commit()
    return v_list


def query_role(p_name):
    db = get_connection()
    cr = db.cursor()
    if p_name == "":
        sql = """select id,name,
                     case status when '1' then '是'
                                 when '0' then '否'
                     end  status,
                     creator,date_format(creation_date,'%Y-%m-%d')    creation_date,
                     updator,date_format(last_update_date,'%Y-%m-%d') last_update_date 
                 from t_role
                 order by name""".format(p_name)
    else:
        sql = """select id,name,
                     case status when '1' then '是'
                                 when '0' then '否'
                     end  status,
                     creator,date_format(creation_date,'%Y-%m-%d')    creation_date,
                     updator,date_format(last_update_date,'%Y-%m-%d') last_update_date 
                 from t_role 
                where binary name like '%{0}%'              
                 order by name""".format(p_name)
    print(sql)
    cr.execute(sql)
    v_list = []
    for r in cr.fetchall():
        v_list.append(list(r))
    cr.close()
    db.commit()
    return v_list


def get_roleid():
    db = get_connection()
    cr = db.cursor()
    sql="select ifnull(max(id),0)+1 from t_role"
    cr.execute(sql)
    rs = cr.fetchone()
    cr.close()
    db.commit()
    return rs[0]

def get_role_by_roleid(p_roleid):
    db = get_connection()
    cr = db.cursor()
    sql="select cast(id as char) as id,name,status,creation_date,creator,last_update_date,updator from t_role where id={0}".format(p_roleid)
    print(sql)
    cr.execute(sql)
    rs = cr.fetchall()
    cr.close()
    db.commit()
    d_role={}
    d_role['roleid']  =str(rs[0][0])
    d_role['name']    = rs[0][1]
    d_role['status']  = rs[0][2]
    return d_role

def get_roles():
    db = get_connection()
    cr = db.cursor()
    sql="select cast(id as char) as id,name from t_role where status='1'"
    print(sql)
    cr.execute(sql)
    v_list = []
    for r in cr.fetchall():
        v_list.append(list(r))
    cr.close()
    db.commit()
    return v_list


def if_exists_role(p_name):
    db = get_connection()
    cr = db.cursor()
    sql="select count(0) from t_role where upper(name)='{0}'".format(p_name.upper())
    cr.execute(sql)
    rs = cr.fetchone()
    cr.close()
    if rs[0]==0:
        return False
    else:
        return True

def is_dba(p_user):
    print("p_user=",p_user,type(p_user))
    db = get_connection()
    cr = db.cursor()
    sql = """SELECT COUNT(0)
              FROM t_role
             WHERE STATUS='1'
               AND id  IN(SELECT role_id FROM t_user_role WHERE user_id='{0}')
               AND NAME='数据库管理员'""".format(p_user['userid'])
    cr.execute(sql)
    rs = cr.fetchone()
    cr.close()
    if rs[0] == 0:
        return False;
    else:
        return True



def save_role(p_role):
    result = {}
    try:
        db        = get_connection()
        cr        = db.cursor()
        role_id   = get_roleid()
        role_name = p_role['name']
        status    = p_role['status']
        privs     = p_role['privs']

        print('privs=',privs)

        sql="""insert into t_role(id,name,status,creation_date,creator,last_update_date,updator) 
                    values('{0}','{1}','{2}','{3}','{4}','{5}','{6}')
            """.format(role_id,role_name,status,current_rq(),'DBA',current_rq(),'DBA');
        print(sql)
        cr.execute(sql)
        save_role_privs(role_id,privs)
        cr.close()
        db.commit()
        result={}
        result['code']='0'
        result['message']='保存成功！'
        return result
    except:
        result['code'] = '-1'
        result['message'] = '保存失败！'
    return result


def upd_role(p_role):
    result={}
    try:
        db = get_connection()
        cr = db.cursor()
        roleid   = p_role['roleid']
        rolename = p_role['name']
        status   = p_role['status']
        privs    = p_role['privs']
        print("upd_role=",roleid,rolename,status)
        sql="""update t_role 
                  set  name    ='{0}',                      
                       status  ='{1}' ,
                       last_update_date ='{2}' ,
                       updator='{3}'
                where id='{4}'""".format(rolename,status,current_rq(),'DBA',roleid)
        print(sql)
        cr.execute(sql)
        upd_role_privs(roleid,privs);
        cr.close()
        db.commit()
        result={}
        result['code']='0'
        result['message']='更新成功！'
    except :
        result['code'] = '-1'
        result['message'] = '更新失败！'
    return result


def del_role(roleid):
    result={}
    try:
        db = get_connection()
        cr = db.cursor()
        print("fun:del_role,roleid=",roleid)
        sql="delete from t_role  where id='{0}'".format(roleid)
        print(sql)
        cr.execute(sql)
        del_role_privs(roleid)
        cr.close()
        db.commit()
        result={}
        result['code']='0'
        result['message']='删除成功！'
    except :
        result['code'] = '-1'
        result['message'] = '删除失败！'
    return result

def check_role(p_role):
    result = {}
    if p_role["name"]=="":
        result['code']='-1'
        result['message']='角色名不能为空！'
        return result
    if  if_exists_role(p_role["name"]):
        result['code'] = '-1'
        result['message'] = '角色名已存在！'
        return result

    result['code'] = '0'
    result['message'] = '验证通过'
    return result

