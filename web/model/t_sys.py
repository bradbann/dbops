#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/11/30 16:30
# @Author : 马飞
# @File : t_sys.py.py
# @Software: PyCharm

from web.utils.common import get_connection

def check_rule(rule):
    for key in rule:
        result = {}
        result['code'] = '0'
        result['message'] = '检测成功！'

        if key == 'switch_char_max_len':
           try:
              int(rule[key])
           except:
              result['code'] = '-1'
              result['message'] ='字符字段最大长度不是整数!'
              return result
    return result

def save_audit_rule(rule):
    result = check_rule(rule)
    if result['code']=='-1':
       return result
    try:
        db = get_connection()
        cr = db.cursor()
        for key in rule:
           sql= "update t_sql_audit_rule set rule_value='{}' where rule_code='{}'".format(rule[key],key)
           print('save_audit_rule=',sql)
           cr.execute(sql)
        cr.close()
        db.commit()
        result={}
        result['code']='0'
        result['message']='保存成功！'
        return result
    except Exception as e:
        print(str(e))
        result['code'] = '-1'
        result['message'] = '保存失败！'
    return result


def query_dm(p_code):
    db = get_connection()
    cr = db.cursor()
    v_where=' and  1=1 '
    if p_code != '':
        v_where = """ and (a.dm like '%{0}%' or a.mc like '%{1}%' 
                             or b.dmm like '%{2}%' or b.dmmc like '%{3}%')
                  """.format(p_code,p_code,p_code,p_code)

    sql = """SELECT a.dm,a.mc,b.dmm,b.dmmc  FROM t_dmlx a LEFT JOIN t_dmmx b ON a.dm=b.`dm`
               {0}
             ORDER BY a.dm,b.dmm
          """.format(v_where)
    print(sql)
    cr.execute(sql)
    v_list = []
    for r in cr.fetchall():
        v_list.append(list(r))
    cr.close()
    db.commit()
    return v_list