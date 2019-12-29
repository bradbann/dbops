#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/9/5 16:08
# @Author : 马飞
# @File : ds.py
# @Software: PyCharm
######################################################################################
#                                                                                    #
#                                   数据库备份管理                                        #
#                                                                                    #
######################################################################################

import json
import tornado.web
from   web.model.t_sync import query_sync,save_sync,get_sync_by_syncid,upd_sync,del_sync,query_sync_log,query_sync_log_detail
from   web.model.t_sync import push_sync_task,run_sync_task,stop_sync_task,update_sync_status,query_sync_log_analyze,query_sync_log_analyze2
from   web.model.t_dmmx import get_dmm_from_dm,get_sync_server,get_sync_db_server,get_db_sync_tags,get_db_sync_tags_by_market_id,get_db_sync_ywlx,get_db_sync_ywlx_by_market_id
from   web.model.t_xtqx import get_db_name
from   web.utils.common import current_rq2,get_day_nday_ago,now

class syncbigdataquery(tornado.web.RequestHandler):
    def get(self):
        self.render("./sync_query.html",
                    dm_proj_type = get_dmm_from_dm('05'),
                    dm_sync_ywlx = get_dmm_from_dm('08'),
                    dm_sync_data_type = get_dmm_from_dm('09'),
                    )

class sync_bigdata_query(tornado.web.RequestHandler):
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        sync_tag   = self.get_argument("sync_tag")
        market_id  = self.get_argument("market_id")
        sync_ywlx  = self.get_argument("sync_ywlx")
        sync_type  = self.get_argument("sync_type")
        v_list   = query_sync(sync_tag,market_id,sync_ywlx,sync_type)
        v_json   = json.dumps(v_list)
        self.write(v_json)

class syncadd_bigdata(tornado.web.RequestHandler):
    def get(self):
        self.render("./sync_bigdata_add.html",
                    sync_server = get_sync_server(),
                    db_server   = get_sync_db_server(),
                    dm_db_type  = get_dmm_from_dm('02'),
                    dm_sync_ywlx= get_dmm_from_dm('08'),
                    dm_sync_data_type = get_dmm_from_dm('09'),
                    dm_sync_time_type = get_dmm_from_dm('10')
                    )

class syncadd_bigdata_save(tornado.web.RequestHandler):
    def post(self):
        d_sync = {}
        d_sync['sync_server']          = self.get_argument("sync_server")
        d_sync['sour_db_server']       = self.get_argument("sour_db_server")
        d_sync['desc_db_server']       = self.get_argument("desc_db_server")
        d_sync['sync_tag']             = self.get_argument("sync_tag")
        d_sync['sync_ywlx']            = self.get_argument("sync_ywlx")
        d_sync['sync_data_type']       = self.get_argument("sync_data_type")
        d_sync['script_base']          = self.get_argument("script_base")
        d_sync['script_name']          = self.get_argument("script_name")
        d_sync['run_time']             = self.get_argument("run_time")
        d_sync['task_desc']            = self.get_argument("task_desc")
        d_sync['python3_home']         = self.get_argument("python3_home")
        d_sync['sync_schema']          = self.get_argument("sync_schema")
        d_sync['sync_tables']          = self.get_argument("sync_tables")
        d_sync['sync_batch_size']      = self.get_argument("sync_batch_size")
        d_sync['sync_batch_size_incr'] = self.get_argument("sync_batch_size_incr")
        d_sync['sync_gap']             = self.get_argument("sync_gap")
        d_sync['sync_col_name']        = self.get_argument("sync_col_name")
        d_sync['sync_col_val']         = self.get_argument("sync_col_val")
        d_sync['sync_time_type']       = self.get_argument("sync_time_type")
        d_sync['api_server']           = self.get_argument("api_server")
        d_sync['status']               = self.get_argument("status")
        print('syncadd_save=',d_sync)
        result=save_sync(d_sync)
        self.write({"code": result['code'], "message": result['message']})

class syncchange(tornado.web.RequestHandler):
    def get(self):
        self.render("./sync_change.html" ,
                    dm_proj_type = get_dmm_from_dm('05'),
                    dm_sync_ywlx = get_dmm_from_dm('08'),
                    dm_sync_data_type = get_dmm_from_dm('09'),)

class syncedit(tornado.web.RequestHandler):
    def get(self):
        sync_id   = self.get_argument("sync_id")
        d_sync    = get_sync_by_syncid(sync_id)
        self.render("./sync_edit.html",
                    sync_id              = sync_id,
                    sync_server          = get_sync_server(),
                    db_server            = get_sync_db_server(),
                    dm_db_type           = get_dmm_from_dm('02'),
                    dm_sync_ywlx         = get_dmm_from_dm('08'),
                    dm_sync_data_type    = get_dmm_from_dm('09'),
                    dm_sync_time_type    = get_dmm_from_dm('10'),
                    server_id            = d_sync['server_id'],
                    sour_db_server       = d_sync['sour_db_server'],
                    desc_db_server       = d_sync['desc_db_server'],
                    sync_tag             = d_sync['sync_tag'],
                    sync_ywlx            = d_sync['sync_ywlx'],
                    sync_data_type       = d_sync['sync_data_type'],
                    script_base          = d_sync['script_base'],
                    script_name          = d_sync['script_name'],
                    run_time             = d_sync['run_time'],
                    task_desc            = d_sync['task_desc'],
                    python3_home         = d_sync['python3_home'],
                    sync_schema          = d_sync['sync_schema'],
                    sync_tables          = d_sync['sync_tables'],
                    sync_batch_size      = d_sync['sync_batch_size'],
                    sync_batch_size_incr = d_sync['sync_batch_size_incr'],
                    sync_gap             = d_sync['sync_gap'],
                    sync_col_name        = d_sync['sync_col_name'],
                    sync_col_val         = d_sync['sync_col_val'],
                    sync_time_type       = d_sync['sync_time_type'],
                    api_server           = d_sync['api_server'],
                    status               = d_sync['status'],
                    )

class syncedit_save(tornado.web.RequestHandler):
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        d_sync = {}
        d_sync['sync_server']     = self.get_argument("sync_server")
        d_sync['sour_db_server']  = self.get_argument("sour_db_server")
        d_sync['desc_db_server']  = self.get_argument("desc_db_server")
        d_sync['sync_tag']        = self.get_argument("sync_tag")
        d_sync['sync_ywlx']       = self.get_argument("sync_ywlx")
        d_sync['sync_data_type']  = self.get_argument("sync_data_type")
        d_sync['script_base']     = self.get_argument("script_base")
        d_sync['script_name']     = self.get_argument("script_name")
        d_sync['run_time']        = self.get_argument("run_time")
        d_sync['task_desc']       = self.get_argument("task_desc")
        d_sync['python3_home']    = self.get_argument("python3_home")
        d_sync['sync_schema']     = self.get_argument("sync_schema")
        d_sync['sync_tables']     = self.get_argument("sync_tables")
        d_sync['sync_batch_size'] = self.get_argument("sync_batch_size")
        d_sync['sync_batch_size_incr'] = self.get_argument("sync_batch_size_incr")
        d_sync['sync_gap']       = self.get_argument("sync_gap")
        d_sync['sync_col_name']  = self.get_argument("sync_col_name")
        d_sync['sync_col_val']   = self.get_argument("sync_col_val")
        d_sync['sync_time_type'] = self.get_argument("sync_time_type")
        d_sync['api_server']     = self.get_argument("api_server")
        d_sync['status']         = self.get_argument("status")
        d_sync['sync_id']        = self.get_argument("sync_id")
        print(d_sync)
        result=upd_sync(d_sync)
        self.write({"code": result['code'], "message": result['message']})

class syncedit_del(tornado.web.RequestHandler):
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        syncid  = self.get_argument("syncid")
        result=del_sync(syncid)
        self.write({"code": result['code'], "message": result['message']})

class synclogquery(tornado.web.RequestHandler):
    def get(self):
        self.render("./sync_log_query.html",
                    dm_proj_type=get_dmm_from_dm('05'),
                    dm_sync_ywlx=get_dmm_from_dm('08'),
                    begin_date=current_rq2(),
                    end_date=current_rq2()
                    )

class sync_log_query(tornado.web.RequestHandler):
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        sync_tag    = self.get_argument("sync_tag")
        market_id   = self.get_argument("market_id")
        sync_ywlx   = self.get_argument("sync_ywlx")
        begin_date  = self.get_argument("begin_date")
        end_date    = self.get_argument("end_date")
        v_list      = query_sync_log(sync_tag,market_id,sync_ywlx,begin_date,end_date)
        v_json      = json.dumps(v_list)
        self.write(v_json)


class sync_log_query_detail(tornado.web.RequestHandler):
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        sync_tag = self.get_argument("sync_tag")
        sync_rqq = self.get_argument("sync_rqq")
        sync_rqz = self.get_argument("sync_rqz")
        v_list=query_sync_log_detail(sync_tag,sync_rqq,sync_rqz)
        print('sync_log_query_detail=>result=',v_list)
        v_json = json.dumps(v_list)
        self.write(v_json)


class syncloganalyze(tornado.web.RequestHandler):
    def get(self):
        print('begin_date=',get_day_nday_ago(now(),15),get_day_nday_ago(now(),0))
        self.render("./sync_log_analyze.html",
                      dm_proj_type = get_dmm_from_dm('05'),
                      db_sync_tags = get_db_sync_tags(),
                      begin_date=get_day_nday_ago(now(),0),
                      end_date=get_day_nday_ago(now(),0)
                    )

class sync_log_analyze(tornado.web.RequestHandler):
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        market_id  = self.get_argument("market_id")
        tagname    = self.get_argument("tagname")
        begin_date = self.get_argument("begin_date")
        end_date   = self.get_argument("end_date")
        d_list     = {}
        v_list1,v_list2 = query_sync_log_analyze(market_id,tagname,begin_date,end_date)
        d_list['data1'] = v_list1
        d_list['data2'] = v_list2
        v_json = json.dumps(d_list)
        print('backup_log_analyze=',v_json)
        self.write(v_json)

class syncloganalyze2(tornado.web.RequestHandler):
    def get(self):
        print('begin_date=',get_day_nday_ago(now(),15),get_day_nday_ago(now(),0))
        self.render("./sync_log_analyze2.html",
                      dm_proj_type = get_dmm_from_dm('05'),
                      db_sync_ywlx = get_db_sync_ywlx(),
                      begin_date   = get_day_nday_ago(now(),0),
                      end_date     = get_day_nday_ago(now(),0)
                    )

class sync_log_analyze2(tornado.web.RequestHandler):
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        market_id  = self.get_argument("market_id")
        sync_type  = self.get_argument("sync_type")
        begin_date = self.get_argument("begin_date")
        end_date   = self.get_argument("end_date")
        d_list     = {}
        v_list1,v_list2 = query_sync_log_analyze2(market_id,sync_type,begin_date,end_date)
        d_list['data1'] = v_list1
        d_list['data2'] = v_list2
        v_json = json.dumps(d_list)
        print('backup_log_analyze=',v_json)
        self.write(v_json)

class get_sync_tasks(tornado.web.RequestHandler):
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        market_id = self.get_argument("market_id")
        d_list  = {}
        v_list  = get_db_sync_tags_by_market_id(market_id)
        d_list['data'] = v_list
        v_json  = json.dumps(d_list)
        print('get_sync_tasks=', v_json)
        self.write(v_json)

class get_sync_ywlx(tornado.web.RequestHandler):
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        market_id = self.get_argument("market_id")
        d_list  = {}
        v_list  = get_db_sync_ywlx_by_market_id(market_id)
        d_list['data'] = v_list
        v_json  = json.dumps(d_list)
        print('get_sync_tasks=', v_json)
        self.write(v_json)


class syncedit_push(tornado.web.RequestHandler):
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        tag    = self.get_argument("tag")
        api    = self.get_argument("api")
        v_list = push_sync_task(tag,api)
        v_json = json.dumps(v_list)
        self.write(v_json)

class syncedit_run(tornado.web.RequestHandler):
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        tag    = self.get_argument("tag")
        api    = self.get_argument("api")
        v_list = run_sync_task(tag,api)
        v_json = json.dumps(v_list)
        self.write(v_json)

class syncedit_stop(tornado.web.RequestHandler):
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        tag    = self.get_argument("tag")
        api    = self.get_argument("api")
        v_list = stop_sync_task(tag,api)
        v_json = json.dumps(v_list)
        self.write(v_json)

class syncedit_status(tornado.web.RequestHandler):
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        v_list = update_sync_status()
        v_json = json.dumps(v_list)
        print('backupedit_status=',v_json)
        self.write(v_json)