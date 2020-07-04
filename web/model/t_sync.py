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

def query_sync(sync_tag,market_id,sync_ywlx,sync_type):
    db = get_connection()
    cr = db.cursor()
    v_where=' and  1=1 '
    if sync_tag != '':
        v_where = v_where + " and a.sync_tag like '%{0}%'\n".format(sync_tag)

    if market_id != '':
        v_where = v_where + " and instr(a.sync_col_val,'{0}')>0\n".format(market_id)

    if sync_ywlx != '':
        v_where = v_where + " and a.sync_ywlx='{0}'\n".format(sync_ywlx)

    if sync_type != '':
        v_where = v_where + " and a.sync_type='{0}'\n".format(sync_type)

    sql = """SELECT  a.id,
                     concat(substr(a.sync_tag,1,40),'...') as sync_tag_,             
                     a.sync_tag,
                     concat(substr(a.comments,1,30),'...') as comments,
                     CONCAT(b.server_ip,':',b.server_port) AS sync_server,
                     c.dmmc AS  sync_ywlx,
                    --  d.dmmc AS  sync_type,
                     a.run_time,
                     a.api_server,
                     CASE a.STATUS WHEN '1' THEN '启用' WHEN '0' THEN '禁用' END  STATUS
             FROM t_db_sync_config a,t_server b ,t_dmmx c,t_dmmx d
            WHERE a.server_id=b.id AND b.status='1' 
              AND c.dm='08' AND d.dm='09'
              AND a.sync_ywlx=c.dmm
              AND a.sync_type=d.dmm
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

def query_sync_log(sync_tag,market_id,sync_ywlx,begin_date,end_date):
    db = get_connection()
    cr = db.cursor()

    v_where=' and 1=1 '
    if sync_tag != '':
        v_where = v_where + " and a.sync_tag='{0}'\n".format(sync_tag)

    if market_id != '':
        v_where = v_where + " and a.sync_col_val='{0}'\n".format(market_id)

    if sync_ywlx != '':
        v_where = v_where + " and a.sync_ywlx='{0}'\n".format(sync_ywlx)

    if begin_date != '':
        v_where = v_where + " and b.create_date>='{0}'\n".format(begin_date+' 0:0:0')
    else:
        v_where = v_where + " and b.create_date>=DATE_ADD(NOW(),INTERVAL -1 hour)\n"

    if end_date != '':
        v_where = v_where + " and b.create_date<='{0}'\n".format(end_date+' 23:59:59')

    sql = """SELECT b.id,
                    c.dmmc as market_name,
                    a.comments,
                    b.sync_tag,
                    cast(b.create_date as char),
                    b.duration,
                    b.amount
            FROM  t_db_sync_config a,t_db_sync_tasks_log b,t_dmmx c
            WHERE a.sync_tag=b.sync_tag 
              and c.dm='05' 
              and instr(a.sync_col_val,c.dmm)>0
              and a.status='1'
              {0}
            -- order by b.create_date desc,b.sync_tag 
        """.format(v_where)
    print(sql)
    cr.execute(sql)
    v_list = []
    for r in cr.fetchall():
        v_list.append(list(r))
    cr.close()
    db.commit()
    return v_list

def query_sync_log_analyze(market_id,tagname,begin_date,end_date):
    db  = get_connection()
    cr  = db.cursor()
    v_where = ' where 1=1 '

    if market_id != '':
        v_where = v_where + " and exists(select 1 from t_db_sync_config b where a.sync_tag=b.sync_tag and instr(b.sync_col_val,'{0}')>0) \n".format(market_id)

    if tagname != '':
        v_where = v_where + " and a.sync_tag='{0}'\n".format(tagname)

    if begin_date != '':
        v_where = v_where + " and a.create_date>='{0}'\n".format(begin_date+' 0:0:0')

    if end_date != '':
        v_where = v_where + " and a.create_date<='{0}'\n".format(end_date+' 23:59:59')

    sql1 = """SELECT 
                  cast(a.create_date as char) as create_date,a.duration
              FROM t_db_sync_tasks_log a
              {0}
              ORDER BY a.create_date
             """.format(v_where)

    sql2 = """SELECT 
                  cast(a.create_date as char) as create_date,a.amount
              FROM t_db_sync_tasks_log a 
              {0}
              ORDER BY a.create_date
             """.format(v_where)

    print(sql1)
    print(sql2)

    cr.execute(sql1)
    v_list1 = []
    for r in cr.fetchall():
        v_list1.append(list(r))

    cr.execute(sql2)
    v_list2 = []
    for r in cr.fetchall():
        v_list2.append(list(r))

    cr.close()
    db.commit()
    return v_list1,v_list2


def query_sync_log_analyze2(market_id,sync_type,begin_date,end_date):
    db  = get_connection()
    cr  = db.cursor()
    v_where = ' where 1=1 '

    if market_id != '':
        v_where = v_where + " and exists(select 1 from t_db_sync_config b where a.sync_tag=b.sync_tag and b.sync_col_val='{0}')\n".format(market_id)

    if sync_type != '':
        v_where = v_where + " and a.sync_ywlx='{0}'\n".format(sync_type)

    if begin_date != '':
        v_where = v_where + " and a.create_date>='{0}'\n".format(begin_date+' 0:0:0')

    if end_date != '':
        v_where = v_where + " and a.create_date<='{0}'\n".format(end_date+' 23:59:59')

    sql1 = """SELECT 
                  cast(a.create_date as char) as create_date,a.duration
              FROM t_db_sync_tasks_log a
              {0}
              ORDER BY a.create_date
             """.format(v_where)

    sql2 = """SELECT 
                  cast(a.create_date as char) as create_date,a.amount
              FROM t_db_sync_tasks_log a 
              {0}
              ORDER BY a.create_date
             """.format(v_where)

    print(sql1)
    print(sql2)

    cr.execute(sql1)
    v_list1 = []
    for r in cr.fetchall():
        v_list1.append(list(r))

    cr.execute(sql2)
    v_list2 = []
    for r in cr.fetchall():
        v_list2.append(list(r))

    cr.close()
    db.commit()
    return v_list1,v_list2


def query_sync_log_detail(p_tag,p_sync_rqq,p_sync_rqz):
    db = get_connection()
    cr = db.cursor()
    v_where = ' and 1=1 '
    if p_tag != '':
        v_where = v_where + " and a.sync_tag='{0}'\n".format(p_tag)

    if p_sync_rqq != '':
       v_where = v_where + " and b.create_date>='{0}' \n".format(p_sync_rqq+' 0:0:0')

    if p_sync_rqz != '':
        v_where = v_where + " and b.create_date<='{0}'\n".format(p_sync_rqz+' 23:59:59')

    sql = """SELECT 
                 a.comments,
                 b.sync_tag,
                 b.sync_table,
                 CAST(b.create_date AS CHAR), 
                 b.sync_amount,
                 b.duration 
                FROM 
                 t_db_sync_config a,t_db_sync_tasks_log_detail b
                WHERE  a.sync_tag=b.sync_tag 
                   AND a.status='1'
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

def save_sync(p_backup):
    result = {}
    #增加tag重复验证
    val=check_sync(p_backup,'add')
    if val['code']=='-1':
        return val
    try:
        db                   = get_connection()
        cr                   = db.cursor()
        result               = {}
        sync_server          = p_backup['sync_server']
        sour_db_server       = p_backup['sour_db_server']
        desc_db_server       = p_backup['desc_db_server']
        sync_tag             = p_backup['sync_tag']
        sync_ywlx            = p_backup['sync_ywlx']
        sync_type            = p_backup['sync_data_type']
        script_base          = p_backup['script_base']
        script_name          = p_backup['script_name']
        run_time             = p_backup['run_time']
        task_desc            = p_backup['task_desc']
        python3_home         = p_backup['python3_home']
        sync_schema          = p_backup['sync_schema']
        sync_schema_dest     = p_backup['sync_schema_dest']
        sync_tables          = p_backup['sync_tables']
        sync_batch_size      = p_backup['sync_batch_size']
        sync_batch_size_incr = p_backup['sync_batch_size_incr']
        sync_gap             = p_backup['sync_gap']
        sync_col_name        = p_backup['sync_col_name']
        sync_col_val         = format_sql(p_backup['sync_col_val'])
        sync_time_type       = p_backup['sync_time_type']
        api_server           = p_backup['api_server']
        status               = p_backup['status']
        sql                  = ''

        if sync_schema_dest=='':
            sql = """insert into t_db_sync_config(
                                  sour_db_id,desc_db_id,server_id,
                                  sync_tag,sync_ywlx,sync_type,
                                  comments,run_time,sync_table,sync_schema,
                                  batch_size,batch_size_incr,sync_gap,
                                  script_path,script_file,python3_home,api_server,
                                  sync_col_name,sync_col_val,sync_time_type,status,sync_schema_dest)
                          values('{0}','{1}','{2}',
                                 '{3}','{4}','{5}',
                                 '{6}','{7}','{8}','{9}',
                                 '{10}','{11}','{12}',
                                 '{13}','{14}','{15}','{16}',
                                 '{17}','{18}','{19}','{20}',null)
                       """.format(sour_db_server, desc_db_server, sync_server,
                                  sync_tag, sync_ywlx, sync_type,
                                  task_desc, run_time, sync_tables, sync_schema,
                                  sync_batch_size, sync_batch_size_incr, sync_gap,
                                  script_base, script_name, python3_home, api_server,
                                  sync_col_name, sync_col_val, sync_time_type, status)

        else:
            sql="""insert into t_db_sync_config(
                           sour_db_id,desc_db_id,server_id,
                           sync_tag,sync_ywlx,sync_type,
                           comments,run_time,sync_table,sync_schema,
                           batch_size,batch_size_incr,sync_gap,
                           script_path,script_file,python3_home,api_server,
                           sync_col_name,sync_col_val,sync_time_type,status,sync_schema_dest)
                   values('{0}','{1}','{2}',
                          '{3}','{4}','{5}',
                          '{6}','{7}','{8}','{9}',
                          '{10}','{11}','{12}',
                          '{13}','{14}','{15}','{16}',
                          '{17}','{18}','{19}','{20}','{21}')
                """.format(sour_db_server,desc_db_server,sync_server,
                           sync_tag,sync_ywlx,sync_type,
                           task_desc,run_time,sync_tables,sync_schema,
                           sync_batch_size,sync_batch_size_incr,sync_gap,
                           script_base,script_name,python3_home,api_server,
                           sync_col_name,sync_col_val,sync_time_type,status,sync_schema_dest)
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

def upd_sync(p_sync):
    result={}
    val = check_sync(p_sync,'upd')
    if  val['code'] == '-1':
        return val
    try:
        db = get_connection()
        cr = db.cursor()
        sync_server     = p_sync['sync_server']
        sour_db_server  = p_sync['sour_db_server']
        desc_db_server  = p_sync['desc_db_server']
        sync_tag        = p_sync['sync_tag']
        sync_ywlx       = p_sync['sync_ywlx']
        sync_type       = p_sync['sync_data_type']
        script_base     = p_sync['script_base']
        script_name     = p_sync['script_name']
        run_time        = p_sync['run_time']
        task_desc       = p_sync['task_desc']
        python3_home    = p_sync['python3_home']
        sync_schema     = p_sync['sync_schema']
        sync_schema_dest = p_sync['sync_schema_dest']
        sync_tables     = p_sync['sync_tables']
        sync_batch_size = p_sync['sync_batch_size']
        sync_batch_size_incr = p_sync['sync_batch_size_incr']
        sync_gap        = p_sync['sync_gap']
        sync_col_name   = p_sync['sync_col_name']
        sync_col_val    = format_sql(p_sync['sync_col_val'])
        sync_time_type  = p_sync['sync_time_type']
        api_server      = p_sync['api_server']
        status          = p_sync['status']
        sync_id         = p_sync['sync_id']
        sql             = ''
        if sync_schema_dest == '':

            sql="""update t_db_sync_config 
                      set  
                          server_id         ='{0}',
                          sour_db_id        ='{1}',     
                          desc_db_id        ='{2}',
                          sync_tag          ='{3}',
                          sync_ywlx         ='{4}',
                          sync_type         ='{5}',
                          comments          ='{6}',
                          run_time          ='{7}',
                          sync_table        ='{8}',
                          sync_schema       ='{9}',
                          batch_size        ='{10}',
                          batch_size_incr   ='{11}',
                          sync_gap          ='{12}',
                          script_path       ='{13}',
                          script_file       ='{14}',
                          python3_home      ='{15}',
                          api_server        ='{16}',
                          sync_col_name     ='{17}',
                          sync_col_val      ='{18}',
                          sync_time_type    ='{19}',
                          status            ='{20}',
                          sync_schema_dest  =null
                    where id={21}""".format(sync_server,sour_db_server,desc_db_server,
                                            sync_tag,sync_ywlx,sync_type,
                                            task_desc,run_time,sync_tables,
                                            sync_schema,sync_batch_size,sync_batch_size_incr,
                                            sync_gap,script_base,script_name,
                                            python3_home,api_server,sync_col_name,
                                            sync_col_val,sync_time_type,status,sync_id)
        else:
            sql = """update t_db_sync_config 
                                 set  
                                     server_id         ='{0}',
                                     sour_db_id        ='{1}',     
                                     desc_db_id        ='{2}',
                                     sync_tag          ='{3}',
                                     sync_ywlx         ='{4}',
                                     sync_type         ='{5}',
                                     comments          ='{6}',
                                     run_time          ='{7}',
                                     sync_table        ='{8}',
                                     sync_schema       ='{9}',
                                     batch_size        ='{10}',
                                     batch_size_incr   ='{11}',
                                     sync_gap          ='{12}',
                                     script_path       ='{13}',
                                     script_file       ='{14}',
                                     python3_home      ='{15}',
                                     api_server        ='{16}',
                                     sync_col_name     ='{17}',
                                     sync_col_val      ='{18}',
                                     sync_time_type    ='{19}',
                                     status            ='{20}',
                                     sync_schema_dest  ='{21}'
                               where id={22}""".format(sync_server, sour_db_server, desc_db_server,
                                                       sync_tag, sync_ywlx, sync_type,
                                                       task_desc, run_time, sync_tables,
                                                       sync_schema, sync_batch_size, sync_batch_size_incr,
                                                       sync_gap, script_base, script_name,
                                                       python3_home, api_server, sync_col_name,
                                                       sync_col_val, sync_time_type, status, sync_schema_dest,sync_id)
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

def del_sync(p_syncid):
    result={}
    try:
        db = get_connection()
        cr = db.cursor()
        sql="delete from t_db_sync_config  where id='{0}'".format(p_syncid)
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


def check_sync_repeat(p_sync):
    result = {}
    db = get_connection()
    cr = db.cursor()
    sql = """select count(0) from t_db_sync_config where sync_tag='{0}' """.format(p_sync["sync_tag"])
    print('check_sync_repeat1=', sql)
    cr.execute(sql)
    rs1 = cr.fetchone()
    sql = """select count(0) from t_db_sync_config where comments='{0}' """.format(p_sync["task_desc"])
    print('check_sync_repeat2=', sql)
    cr.execute(sql)
    rs2 = cr.fetchone()
    if rs1[0]>0:
        result['code'] = True
        result['message'] = '数据标识不能重复!'
    elif rs2[0]>0:
        result['code'] = True
        result['message'] = '同步描述不能重复!'
    else:
        result['code'] = False
        result['message'] = '!'
    cr.close()
    db.commit()
    return result

def check_sync(p_server,p_flag):
    result = {}

    if p_server["sync_server"]=="":
        result['code']='-1'
        result['message']='同步服务器不能为空！'
        return result

    if p_server["sour_db_server"]=="":
        result['code']='-1'
        result['message']='源端数据库不能为空！'
        return result

    if p_server["desc_db_server"]=="":
        result['code']='-1'
        result['message']='目标数据库不能为空！'
        return result

    if p_server["sync_tag"]=="":
        result['code']='-1'
        result['message']='同步标识号不能为空！'
        return result

    if p_server["sync_ywlx"] == "":
        result['code'] = '-1'
        result['message'] = '同步业务类型不能为空！'
        return result

    if p_server["sync_data_type"] == "":
        result['code'] = '-1'
        result['message'] = '同步数据方向不能为空！'
        return result

    if p_server["script_base"] == "":
        result['code'] = '-1'
        result['message'] = '脚本主目录不能为空！'
        return result

    if p_server["script_name"] == "":
        result['code'] = '-1'
        result['message'] = '备份脚本名不能为空！'
        return result

    if p_server["run_time"] == "":
        result['code'] = '-1'
        result['message'] = '运行时间不能为空！'
        return result

    if p_server["task_desc"] == "":
        result['code'] = '-1'
        result['message'] = '任务描述不能为空！'
        return result

    if p_server["python3_home"] == "":
        result['code'] = '-1'
        result['message'] = 'PYTHON3主目录不能为空！'
        return result

    if p_server["sync_schema"] == "":
        result['code'] = '-1'
        result['message'] = '同步数据库名不能为空！'
        return result

    if p_server["sync_tables"] == "":
        result['code'] = '-1'
        result['message'] = '同步表列表不能为空！'
        return result

    if p_server["sync_batch_size"] == "":
        result['code'] = '-1'
        result['message'] = '全量批大小不能为空！'
        return result

    if p_server["sync_batch_size_incr"] == "":
        result['code'] = '-1'
        result['message'] = '增量批大小不能为空！'
        return result

    if p_server["sync_gap"] == "":
        result['code'] = '-1'
        result['message'] = '同步间隔不能为空！'
        return result

    if p_server["sync_col_name"] == "":
        result['code'] = '-1'
        result['message'] = '新增同步列名不能为空！'
        return result

    if p_server["sync_col_val"] == "":
        result['code'] = '-1'
        result['message'] = '新增同步列值不能为空！'
        return result

    if p_server["sync_time_type"] == "":
        result['code'] = '-1'
        result['message'] = '同步时间类型不能为空！'
        return result

    if p_server["api_server"] == "":
        result['code'] = '-1'
        result['message'] = 'API服务器不能为空！'
        return result

    if p_server["status"] == "":
        result['code'] = '-1'
        result['message'] = '任务状态不能为空！'
        return result

    if p_flag == 'add':
        v = check_sync_repeat(p_server)
        if v['code']:
            result['code'] = '-1'
            result['message'] = v['message']
            return result


    result['code'] = '0'
    result['message'] = '验证通过'
    return result

def get_sync_by_syncid(p_syncid):
    db = get_connection()
    cr = db.cursor()
    sql = """select server_id,sour_db_id,desc_db_id,
                    sync_tag,sync_ywlx,sync_type,
                    script_path,script_file,run_time,
                    comments,python3_home,sync_schema,
                    sync_table,batch_size,batch_size_incr,
                    sync_gap,sync_col_name,sync_col_val,
                    sync_time_type,api_server,status,ifnull(sync_schema_dest,'')
             from t_db_sync_config where id={0}
          """.format(p_syncid)
    cr.execute(sql)
    rs = cr.fetchall()
    d_sync = {}
    d_sync['server_id']      = rs[0][0]
    d_sync['sour_db_server'] = rs[0][1]
    d_sync['desc_db_server'] = rs[0][2]
    d_sync['sync_tag']       = rs[0][3]
    d_sync['sync_ywlx']      = rs[0][4]
    d_sync['sync_data_type'] = rs[0][5]
    d_sync['script_base']    = rs[0][6]
    d_sync['script_name']    = rs[0][7]
    d_sync['run_time']       = rs[0][8]
    d_sync['task_desc']       = rs[0][9]
    d_sync['python3_home']   = rs[0][10]
    d_sync['sync_schema']    = rs[0][11]
    d_sync['sync_tables']    = rs[0][12]
    d_sync['sync_batch_size'] = rs[0][13]
    d_sync['sync_batch_size_incr'] = rs[0][14]
    d_sync['sync_gap']       = rs[0][15]
    d_sync['sync_col_name']  = rs[0][16]
    d_sync['sync_col_val']   = rs[0][17]
    d_sync['sync_time_type'] = rs[0][18]
    d_sync['api_server']     = rs[0][19]
    d_sync['status']         = rs[0][20]
    d_sync['sync_schema_dest'] = rs[0][21]
    cr.close()
    db.commit()
    print(d_sync)
    return d_sync

def push_sync_task(p_tag,p_api):
    try:
        result = {}
        result['code'] = '0'
        result['message'] = '推送成功！'
        v_cmd="curl -XPOST {0}/push_script_remote_sync -d 'tag={1}'".format(p_api,p_tag)
        r=os.popen(v_cmd).read()
        d=json.loads(r)

        if d['code']==200:
           return result
        else:
           result['code'] = '-1'
           result['message'] = '{0}!'.format(d['msg'])
           return result
    except Exception as e:
        result['code'] = '-1'
        result['message'] = '{0!'.format(str(e))
        return result

def run_sync_task(p_tag,p_api):
    try:
        result = {}
        result['code'] = '0'
        result['message'] = '执行成功！'
        v_cmd = "curl -XPOST {0}/run_script_remote_sync -d 'tag={1}'".format(p_api,p_tag)
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

def stop_sync_task(p_tag,p_api):
    try:
        result = {}
        result['code'] = '0'
        result['message'] = '执行成功！'
        v_cmd = "curl -XPOST {0}/stop_script_remote_sync -d 'tag={1}'".format(p_api,p_tag)
        print('stop_sync_task=',v_cmd)
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

def update_sync_status():
    try:
        result = {}
        result['code'] = '0'
        result['message'] = '执行成功！'
        r = os.system("curl -XPOST {0}/update_backup_status".format(get_api_server()))
        if r == 0:
            return result
        else:
            result['code'] = '-1'
            result['message'] = '执行失败！'
            return result
    except:
        result['code'] = '-1'
        result['message'] = '执行失败！'
        return result

def sync_log_query(p_param):
    pass

def sync_log_query_detail(p_param):
    pass

def query_sync_park():
    # ds  = get_ds_by_dsid()
    # db  = get_connection_ds(ds)
    db  = get_connection()
    cr  = db.cursor()
    sql = """SELECT 
                 b.sync_col_val,  
                 b.comments,
                 date_format(a.create_date,'%Y-%m-%d %H:%i:%s') as create_date,
                 concat(a.duration,''),
                 concat(a.amount,''),
                 CASE WHEN TIMESTAMPDIFF(MINUTE,a.create_date,NOW())<60 THEN '√' ELSE '×' END AS flag
            FROM t_db_sync_tasks_log a,t_db_sync_config b
            WHERE a.sync_tag = b.sync_tag 
              AND b.sync_ywlx='3' AND b.status='1'           
              AND (a.sync_tag,a.create_date) IN(
                SELECT 
                     a.sync_tag,
                     MAX(a.create_date)
                FROM t_db_sync_tasks_log a
                WHERE a.create_date>DATE_SUB(DATE(NOW()),INTERVAL 3 DAY)
                GROUP BY a.sync_tag
            )
        """
    print(sql)
    cr.execute(sql)
    v_list = []
    for r in cr.fetchall():
        v_list.append(list(r))
    cr.close()
    db.commit()
    return v_list


def query_sync_park_real_time():
    # ds  = get_ds_by_dsid()
    # db  = get_connection_ds(ds)
    db  = get_connection()
    cr  = db.cursor()
    sql = """SELECT 
                 b.sync_col_val,  
                 b.comments,
                 date_format(a.create_date,'%Y-%m-%d %H:%i:%s') as create_date,
                 concat(a.duration,''),
                 concat(a.amount,''),
                 CASE WHEN TIMESTAMPDIFF(MINUTE,a.create_date,NOW())<30 THEN '√' ELSE '×' END AS flag
            FROM t_db_sync_tasks_log a,t_db_sync_config b
            WHERE a.sync_tag = b.sync_tag 
              AND b.sync_ywlx='4' AND b.status='1'
              AND (a.sync_tag,a.create_date) IN(
                SELECT 
                     a.sync_tag,
                     MAX(a.create_date)
                FROM t_db_sync_tasks_log a
                WHERE a.create_date>DATE_SUB(DATE(NOW()),INTERVAL 3 HOUR)
                GROUP BY a.sync_tag
            )
        """
    print(sql)
    cr.execute(sql)
    v_list = []
    for r in cr.fetchall():
        v_list.append(list(r))
    cr.close()
    db.commit()
    return v_list

def query_sync_flow():
    # ds  = get_ds_by_dsid()
    # db  = get_connection_ds(ds)
    db  = get_connection()
    cr  = db.cursor()
    sql = """SELECT 
                 b.sync_col_val,  
                 b.comments,
                 date_format(a.create_date,'%Y-%m-%d %H:%i:%s') as create_date,
                 concat(a.duration,''),
                 concat(a.amount,''),
                 CASE WHEN TIMESTAMPDIFF(MINUTE,a.create_date,NOW())<60 THEN '√' ELSE '×' END AS flag
            FROM t_db_sync_tasks_log a,t_db_sync_config b
            WHERE a.sync_tag = b.sync_tag 
              AND b.sync_ywlx='1' AND b.status='1'           
              AND (a.sync_tag,a.create_date) IN(
                SELECT 
                     a.sync_tag,
                     MAX(a.create_date)
                FROM t_db_sync_tasks_log a
                WHERE a.create_date>DATE_SUB(DATE(NOW()),INTERVAL 2 DAY)
                GROUP BY a.sync_tag
            )
        """
    print(sql)
    cr.execute(sql)
    v_list = []
    for r in cr.fetchall():
        v_list.append(list(r))
    cr.close()
    db.commit()
    return v_list


def query_sync_flow_real_time():
    # ds  = get_ds_by_dsid()
    # db  = get_connection_ds(ds)
    db  = get_connection()
    cr  = db.cursor()
    sql = """SELECT 
                 b.sync_col_val,  
                 b.comments,
                 date_format(a.create_date,'%Y-%m-%d %H:%i:%s') as create_date,
                 concat(a.duration,''),
                 concat(a.amount,''),
                 CASE WHEN TIMESTAMPDIFF(MINUTE,a.create_date,NOW())<30 THEN '√' ELSE '×' END AS flag
            FROM t_db_sync_tasks_log a,t_db_sync_config b
            WHERE a.sync_tag = b.sync_tag 
              AND b.sync_ywlx='2' AND b.status='1'
              AND (a.sync_tag,a.create_date) IN(
                SELECT 
                     a.sync_tag,
                     MAX(a.create_date)
                FROM t_db_sync_tasks_log a
                WHERE a.create_date>DATE_SUB(DATE(NOW()),INTERVAL 2 HOUR)
                GROUP BY a.sync_tag
            )
        """
    print(sql)
    cr.execute(sql)
    v_list = []
    for r in cr.fetchall():
        v_list.append(list(r))
    cr.close()
    db.commit()
    return v_list

def query_sync_flow_device():
    # ds  = get_ds_by_dsid()
    # db  = get_connection_ds(ds)
    db  = get_connection()
    cr  = db.cursor()
    sql = """SELECT 
                 b.sync_col_val,  
                 b.comments,
                 date_format(a.create_date,'%Y-%m-%d %H:%i:%s') as create_date,
                 concat(a.duration,''),
                 concat(a.amount,''),
                 CASE WHEN TIMESTAMPDIFF(MINUTE,a.create_date,NOW())<30 THEN '√' ELSE '×' END AS flag
            FROM t_db_sync_tasks_log a,t_db_sync_config b
            WHERE a.sync_tag = b.sync_tag 
              AND b.sync_ywlx='5' AND b.status='1'
              AND (a.sync_tag,a.create_date) IN(
                SELECT 
                     a.sync_tag,
                     MAX(a.create_date)
                FROM t_db_sync_tasks_log a
                WHERE a.create_date>DATE_SUB(DATE(NOW()),INTERVAL 2 HOUR)
                GROUP BY a.sync_tag
            )
        """
    print(sql)
    cr.execute(sql)
    v_list = []
    for r in cr.fetchall():
        v_list.append(list(r))
    cr.close()
    db.commit()
    return v_list

def query_sync_park_charge():
    # ds  = get_ds_by_dsid()
    # db  = get_connection_ds(ds)
    db  = get_connection()
    cr  = db.cursor()
    sql = """SELECT 
                 b.sync_col_val,  
                 b.comments,
                 date_format(a.create_date,'%Y-%m-%d %H:%i:%s') as create_date,
                 concat(a.duration,''),
                 concat(a.amount,''),
                 CASE WHEN TIMESTAMPDIFF(MINUTE,a.create_date,NOW())<60 THEN '√' ELSE '×' END AS flag
            FROM t_db_sync_tasks_log a,t_db_sync_config b
            WHERE a.sync_tag = b.sync_tag 
              AND b.sync_ywlx='7' AND b.status='1'
              AND (a.sync_tag,a.create_date) IN(
                SELECT 
                     a.sync_tag,
                     MAX(a.create_date)
                FROM t_db_sync_tasks_log a
                WHERE a.create_date>DATE_SUB(DATE(NOW()),INTERVAL 1 DAY)
                GROUP BY a.sync_tag
            )
        """
    print(sql)
    cr.execute(sql)
    v_list = []
    for r in cr.fetchall():
        v_list.append(list(r))
    cr.close()
    db.commit()
    return v_list

def query_sync_bi():
    # ds  = get_ds_by_dsid()
    # db  = get_connection_ds(ds)
    db  = get_connection()
    cr  = db.cursor()
    sql = """SELECT 
                 b.sync_col_val,  
                 b.comments,
                 date_format(a.create_date,'%Y-%m-%d %H:%i:%s') as create_date,
                 concat(a.duration,''),
                 concat(a.amount,''),
                 CASE WHEN TIMESTAMPDIFF(HOUR,a.create_date,NOW())<3 THEN '√' ELSE '×' END AS flag
            FROM t_db_sync_tasks_log a,t_db_sync_config b
            WHERE a.sync_tag = b.sync_tag 
              AND b.sync_ywlx='18' AND b.status='1'
              AND (a.sync_tag,a.create_date) IN(
                SELECT 
                     a.sync_tag,
                     MAX(a.create_date)
                FROM t_db_sync_tasks_log a
                WHERE a.create_date>DATE_SUB(DATE(NOW()),INTERVAL 2 DAY)
                GROUP BY a.sync_tag
            )
        """
    print(sql)
    cr.execute(sql)
    v_list = []
    for r in cr.fetchall():
        v_list.append(list(r))
    cr.close()
    db.commit()
    return v_list