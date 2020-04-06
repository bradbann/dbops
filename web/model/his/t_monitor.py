#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/3 15:46
# @Author  : 马飞
# @File    : t_user.py
# @Software: PyCharm
from web.model.t_ds        import get_ds_by_dsid,get_connection

def get_projs():
    #p_ds = get_ds_by_dsid(3)
    #db   = get_connection_ds(p_ds)
    db = get_connection()
    cr   = db.cursor()
    sql  ="""SELECT hostid,NAME FROM hosts WHERE NAME LIKE '%DB' order by name"""
    cr.execute(sql)
    v_list = []
    for r in cr.fetchall():
        v_list.append(list(r))
    cr.close()
    db.commit()
    return v_list

def query_monitor(v_bz,proj_id,start_date,end_date):
    db = get_connection()
    cr   = db.cursor()
    sql  = ''
    if v_bz == 'avg_0':
        sql  ="""SELECT DATE_FORMAT(riqi,'%Y-%m-%d') AS riqi, avg_cpu_value_0   
                   FROM monitor_zabbix_cpu 
                 WHERE host_id={0}
                  AND riqi BETWEEN '{1}' AND '{2}' order by riqi
              """.format(proj_id,start_date,end_date)

    if v_bz == 'avg_7':
        sql  ="""SELECT DATE_FORMAT(riqi,'%Y-%m-%d') AS riqi, avg_cpu_value_7   
                   FROM monitor_zabbix_cpu 
                 WHERE host_id={0}
                  AND riqi BETWEEN '{1}' AND '{2}' order by riqi
              """.format(proj_id,start_date,end_date)

    if v_bz == 'avg_20':
        sql  ="""SELECT DATE_FORMAT(riqi,'%Y-%m-%d') AS riqi, avg_cpu_value_20   
                   FROM monitor_zabbix_cpu 
                  WHERE host_id={0}
                  AND riqi BETWEEN '{1}' AND '{2}' order by riqi
              """.format(proj_id,start_date,end_date)

    if v_bz == 'max_0':
        sql = """SELECT DATE_FORMAT(riqi,'%Y-%m-%d') AS riqi, max_cpu_value_0   
                       FROM monitor_zabbix_cpu 
                     WHERE host_id={0}
                  AND riqi BETWEEN '{1}' AND '{2}' order by riqi
              """.format(proj_id,start_date,end_date)

    if v_bz == 'max_7':
        sql = """SELECT DATE_FORMAT(riqi,'%Y-%m-%d') AS riqi, max_cpu_value_7   
                       FROM monitor_zabbix_cpu 
                     WHERE host_id={0}
                  AND riqi BETWEEN '{1}' AND '{2}' order by riqi
              """.format(proj_id,start_date,end_date)

    if v_bz == 'max_20':
        sql = """SELECT DATE_FORMAT(riqi,'%Y-%m-%d') AS riqi, max_cpu_value_20   
                       FROM monitor_zabbix_cpu 
                     WHERE host_id={0}
                  AND riqi BETWEEN '{1}' AND '{2}' order by riqi
              """.format(proj_id,start_date,end_date)
    cr.execute(sql)
    v_list = []
    for r in cr.fetchall():
        v_list.append(list(r))
    cr.close()
    db.commit()
    return v_list

def query_monitor_image(proj_id,period,type):
    ds   = get_ds_by_dsid(proj_id)
    db   = get_connection()
    cr   = db.cursor()
    if period=="0":
        if type=="CPU":
            sql  ="""SELECT DATE_FORMAT(rq,'%H:%i:%s') AS rq, 
                             concat(cpu_usage_rate,'') as cpu_usage_rate  
                       FROM t_sys_usage 
                     WHERE ip='{0}' and port='{1}'
                      AND rq BETWEEN  DATE_SUB(NOW(), INTERVAL 1 HOUR) AND now() order by rq
                  """.format(ds['ip'],ds['port'])
        elif type=="Memory":
            sql = """SELECT DATE_FORMAT(rq,'%H:%i:%s') AS rq, 
                            concat(memory_usage_rate,'') as memory_usage_rate  
                      FROM t_sys_usage 
                    WHERE ip='{0}' and port='{1}'
                      AND rq BETWEEN  DATE_SUB(NOW(), INTERVAL 1 HOUR) AND now() order by rq
                  """.format(ds['ip'],ds['port'])
        elif type=="Disk(R)":
            sql = """SELECT DATE_FORMAT(rq,'%H:%i:%s') AS rq, 
                             concat(disk_read_bytes,'') as disk_read_bytes                            
                      FROM t_sys_usage 
                    WHERE ip='{0}' and port='{1}'
                      AND rq BETWEEN  DATE_SUB(NOW(), INTERVAL 1 HOUR) AND now() order by rq
                  """.format(ds['ip'],ds['port'])
        elif type == "Disk(W)":
            sql = """SELECT DATE_FORMAT(rq,'%H:%i:%s') AS rq,                                   
                             concat(disk_write_bytes,'') as disk_write_bytes  
                     FROM t_sys_usage 
                   WHERE ip='{0}' and port='{1}'
                     AND rq BETWEEN  DATE_SUB(NOW(), INTERVAL 1 HOUR) AND now() order by rq
                 """.format(ds['ip'], ds['port'])
        elif type == "Network(In)":
            sql = """SELECT DATE_FORMAT(rq,'%H:%i:%s') AS rq,                           
                            concat(net_recv_bytes,'') as net_recv_bytes  
                      FROM t_sys_usage 
                     WHERE ip='{0}' and port='{1}'
                      AND rq BETWEEN  DATE_SUB(NOW(), INTERVAL 1 HOUR) AND now() order by rq
                  """.format(ds['ip'],ds['port'])
        elif type == "Network(Out)":
            sql = """SELECT DATE_FORMAT(rq,'%H:%i:%s') AS rq, 
                            concat(net_send_bytes,'') as net_send_bytes                           
                      FROM t_sys_usage 
                     WHERE ip='{0}' and port='{1}'
                      AND rq BETWEEN  DATE_SUB(NOW(), INTERVAL 1 HOUR) AND now() order by rq
                  """.format(ds['ip'],ds['port'])
        else:
            sql=""""""

    if period=="1":
        if type=="CPU":
            sql = """SELECT DATE_FORMAT(rq,'%H:%i:%s') AS rq, 
                                concat(cpu_usage_rate,'') as cpu_usage_rate  
                          FROM t_sys_usage 
                        WHERE ip='{0}' and port='{1}'
                         AND rq BETWEEN  DATE_SUB(NOW(), INTERVAL 1 day) AND now() order by rq
                     """.format(ds['ip'],ds['port'])
        elif type=="Memory":
            sql = """SELECT DATE_FORMAT(rq,'%H:%i:%s') AS rq, 
                            concat(memory_usage_rate,'') as memory_usage_rate  
                      FROM t_sys_usage 
                    WHERE ip='{0}' and port='{1}'
                      AND rq BETWEEN  DATE_SUB(NOW(), INTERVAL 1 day) AND now() order by rq
                  """.format(ds['ip'],ds['port'])
        elif type == "Disk(R)":
            sql = """SELECT DATE_FORMAT(rq,'%H:%i:%s') AS rq, 
                            concat(disk_read_bytes,'') as disk_read_bytes                          
                      FROM t_sys_usage 
                    WHERE ip='{0}' and port='{1}'
                     AND rq BETWEEN  DATE_SUB(NOW(), INTERVAL 1 day) AND now() order by rq
                 """.format(ds['ip'],ds['port'])
        elif type == "Disk(W)":
            sql = """SELECT DATE_FORMAT(rq,'%H:%i:%s') AS rq,                            
                            concat(disk_write_bytes,'') as disk_write_bytes  
                      FROM t_sys_usage 
                    WHERE ip='{0}' and port='{1}'
                     AND rq BETWEEN  DATE_SUB(NOW(), INTERVAL 1 day) AND now() order by rq
                 """.format(ds['ip'],ds['port'])
        elif type == "Network(In)":
            sql = """SELECT DATE_FORMAT(rq,'%H:%i:%s') AS rq,                              
                              concat(net_recv_bytes,'') as net_recv_bytes  
                        FROM t_sys_usage 
                      WHERE ip='{0}' and port='{1}'
                       AND rq BETWEEN  DATE_SUB(NOW(), INTERVAL 1 day) AND now() order by rq
                   """.format(ds['ip'],ds['port'])
        elif type == "Network(Out)":
            sql = """SELECT DATE_FORMAT(rq,'%H:%i:%s') AS rq, 
                                     concat(net_send_bytes,'') as net_send_bytes
                               FROM t_sys_usage 
                             WHERE ip='{0}' and port='{1}'
                              AND rq BETWEEN  DATE_SUB(NOW(), INTERVAL 1 day) AND now() order by rq
                          """.format(ds['ip'], ds['port'])
        else:
           sql = """"""
    print(sql)
    cr.execute(sql)
    v_list = []
    for r in cr.fetchall():
        v_list.append(list(r))
    cr.close()
    db.commit()
    print("query_monitor_image=",v_list)
    return v_list

def save_sys_usage(host):
    result = {}
    try:
        db = get_connection()
        cr = db.cursor()

        sql = """insert into t_sys_usage(ip,port,rq,cpu_usage_rate,memory_usage_rate,disk_read_bytes,disk_write_bytes,net_send_bytes,net_recv_bytes) 
                 values('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}')
              """.format(host['ip'],host['port'],host['rq'],host['cpu_usage'],host['memory_usage'],
                              host['disk_read_bytes'], host['disk_write_bytes'],host['net_sent_bytes'], host['net_resv_bytes'] );
        print(sql)
        cr.execute(sql)
        cr.close()
        db.commit()
        result['code'] = '0'
        result['message'] = '保存成功！'
    except:
        result['code'] = '-1'
        result['message'] = '保存失败！'
    return result