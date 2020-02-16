#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/30 15:46
# @Author  : 马飞
# @File    : t_user.py
# @Software: PyCharm

from web.utils.common     import exception_info,current_rq,aes_encrypt,aes_decrypt
from web.utils.common     import get_connection,get_connection_ds,get_connection_ds_sqlserver,get_connection_ds_oracle
from web.utils.common     import get_connection_ds_pg,get_connection_ds_mongo,get_connection_ds_redis,get_connection_ds_es
from web.model.t_user     import get_user_by_loginame
import re

def query_ds(dsname,market_id,db_env):
    db = get_connection()
    cr = db.cursor()
    v_where=' and 1=1 '

    if dsname != '':
        v_where = v_where + " and binary concat(b.dmmc,':/',ip,':',port,'/',service)  like '%{0}%'\n".format(dsname)

    if market_id != '':
        v_where = v_where + " and a.market_id='{0}'\n".format(market_id)

    if db_env != '':
        v_where = v_where + " and a.db_env='{0}'\n".format(db_env)

    sql ="""select  a.id,
                    d.dmmc as market_name,
                    a.db_desc,
                    c.dmmc as db_env,
                    concat(substr(concat(b.dmmc,':/',ip,':',port,'/',service),1,40),'...')  as name,              
                    user,
                    case status when '1' then '是' when '0' then '否' end  status,                    
                    updator,date_format(last_update_date,'%Y-%m-%d') last_update_date           
          from t_db_source a,t_dmmx b,t_dmmx c,t_dmmx d
          where a.db_type=b.dmm and b.dm='02'
            and a.db_env=c.dmm  and c.dm='03' 
            and a.market_id=d.dmm  and d.dm='05' 
            {0}
        order by d.dmmc,c.dmmc""".format(v_where)

    print(sql)
    cr.execute(sql)
    v_list = []
    for r in cr.fetchall():
        v_list.append(list(r))
    cr.close()
    db.commit()
    return v_list

def query_project(p_name):
    db = get_connection()
    cr = db.cursor()
    if p_name == "":
        sql ="""SELECT  a.id,
                        e.dmmc AS inst_name,
                        d.dmmc AS market_name,
                        a.db_desc,
                        c.dmmc AS db_env,
                        CONCAT(b.dmmc,':/',ip,':',PORT,'/',service) AS NAME,                   
                        USER,
                        CASE STATUS WHEN '1' THEN '是' WHEN '0' THEN '否' END  STATUS,                    
                        updator,DATE_FORMAT(last_update_date,'%Y-%m-%d') last_update_date           
                FROM t_db_source a,t_dmmx b,t_dmmx c,t_dmmx d,t_dmmx e
                WHERE a.db_type=b.dmm AND b.dm='02'
                  AND a.db_env=c.dmm AND c.dm='03' 
                  AND a.market_id=d.dmm AND d.dm='05'
                  AND a.inst_type=e.dmm AND e.dm='07'
                ORDER BY a.ip,PORT,a.service"""
    else:
        sql = """SELECT  a.id,
                         e.dmmc AS inst_name,
                         d.dmmc AS market_name,
                         a.db_desc,
                         c.dmmc AS db_env,
                         CONCAT(b.dmmc,':/',ip,':',PORT,'/',service) AS NAME,                   
                         USER,
                         CASE STATUS WHEN '1' THEN '是' WHEN '0' THEN '否' END  STATUS,                    
                         updator,DATE_FORMAT(last_update_date,'%Y-%m-%d') last_update_date           
                FROM t_db_source a,t_dmmx b,t_dmmx c,t_dmmx d,t_dmmx e
                WHERE a.db_type=b.dmm AND b.dm='02'
                  AND a.db_env=c.dmm AND c.dm='03' 
                  AND a.market_id=d.dmm AND d.dm='05'
                  AND a.inst_type=e.dmm AND e.dm='07'
                  AND binary concat(a.ip,':',a.port,'/',a.service)  like '%{0}%' 
                order by a.ip,port,a.service""".format(p_name)
    print(sql)
    cr.execute(sql)
    v_list = []
    for r in cr.fetchall():
        v_list.append(list(r))
    cr.close()
    db.commit()
    return v_list


def get_dsid():
    db = get_connection()
    cr = db.cursor()
    sql="select ifnull(max(id),0)+1 from t_db_source"
    cr.execute(sql)
    rs = cr.fetchone()
    cr.close()
    db.commit()
    return rs[0]

def get_ds_by_dsid(p_dsid):
    db = get_connection()
    cr = db.cursor()
    sql="""select cast(id as char) as id,db_type,db_desc,
                  ip,port,service,
                  user,password,status,creation_date,creator,last_update_date,updator ,
                  db_env,inst_type,market_id
           from t_db_source where id={0}
        """.format(p_dsid)
    cr.execute(sql)
    rs = cr.fetchall()
    cr.close()
    db.commit()
    d_ds={}
    d_ds['dsid']        = rs[0][0]
    d_ds['db_type']     = rs[0][1]
    d_ds['db_desc']     = rs[0][2]
    d_ds['ip']          = rs[0][3]
    d_ds['port']        = rs[0][4]
    d_ds['service']     = rs[0][5]
    d_ds['user']        = rs[0][6]
    d_ds['password']    = aes_decrypt(rs[0][7],rs[0][6])
    d_ds['status']      = rs[0][8]
    d_ds['db_env']      = rs[0][13]
    d_ds['inst_type']   = rs[0][14]
    d_ds['market_id']   = rs[0][15]
    d_ds['url']         = 'MySQL://{0}:{1}/{2}'.format(d_ds['ip'],d_ds['port'],d_ds['service'])
    return d_ds

def get_ds_by_dsid_by_cdb(p_dsid,p_cdb):
    db = get_connection()
    cr = db.cursor()
    sql="""select cast(id as char) as id,db_type,db_desc,
                  ip,port,
                  CASE WHEN service=NULL OR service='' THEN
                    '{0}'
                  ELSE
                     service 
                  END AS service,
                  user,password,status,creation_date,creator,last_update_date,updator ,
                  db_env,inst_type,market_id
           from t_db_source where id={1}
        """.format(p_cdb,p_dsid)
    cr.execute(sql)
    rs = cr.fetchall()
    cr.close()
    db.commit()
    d_ds={}
    d_ds['dsid']        = rs[0][0]
    d_ds['db_type']     = rs[0][1]
    d_ds['db_desc']     = rs[0][2]
    d_ds['ip']          = rs[0][3]
    d_ds['port']        = rs[0][4]
    d_ds['service']     = rs[0][5]
    d_ds['user']        = rs[0][6]
    d_ds['password']    = aes_decrypt(rs[0][7],rs[0][6])
    d_ds['status']      = rs[0][8]
    d_ds['db_env']      = rs[0][13]
    d_ds['inst_type']   = rs[0][14]
    d_ds['market_id']   = rs[0][15]
    d_ds['url']         = 'MySQL://{0}:{1}/{2}'.format(d_ds['ip'],d_ds['port'],d_ds['service'])
    print(d_ds)
    return d_ds


def get_dss_sql_query(logon_name):
    db = get_connection()
    cr = db.cursor()
    d_user=get_user_by_loginame(logon_name)

    sql="""select cast(id as char) as id,concat(b.dmmc,':/',ip,':',port,'/',service) as name 
           from t_db_source a,t_dmmx b
           where a.db_type=b.dmm and b.dm='02' and a.status='1'
               and (select proj_id from t_user_proj_privs where proj_id=a.id and user_id='{0}' and priv_id='1')
        """.format(d_user['userid'])
    print(sql)
    cr.execute(sql)
    v_list = []
    for r in cr.fetchall():
        v_list.append(list(r))
    cr.close()
    db.commit()
    return v_list

def get_dss2_sql_query(logon_name):
    db = get_connection()
    cr = db.cursor()
    d_user=get_user_by_loginame(logon_name)

    sql="""select cast(id as char) as id,a.db_desc as name 
           from t_db_source a,t_dmmx b
           where a.db_type=b.dmm and b.dm='02' and a.status='1'
               and (select proj_id from t_user_proj_privs where proj_id=a.id and user_id='{0}' and priv_id='1')
        """.format(d_user['userid'])
    print(sql)
    cr.execute(sql)
    v_list = []
    for r in cr.fetchall():
        v_list.append(list(r))
    cr.close()
    db.commit()
    return v_list

def get_dss_sql_release(logon_name):
    db = get_connection()
    cr = db.cursor()
    d_user = get_user_by_loginame(logon_name)
    sql="""select cast(id as char) as id,concat(b.dmmc,':/',ip,':',port,'/',service) as name 
           from t_db_source a,t_dmmx b
           where a.db_type=b.dmm and b.dm='02' and a.status='1'
               and (select proj_id from t_user_proj_privs where proj_id=a.id and user_id='{0}' and priv_id='2')
        """.format(d_user['userid'])
    print(sql)
    cr.execute(sql)
    v_list = []
    for r in cr.fetchall():
        v_list.append(list(r))
    cr.close()
    db.commit()
    return v_list

def save_ds(p_ds):
    result = {}
    val=check_ds(p_ds)
    if val['code']=='-1':
        return val
    try:
        db             = get_connection()
        cr             = db.cursor()
        ds_id          = get_dsid()
        ds_market_id   = p_ds['market_id']
        ds_inst_type   = p_ds['inst_type']
        ds_db_type     = p_ds['db_type']
        ds_db_env      = p_ds['db_env']
        ds_db_desc     = p_ds['db_desc']
        ds_ip          = p_ds['ip']
        ds_port        = p_ds['port']
        ds_service     = p_ds['service']
        ds_user        = p_ds['user']

        if p_ds['pass'] != '':
            ds_pass    = aes_encrypt(p_ds['pass'], ds_user)
        else:
            ds_pass    = p_ds['pass']

        status         = p_ds['status']
        sql="""insert into t_db_source(id,db_type,db_env,db_desc,ip,port,service,user,password,status,creation_date,creator,last_update_date,updator,market_id,inst_type) 
                    values('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}','{13}','{14}','{15}')
            """.format(ds_id,ds_db_type,ds_db_env,ds_db_desc,ds_ip,ds_port,ds_service,ds_user,ds_pass,status,current_rq(),'DBA',current_rq(),'DBA',ds_market_id,ds_inst_type);
        print(sql)
        cr.execute(sql)
        cr.close()
        db.commit()
        result={}
        result['code']='0'
        result['message']='保存成功！'
        return result
    except:
        e_str = exception_info()
        print(e_str)
        result['code'] = '-1'
        result['message'] = '保存失败！'
    return result


def upd_ds(p_ds):
    result={}
    val = check_ds(p_ds)
    if  val['code'] == '-1':
        return val
    try:
        db = get_connection()
        cr = db.cursor()
        ds_id          = p_ds['dsid']
        ds_market_id   = p_ds['market_id']
        ds_inst_type   = p_ds['inst_type']
        ds_db_type     = p_ds['db_type']
        ds_db_env      = p_ds['db_env']
        ds_db_desc     = p_ds['db_desc']
        ds_ip          = p_ds['ip']
        ds_port        = p_ds['port']
        ds_service     = p_ds['service']
        ds_user        = p_ds['user']

        print('upd_ds...p_ds=',p_ds)

        if p_ds['pass']!='':
           ds_pass     = aes_encrypt(p_ds['pass'],ds_user)
        else:
           ds_pass    = p_ds['pass']

        status         = p_ds['status']
        sql="""update t_db_source 
                  set  db_type     ='{0}', 
                       db_env      ='{1}',
                       db_desc     ='{2}' ,                        
                       ip          ='{3}',      
                       port        ='{4}' ,           
                       service     ='{5}' ,                           
                       user        ='{6}' ,           
                       password    ='{7}' , 
                       status      ='{8}' ,
                       last_update_date ='{9}' ,
                       updator='{10}',
                       market_id='{11}',
                       inst_type='{12}'
                where id='{13}'""".format(ds_db_type,ds_db_env,ds_db_desc,ds_ip,ds_port,ds_service,
                                          ds_user,ds_pass,status,current_rq(),'DBA',ds_market_id,ds_inst_type,ds_id)
        print(sql)
        cr.execute(sql)
        cr.close()
        db.commit()
        result={}
        result['code']='0'
        result['message']='更新成功！'
    except :
        result['code'] = '-1'
        result['message'] = '更新失败！'
    return result


def del_ds(p_dsid):
    result={}
    try:
        db = get_connection()
        cr = db.cursor()
        sql="delete from t_db_source  where id='{0}'".format(p_dsid)
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

def check_ds(p_ds):
    result = {}
    if p_ds["ip"]=="":
        result['code']='-1'
        result['message']='IP地址不能为空！'
        return result
    '''
    if re.match(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$", p_ds["ip"])==None:
        result['code'] = '-1'
        result['message'] = 'IP地址不正确！'
        return result
    '''
    if p_ds["port"] == "":
        result['code'] = '-1'
        result['message'] = '端口不能为空！'
        return result

    if re.match(r"^([1-9][0-9]{3,4})$",p_ds["port"])==None:
        result['code'] = '-1'
        result['message'] = '端口必须为4-5位连续数字且不能以0开头！'
        return result

    '''
    if p_ds["service"] == "":
        result['code'] = '-1'
        result['message'] = '服务名不能为空！'
        return result
    
    if re.match(r"^([a-zA-Z]{2,})",p_ds["service"]) == None:
        result['code'] = '-1'
        result['message'] = '服务名必须以两位字母开头！'
        return result
    '''

    if p_ds["user"] == "" and p_ds['db_type']=='0':
        result['code'] = '-1'
        result['message'] = '用户不能为空！'
        return result

    if p_ds["pass"] == "" and p_ds['db_type']=='0':
        result['code'] = '-1'
        result['message'] = '口令不能为空！'
        return result

    result['code'] = '0'
    result['message'] = '验证通过'
    return result

def check_ds_valid(p_id):
    result = {}
    try:
        p_ds=get_ds_by_dsid(p_id)
        if p_ds['db_type']=='0':
           conn=get_connection_ds(p_ds)
        elif p_ds['db_type']=='1':
           conn = get_connection_ds_oracle(p_ds)
        elif p_ds['db_type']=='2':
           conn = get_connection_ds_sqlserver(p_ds)
        elif p_ds['db_type']=='3':
           conn=get_connection_ds_pg(p_ds)
        elif p_ds['db_type'] == '4':
           conn = get_connection_ds_es(p_ds)
        elif p_ds['db_type']=='5':
           conn=get_connection_ds_redis(p_ds)
        elif p_ds['db_type']=='6':
           conn=get_connection_ds_mongo(p_ds)
        result['code'] = '0'
        result['message'] = '验证通过'
        print('ds=',conn)
        return result
    except:
        exception_info()
        result['code'] = '-1'
        result['message'] = '验证失败'
        return result