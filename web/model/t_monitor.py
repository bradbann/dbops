#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/30 15:46
# @Author  : 马飞
# @File    : t_user.py
# @Software: PyCharm

from web.utils.common     import exception_info
from web.utils.common     import get_connection,get_connection_dict
from web.utils.common     import current_rq
import os,json
import traceback

def query_monitor_index(index_code):
    db = get_connection()
    cr = db.cursor()
    v_where=' '
    if index_code != '':
        v_where = " where a.index_code like '%{0}%' or a.index_name like '%{1}%'".format(index_code,index_code)

    sql = """SELECT
                 id,  
                 index_code,
                 index_name,                 
                 (SELECT dmmc FROM t_dmmx b 
                    WHERE a.index_type=b.dmm AND b.dm='23') AS index_type,
                 (SELECT dmmc FROM t_dmmx b 
                    WHERE a.index_db_type=b.dmm AND b.dm='02') AS index_db_type,  
                 (SELECT dmmc FROM t_dmmx b 
                    WHERE a.index_threshold_type=b.dmm AND b.dm='24') AS index_threshold_type,     
                 case when a.index_threshold_type='1' or a.index_threshold_type='3' then
                    index_threshold
                 else
                    concat(index_threshold_day,'^',index_threshold_times)                   
                 end as    index_threshold,
                 concat(trigger_time,'^',trigger_times),
                 CASE a.STATUS WHEN '1' THEN '启用' WHEN '0' THEN '禁用' END  AS  flag
            FROM t_monitor_index a
            {0}
            order by a.index_type,a.id
          """.format(v_where)
    print(sql)
    cr.execute(sql)
    v_list = []
    for r in cr.fetchall():
        v_list.append(list(r))
    cr.close()
    db.commit()
    return v_list

def save_index(p_index):
    result = {}
    val=check_index(p_index)
    if val['code']=='-1':
        return val
    try:
        db      = get_connection()
        cr      = db.cursor()
        result  = {}
        sql="""insert into t_monitor_index(
                           index_name,index_code,index_type,index_db_type,index_threshold_type,
                           index_threshold_day,index_threshold_times,index_threshold,status,trigger_time,trigger_times)
               values('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}')
            """.format(p_index['index_name'],p_index['index_code'],p_index['index_type'],p_index['index_db_type'],
                       p_index['index_val_type'],p_index['index_threshold_day'],p_index['index_threshold_times'],
                       p_index['index_threshold'],p_index['index_status'],
                       p_index['index_trigger_time'],p_index['index_trigger_times']
                     )
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

def upd_index(p_index):
    result={}
    val = check_index(p_index)
    if  val['code'] == '-1':
        return val
    try:
        db   = get_connection()
        cr   = db.cursor()

        sql="""update t_monitor_index  set  
                      index_name            ='{0}',
                      index_code            ='{1}',
                      index_type            ='{2}', 
                      index_db_type         ='{3}',
                      index_threshold_type  ='{4}',
                      index_threshold       ='{5}', 
                      index_threshold_day   ='{6}',
                      index_threshold_times ='{7}',
                      status                ='{8}',                      
                      trigger_time          ='{9}',
                      trigger_times         ='{10}'                      
                where id='{11}'
            """.format(p_index['index_name'],p_index['index_code'],p_index['index_type'], p_index['index_db_type'],
                       p_index['index_val_type'], p_index['index_threshold'],p_index['index_threshold_day'],
                       p_index['index_threshold_times'],p_index['index_status'],
                       p_index['index_trigger_time'],p_index['index_trigger_times'],p_index['index_id'])
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

def del_index(p_index_code):
    result={}
    try:
        db = get_connection()
        cr = db.cursor()
        sql="delete from t_monitor_index  where index_code='{0}'".format(p_index_code)
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

def check_index(p_index):
    result = {}

    if p_index["index_name"]=="":
        result['code']='-1'
        result['message']='指标名称不能为空！'
        return result

    if p_index["index_code"] == "":
        result['code'] = '-1'
        result['message'] = '指标代码不能为空！'
        return result

    if p_index["index_type"]=="":
        result['code']='-1'
        result['message']='指标类型不能为空！'
        return result

    if p_index["index_type"]=='2':
        if p_index["index_db_type"]=="":
            result['code']='-1'
            result['message']='数据库类型不能为空！'
            return result

    if p_index["index_val_type"] == "":
        result['code'] = '-1'
        result['message'] = '阀值类型不能为空！'
        return result

    if p_index["index_val_type"] == "1":
        if p_index["index_threshold"] == "":
            result['code'] = '-1'
            result['message'] = '指标阀值(百分比)不能为空！'
            return result
    elif p_index["index_val_type"] == "3":
        if p_index["index_threshold"] == "":
            result['code'] = '-1'
            result['message'] = '指标阀值(布尔值)不能为空！'
            return result
    else:
        if p_index["index_threshold_day"] == "" or p_index["index_threshold_times"] == "":
            result['code'] = '-1'
            result['message'] = '指标阀值(计算)不能为空！'
            return result

    if p_index["index_status"] == "":
        result['code'] = '-1'
        result['message'] = '指标状态不能为空！'
        return result

    result['code'] = '0'
    result['message'] = '验证通过'
    return result

def get_index_by_index_code(p_index_code):
    db = get_connection_dict()
    cr = db.cursor()
    sql = """SELECT  index_name,index_code,index_type,index_db_type,index_threshold,status
             FROM t_monitor_index where index_code='{0}'
          """.format(p_index_code)
    cr.execute(sql)
    rs = cr.fetchall()
    cr.close()
    db.commit()
    print('get_index_by_index_code->rs=',rs)
    return rs[0]

def get_index_by_index_id(p_id):
    db = get_connection_dict()
    cr = db.cursor()
    sql = """SELECT  index_name,index_code,index_type,index_db_type,index_threshold,status
             FROM t_monitor_index where id='{0}'
          """.format(p_id)
    cr.execute(sql)
    rs = cr.fetchall()
    cr.close()
    db.commit()
    print('get_index_by_index_id->rs=',rs)
    return rs[0]

def get_monitor_indexes():
    db = get_connection()
    cr = db.cursor()
    sql = """SELECT  id,index_name FROM t_monitor_index WHERE STATUS='1'"""
    cr.execute(sql)
    v_list = []
    for r in cr.fetchall():
        v_list.append(list(r))
    cr.close()
    return v_list

def get_monitor_indexes2(p_type):
    db = get_connection()
    cr = db.cursor()
    sql=''
    if p_type=='':
        sql = """SELECT  index_code,index_name FROM t_monitor_index
                          WHERE STATUS='1' order by index_type,id"""
    else:
        sql = """SELECT  index_code,index_name FROM t_monitor_index 
                     WHERE STATUS='1' and index_type='{0}' order by index_type,id """.format(p_type)
    cr.execute(sql)
    v_list = []
    for r in cr.fetchall():
        v_list.append(list(r))
    cr.close()
    return v_list

def query_monitor_templete(templete_code):
    db = get_connection()
    cr = db.cursor()
    v_where=' '
    if templete_code != '':
        v_where = " where a.code like '%{0}%' or a.code like '%{1}%'".format(templete_code,templete_code)

    sql = """SELECT  
                 code,
                 name,       
                 (SELECT dmmc FROM t_dmmx b 
                    WHERE a.type=b.dmm AND b.dm='23') AS templete_type,     
                 CASE a.STATUS WHEN '1' THEN '启用' WHEN '0' THEN '禁用' END  AS  flag, 
                 creator,
                 date_format(creation_date,'%Y-%m-%d')  creation_date,
                 updator,
                 date_format(last_update_date,'%Y-%m-%d') last_update_date
            FROM t_monitor_templete a
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

def get_monitor_sys_indexes(p_templete_code):
    db = get_connection()
    cr = db.cursor()
    sql = """SELECT  id,index_name FROM t_monitor_index 
              WHERE STATUS='1' and id not in(select index_id from t_monitor_templete_index 
                                             where templete_id=(select id from t_monitor_templete where code='{0}'))
          """.format(p_templete_code)
    cr.execute(sql)
    v_list = []
    for r in cr.fetchall():
        v_list.append(list(r))
    cr.close()
    return v_list

def get_monitor_templete_indexes(p_templete_code):
    db = get_connection()
    cr = db.cursor()
    sql = """SELECT  id,index_name FROM t_monitor_index 
              WHERE STATUS='1'  and id in(select index_id from t_monitor_templete_index
                                          where templete_id=(select id from t_monitor_templete where code='{0}'))
          """.format(p_templete_code)
    cr.execute(sql)
    v_list = []
    for r in cr.fetchall():
        v_list.append(list(r))
    cr.close()
    return v_list

def get_templeteid():
    db = get_connection()
    cr = db.cursor()
    sql="select ifnull(max(id),0)+1 from t_monitor_templete"
    cr.execute(sql)
    rs = cr.fetchone()
    cr.close()
    db.commit()
    return rs[0]

def get_templeteid_by_code(p_code):
    db = get_connection()
    cr = db.cursor()
    sql="select id from t_monitor_templete where code='{0}'".format(p_code)
    cr.execute(sql)
    rs = cr.fetchone()
    cr.close()
    db.commit()
    return rs[0]

def save_templete_indexes(p_templete_id,p_indexes):
    result = {}
    try:
        db = get_connection()
        cr = db.cursor()
        print(p_indexes)
        for id in p_indexes.split(','):
          sql="""insert into t_monitor_templete_index(templete_id,index_id,creation_date,creator,last_update_date,updator) 
                    values({0},'{1}','{2}','{3}','{4}','{5}')
              """.format(p_templete_id,id,current_rq(),'DBA',current_rq(),'DBA')
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

def upd_templete_indexes(p_templete_id,p_indexes):
    result = {}
    try:
        db = get_connection()
        cr = db.cursor()
        print(p_indexes)
        cr.execute("delete from t_monitor_templete_index where  templete_id='{0}'".format(p_templete_id))
        for id in p_indexes.split(','):
          sql="""insert into t_monitor_templete_index(templete_id,index_id,creation_date,creator,last_update_date,updator) 
                    values({0},'{1}','{2}','{3}','{4}','{5}')
              """.format(p_templete_id,id,current_rq(),'DBA',current_rq(),'DBA')
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

def save_templete(p_templete):
    result = {}
    val=check_templete(p_templete)
    if val['code']=='-1':
        return val
    try:
        db      = get_connection()
        cr      = db.cursor()
        templete_id= get_templeteid()
        result  = {}
        sql ="""insert into t_monitor_templete(id,name,code,type,status,creation_date,creator,last_update_date,updator)
                  values('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}')
             """.format(templete_id,p_templete['templete_name'],p_templete['templete_code'],p_templete['templete_type'],
                        p_templete['templete_status'],current_rq(), 'DBA', current_rq(), 'DBA')
        print(sql)
        cr.execute(sql)
        save_templete_indexes(templete_id,p_templete['templete_indexes'])
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

def upd_templete(p_templete):
    result={}
    val = check_templete(p_templete)
    if  val['code'] == '-1':
        return val
    try:
        db          = get_connection()
        cr          = db.cursor()
        templete_id = get_templeteid_by_code(p_templete['templete_code'])
        sql         = """update t_monitor_templete  set  
                            name    ='{0}',
                            type    ='{1}',
                            status  ='{2}',
                            updator ='{3}',
                            last_update_date ='{4}'
                          where code='{5}'
                      """.format(p_templete['templete_name'],p_templete['templete_type'],
                                 p_templete['templete_status'], 'DBA',current_rq(),p_templete['templete_code'])
        print(sql)
        cr.execute(sql)
        upd_templete_indexes(templete_id, p_templete['templete_indexes'])
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

def del_templete(p_templete_code):
    result={}
    try:
        db = get_connection()
        cr = db.cursor()
        cr.execute("delete from t_monitor_templete_index where templete_id =(select id from t_monitor_templete where code='{0}')".format(p_templete_code))
        cr.execute("delete from t_monitor_templete  where code='{0}'".format(p_templete_code))
        cr.close()
        db.commit()
        result={}
        result['code']='0'
        result['message']='删除成功！'
    except :
        result['code'] = '-1'
        result['message'] = '删除失败！'
    return result

def check_templete(p_index):
    result = {}

    if p_index["templete_name"]=="":
        result['code']='-1'
        result['message']='模板名称不能为空！'
        return result

    if p_index["templete_code"] == "":
        result['code'] = '-1'
        result['message'] = '模板代码不能为空！'
        return result

    if p_index["templete_indexes"]=="":
        result['code']='-1'
        result['message']='模板指标不能为空！'
        return result

    result['code'] = '0'
    result['message'] = '验证通过'
    return result

def check_task(p_task):
    result = {}

    result['code'] = '0'
    result['message'] = '验证通过'
    return result

def get_templete_by_templete_code(p_index_code):
    db = get_connection_dict()
    cr = db.cursor()
    sql = """SELECT  name,code,status FROM t_monitor_index where code='{0}'
          """.format(p_index_code)
    cr.execute(sql)
    rs = cr.fetchall()
    cr.close()
    db.commit()
    print('get_templete_by_templete_code->rs=',rs)
    return rs[0]

def get_templetes_by_templete_id(p_templeteid):
    db = get_connection()
    cr = db.cursor()
    sql = """SELECT  name FROM t_monitor_templete where status='1' and instr('{0}',id)>0""".format(p_templeteid)
    cr.execute(sql)
    rs = cr.fetchall()
    t=''
    for i in range(len(rs)):
       t=t+rs[i][0]+','
    cr.close()
    db.commit()
    return t[0:-1]

def query_task(p_task_tag):
    db = get_connection()
    cr = db.cursor()
    v_where=' '
    if p_task_tag != '':
        v_where = " and a.task_tag like '%{0}%'".format(p_task_tag)

    sql = """SELECT  
                 task_tag,
                 comments,
                 CONCAT(b.server_ip,':',b.server_port) AS sync_server,             
                 templete_id,
                 run_time,
                 api_server,
                 CASE a.STATUS WHEN '1' THEN '启用' WHEN '0' THEN '禁用' END  AS  flag
            FROM t_monitor_task a,t_server b
            where a.server_id=b.id
             {0}
          """.format(v_where)
    print(sql)
    cr.execute(sql)
    v_list = []
    v_temp = []
    for r in cr.fetchall():
        v_temp = list(r)
        v_temp.insert(4,get_templetes_by_templete_id(v_temp[3]))
        v_list.append(v_temp)
    cr.close()
    db.commit()
    return v_list

def save_gather_task(p_task):
    result = {}
    val=check_task(p_task)
    if val['code']=='-1':
        return val
    try:
        db      = get_connection()
        cr      = db.cursor()
        result  = {}
        sql ="""insert into t_monitor_task
                  (task_tag,comments,server_id,db_id,templete_id,run_time,script_path,script_file,python3_home,api_server,status)
                values('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}')
             """.format(p_task['add_gather_task_tag'],
                        p_task['add_gather_task_desc'],
                        p_task['add_gather_server'],
                        p_task['add_gather_task_db_server'],
                        p_task['add_gather_task_templete_name'],
                        p_task['add_gather_task_run_time'],
                        p_task['add_gather_task_script_base'],
                        p_task['add_gather_task_script_name'],
                        p_task['add_gather_task_python3_home'],
                        p_task['add_gather_task_api_server'],
                        p_task['add_gather_task_status']
                        )
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

def push_monitor_task(p_tag,p_api):
    try:
        result = {}
        result['code'] = '0'
        result['message'] = '推送成功！'
        v_cmd="curl -XPOST {0}/push_script_remote_monitor -d 'tag={1}'".format(p_api,p_tag)
        print('push_archive_task=',v_cmd)
        r=os.popen(v_cmd).read()
        d=json.loads(r)

        if d['code']==200:
           return result
        else:
           result['code'] = '-1'
           result['message'] = '{0}!'.format(d['msg'])
           return result
    except Exception as e:
        print('push_script_remote_monitor.error:',traceback.format_exc())
        result['code'] = '-1'
        result['message'] = '{0!'.format(traceback.format_exc())
        return result

def run_monitor_task(p_tag,p_api):
    try:
        result = {}
        result['code'] = '0'
        result['message'] = '执行成功！'
        v_cmd = "curl -XPOST {0}/run_script_remote_archive -d 'tag={1}'".format(p_api,p_tag)
        print('v_cmd=', v_cmd)
        r = os.popen(v_cmd).read()
        d = json.loads(r)
        if d['code'] == 200:
            return result
        else:
            result['code'] = '-1'
            result['message'] = '{0}!'.format(d['msg'])
            return result

    except Exception as e:
          result['code'] = '-1'
          result['message'] = '{0}!'.format(str(e))
          return result

def stop_monitor_task(p_tag,p_api):
    try:
        result = {}
        result['code'] = '0'
        result['message'] = '停止成功！'
        v_cmd = "curl -XPOST {0}/stop_script_remote_archive -d 'tag={1}'".format(p_api,p_tag)
        r = os.popen(v_cmd).read()
        d = json.loads(r)

        if d['code'] == 200:
            return result
        else:
            result['code'] = '-1'
            result['message'] = '{0}!'.format(d['msg'])
            return result

    except Exception as e:
         result['code'] = '-1'
         result['message'] = '{0!'.format(str(e))
         return result


def query_monitor_log_analyze(server_id,index_code,begin_date,end_date):
    db  = get_connection()
    cr  = db.cursor()
    v_where    = ' where 1=1 '

    if server_id != '':
        v_where = v_where + " and a.server_id='{0}'\n".format(server_id)

    if begin_date != '':
        v_where = v_where + " and a.create_date>='{0}'\n".format(begin_date+' 0:0:0')

    if end_date != '':
        v_where = v_where + " and a.create_date<='{0}'\n".format(end_date+' 23:59:59')

    if index_code=='cpu_usage':
       sql = """SELECT cast(a.create_date as char) as create_date,a.cpu_usage 
                 FROM t_monitor_task_server_log a {0} ORDER BY a.create_date
             """.format(v_where)
    elif index_code=='mem_usage':
       sql = """SELECT cast(a.create_date as char) as create_date,a.mem_usage 
                 FROM t_monitor_task_server_log a {0} ORDER BY a.create_date
             """.format(v_where)
    elif index_code == 'disk_usage':
        sql = """SELECT cast(a.create_date as char) as create_date,a.disk_usage 
                    FROM t_monitor_task_server_log a {0} ORDER BY a.create_date
              """.format(v_where)
    elif index_code == 'disk_read':
        sql = """SELECT cast(a.create_date as char) as create_date,a.disk_read 
                    FROM t_monitor_task_server_log a {0} ORDER BY a.create_date
              """.format(v_where)
    elif index_code == 'disk_write':
        sql = """SELECT cast(a.create_date as char) as create_date,a.disk_write
                    FROM t_monitor_task_server_log a {0} ORDER BY a.create_date
              """.format(v_where)
    elif index_code == 'net_out':
        sql = """SELECT cast(a.create_date as char) as create_date,a.net_out 
                      FROM t_monitor_task_server_log a {0} ORDER BY a.create_date
                """.format(v_where)
    elif index_code == 'net_in':
        sql = """SELECT cast(a.create_date as char) as create_date,a.net_in
                      FROM t_monitor_task_server_log a {0} ORDER BY a.create_date
                """.format(v_where)
    elif index_code == 'mysql_total_connect':
        sql = """SELECT cast(a.create_date as char) as create_date,a.total_connect
                      FROM t_monitor_task_db_log a {0} ORDER BY a.create_date
                """.format(v_where)
    elif index_code == 'mysql_active_connect':
        sql = """SELECT cast(a.create_date as char) as create_date,a.active_connect
                         FROM t_monitor_task_db_log a {0} ORDER BY a.create_date
                   """.format(v_where)
    elif index_code == 'mysql_available':
        sql = """SELECT cast(a.create_date as char) as create_date,a.db_available
                            FROM t_monitor_task_db_log a {0} ORDER BY a.create_date
                      """.format(v_where)
    else:
        pass

    print(sql)
    cr.execute(sql)
    v_list1 = []
    for r in cr.fetchall():
        v_list1.append(list(r))
    cr.close()
    db.commit()
    return v_list1