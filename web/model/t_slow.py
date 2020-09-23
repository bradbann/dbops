#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/30 15:46
# @Author  : 马飞
# @File    : t_user.py
# @Software: PyCharm

import traceback
from   web.utils.common import get_connection,get_connection_dict
from   web.model.t_db_inst import query_inst_by_id
import os,json

def query_slow(p_inst_id,p_inst_env):
    db  = get_connection()
    cr  = db.cursor()
    vv  = ''
    if p_inst_id != '':
        vv = "  where a.inst_id ='{0}' ".format(p_inst_id)

    if p_inst_env != '':
        vv = vv +"  and b.inst_env ='{0}' ".format(p_inst_env)

    sql = """select a.id,
                    b.inst_name,
                   (SELECT dmmc FROM t_dmmx X WHERE x.dm='03' AND x.dmm=b.inst_env) AS env_name,
                    a.log_file,
                    a.query_time,
                    a.script_file,
                    a.api_server,
                    case a.status when '1' then '是'  when '0' then '否'  end  status,
                    date_format(create_date,'%Y-%m-%d')    create_date
             from t_slow_log a,t_db_inst b
             where a.inst_id=b.id
             {}
             order by a.id""".format(vv)

    print(sql)
    cr.execute(sql)
    v_list = []
    for r in cr.fetchall():
        v_list.append(list(r))
    cr.close()
    db.commit()
    return v_list


def get_slowid():
    db = get_connection()
    cr = db.cursor()
    sql="select ifnull(max(id),0)+1 from t_role"
    cr.execute(sql)
    rs = cr.fetchone()
    cr.close()
    db.commit()
    return rs[0]

def get_slow_by_slowid(p_slowid):
    db = get_connection_dict()
    cr = db.cursor()
    sql="select * from t_slow_log where id={0}".format(p_slowid)
    print(sql)
    cr.execute(sql)
    rs = cr.fetchone()
    cr.close()
    db.commit()
    return rs

def get_slows():
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


def if_exists_slow(p_inst_id):
    db = get_connection()
    cr = db.cursor()
    sql="select count(0) from t_slow_log where inst_id='{0}'".format(p_inst_id)
    cr.execute(sql)
    rs = cr.fetchone()
    cr.close()
    if rs[0]==0:
        return False
    else:
        return True

def save_slow(p_slow):
    result = {}
    val = check_slow(p_slow)
    if val['code'] == '-1':
        return val
    try:
        db            = get_connection()
        cr            = db.cursor()
        inst_id       = p_slow['inst_id']
        server_id     = p_slow['server_id']
        slow_time     = p_slow['slow_time']
        slow_log_name = p_slow['slow_log_name']
        python3_home  = p_slow['python3_home']
        run_time      = p_slow['run_time']
        exec_time     = p_slow['exec_time']
        script_path   = p_slow['script_path']
        script_file   = p_slow['script_file']
        slow_status   = p_slow['slow_status']
        api_server    = p_slow['api_server']
        d_inst        = query_inst_by_id(inst_id)


        sql="""insert into t_slow_log(inst_id,server_id,log_file,query_time,python3_home,
                                      run_time,exec_time,script_path,script_file,status,api_server,create_date) 
                    values('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}',now())
            """.format(inst_id,server_id,slow_log_name,slow_time,python3_home,
                       run_time,exec_time,script_path,script_file,slow_status,api_server);
        print(sql)
        cr.execute(sql)

        if d_inst.get('is_rds') == 'N':
           sql = """INSERT INTO t_db_inst_parameter(inst_id,NAME,VALUE,TYPE,STATUS,create_date) 
                                 VALUES({},'慢日志开关'  ,'{}','mysqld','1',NOW()),
                                       ({},'慢日志文件名','{}','mysqld','1',NOW()),
                                       ({},'慢日志时长'  ,'{}','mysqld','1',NOW()) 
                """.format(inst_id, 'slow_query_log={}'.format('ON' if slow_status == '1' else 'OFF'),
                           inst_id, 'slow_query_log_file=''{{}}/{}'''.format(slow_log_name),
                           inst_id,'long_query_time={}'.format(slow_time))
           print(sql)
           cr.execute(sql)

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


def upd_slow(p_slow):
    result = {}
    try:
        db             = get_connection()
        cr             = db.cursor()
        slow_id        = p_slow['slow_id']
        inst_id        = p_slow['inst_id']
        server_id      = p_slow['server_id']
        slow_time      = p_slow['slow_time']
        slow_log_name  = p_slow['slow_log_name']
        python3_home   = p_slow['python3_home']
        run_time       = p_slow['run_time']
        exec_time      = p_slow['exec_time']
        script_path    = p_slow['script_path']
        script_file    = p_slow['script_file']
        slow_status    = p_slow['slow_status']
        api_server     = p_slow['api_server']

        sql="""update t_slow_log
                  set  inst_id        ='{}' ,
                       server_id      ='{}' ,
                       query_time     ='{}' ,
                       log_file       ='{}' ,
                       python3_home   ='{}' ,
                       run_time       ='{}' ,
                       exec_time      ='{}' ,
                       script_path    ='{}' ,
                       script_file    ='{}' ,
                       api_server     ='{}' ,
                       status         ='{}' ,
                       last_update_date =now() 
                where id='{}'
            """.format(inst_id,server_id,slow_time,slow_log_name,python3_home,
                       run_time,exec_time,script_path,script_file,api_server,slow_status,slow_id)
        print(sql)
        cr.execute(sql)

        sql = """delete from  t_db_inst_parameter 
                  where inst_id={} 
                   and (value like 'slow_query_log%' or value like 'long_query_time%')""".format(inst_id)
        print(sql)
        cr.execute(sql)

        sql = """INSERT INTO t_db_inst_parameter(inst_id,NAME,VALUE,TYPE,STATUS,create_date) 
                     VALUES({},'慢日志开关'  ,'{}','mysqld','1',NOW()),
                           ({},'慢日志文件名','{}','mysqld','1',NOW()),
                           ({},'慢日志时长'  ,'{}','mysqld','1',NOW()) 
              """.format(inst_id, 'slow_query_log={}'.format('ON' if slow_status == '1' else 'OFF'),
                         inst_id, 'slow_query_log_file=''{{}}/{}'''.format(slow_log_name),
                         inst_id, 'long_query_time={}'.format(slow_time))
        print(sql)
        cr.execute(sql)

        cr.close()
        db.commit()
        result={}
        result['code']='0'
        result['message']='更新成功！'
    except :
        print(traceback.print_exc())
        result['code'] = '-1'
        result['message'] = '更新失败！'
    return result


def del_slow(p_slowid):
    result={}
    try:
        db = get_connection()
        cr = db.cursor()
        sl = get_slow_by_slowid(p_slowid)
        print('del_slow.s1=',sl)

        sql="delete from t_slow_log  where id='{0}'".format(p_slowid)
        print(sql)
        cr.execute(sql)

        sql = """delete from  t_db_inst_parameter 
                        where inst_id={} 
                         and (value like 'slow_query_log%' or value like 'long_query_time%')""".format(sl['inst_id'])
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

def check_slow(p_slow):
    result = {}
    if p_slow["slow_time"]=="":
        result['code']='-1'
        result['message']='慢查询时长不能为空！'
        return result

    if p_slow["python3_home"]=="":
        result['code']='-1'
        result['message']='python3目录不能为空！'
        return result

    if p_slow["script_path"]=="":
        result['code']='-1'
        result['message']='脚本路径不能为空！'
        return result

    if p_slow["api_server"]=="":
        result['code']='-1'
        result['message']='API服务器不能为空！'
        return result


    if if_exists_slow(p_slow["inst_id"]):
        result['code'] = '-1'
        result['message'] = '慢日志已存在！'
        return result

    result['code'] = '0'
    result['message'] = '验证通过'
    return result

def query_slow_by_id(p_slow_id):
    db  = get_connection_dict()
    cr  = db.cursor()
    sql = """SELECT a.id,
                    a.inst_id,
                    a.server_id,
                    a.query_time,
                    a.log_file,
                    a.python3_home,
                    a.run_time,
                    a.exec_time,
                    a.script_path,
                    a.script_file,
                    a.api_server,
                    a.status,
                    date_format(a.create_date,'%Y-%m-%d %H:%i:%s')  as create_date,
                    date_format(a.last_update_date,'%Y-%m-%d %H:%i:%s')  as last_update_date                        
             FROM t_slow_log a  WHERE  a.id='{0}'""".format(p_slow_id)
    print(sql)
    cr.execute(sql)
    rs=cr.fetchone()
    cr.close()
    db.commit()
    return rs


def push_slow(p_api,p_slowid):
    try:
        result = {}
        result['code'] = '0'
        result['message'] = '慢日志配置正在更新中...'
        v_cmd="curl -XPOST {0}/push_slow_remote -d 'slow_id={1}'".format(p_api,p_slowid)
        print('push_slow=',v_cmd)
        r=os.popen(v_cmd).read()
        d=json.loads(r)
        if d['code']==200:
              return result
        else:
           result['code'] = '-1'
           result['message'] = '{0}!'.format(d['msg'])
           return result
    except Exception as e:
        print(traceback.print_exc())
        result['code'] = '-1'
        result['message'] = '慢日志配置更新失败!'
        return result