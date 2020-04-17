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
from   web.model.t_monitor   import query_monitor_index,save_index,upd_index,del_index,query_monitor_log_analyze
from   web.model.t_monitor   import get_monitor_indexes,get_monitor_indexes2,query_monitor_templete,save_templete,upd_templete,del_templete
from   web.model.t_monitor   import get_monitor_sys_indexes,get_monitor_templete_indexes,save_gather_task,query_task,push_monitor_task,run_monitor_task,stop_monitor_task
from   web.utils.basehandler import basehandler
from   web.model.t_dmmx      import get_dmm_from_dm,get_sync_server,get_templete_names,get_sync_db_server,get_gather_tasks
from   web.utils.common      import get_day_nday_ago,now

'''指标管理'''
class monitorindexquery(basehandler):
    @tornado.web.authenticated
    def get(self):
        self.render("./monitor_index.html",
                    index_types= get_dmm_from_dm('23'),
                    index_val_types=get_dmm_from_dm('24'),
                    index_db_types= get_dmm_from_dm('02'),
                    )

class monitorindex_query(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        index_code   = self.get_argument("index_code")
        v_list       = query_monitor_index(index_code)
        v_json       = json.dumps(v_list)
        self.write(v_json)


class monitorindexadd_save(basehandler):
    @tornado.web.authenticated
    def post(self):
        d_index = {}
        d_index['index_name']            = self.get_argument("index_name")
        d_index['index_code']            = self.get_argument("index_code")
        d_index['index_type']            = self.get_argument("index_type")
        d_index['index_db_type']         = self.get_argument("index_db_type")
        d_index['index_val_type']        = self.get_argument("index_val_type")
        d_index['index_threshold']       = self.get_argument("index_threshold")
        d_index['index_threshold_day']   = self.get_argument("index_threshold_day")
        d_index['index_threshold_times'] = self.get_argument("index_threshold_times")
        d_index['index_status']          = self.get_argument("index_status")
        d_index['index_trigger_time']    = self.get_argument("index_trigger_time")
        d_index['index_trigger_times']   = self.get_argument("index_trigger_times")
        print('monitorindexadd_save=',d_index)
        result=save_index(d_index)
        self.write({"code": result['code'], "message": result['message']})


class monitorindexedit_save(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        d_index = {}
        d_index['index_id']              = self.get_argument("index_id")
        d_index['index_name']            = self.get_argument("index_name")
        d_index['index_code']            = self.get_argument("index_code")
        d_index['index_type']            = self.get_argument("index_type")
        d_index['index_db_type']         = self.get_argument("index_db_type")
        d_index['index_val_type']        = self.get_argument("index_val_type")
        d_index['index_threshold']       = self.get_argument("index_threshold")
        d_index['index_threshold_day']   = self.get_argument("index_threshold_day")
        d_index['index_threshold_times'] = self.get_argument("index_threshold_times")
        d_index['index_status']          = self.get_argument("index_status")
        d_index['index_trigger_time']    = self.get_argument("index_trigger_time")
        d_index['index_trigger_times']   = self.get_argument("index_trigger_times")
        print(d_index)
        result=upd_index(d_index)
        self.write({"code": result['code'], "message": result['message']})

class monitorindexedit_del(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        index_code  = self.get_argument("index_code")
        result=del_index(index_code)
        self.write({"code": result['code'], "message": result['message']})


'''模板管理'''
class monitortempletequery(basehandler):
    @tornado.web.authenticated
    def get(self):
        self.render("./monitor_templete.html",
                    monitor_indexes=get_monitor_indexes(),
                    templete_types=get_dmm_from_dm('23'),
                    )

class monitortemplete_query(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        templete_code  = self.get_argument("templete_code")
        v_list         = query_monitor_templete(templete_code)
        v_json         = json.dumps(v_list)
        self.write(v_json)


class monitortempleteadd_save(basehandler):
    @tornado.web.authenticated
    def post(self):
        d_templete = {}
        d_templete['templete_name']    = self.get_argument("templete_name")
        d_templete['templete_code']    = self.get_argument("templete_code")
        d_templete['templete_type']    = self.get_argument("templete_type")
        d_templete['templete_indexes'] = self.get_argument("templete_indexes")
        d_templete['templete_status']  = self.get_argument("templete_status")
        print('monitortempleteadd_save=',d_templete)
        result=save_templete(d_templete)
        self.write({"code": result['code'], "message": result['message']})

class monitortempleteedit_save(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        d_templete = {}
        d_templete['templete_name']    = self.get_argument("templete_name")
        d_templete['templete_code']    = self.get_argument("templete_code")
        d_templete['templete_type'] = self.get_argument("templete_type")
        d_templete['templete_indexes'] = self.get_argument("templete_indexes")
        d_templete['templete_status']  = self.get_argument("templete_status")
        print('monitortempleteedit_save=', d_templete)
        result=upd_templete(d_templete)
        self.write({"code": result['code'], "message": result['message']})

class monitortempleteedit_del(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        templete_code  = self.get_argument("templete_code")
        result=del_templete(templete_code)
        self.write({"code": result['code'], "message": result['message']})


class monitor_sys_indexes(basehandler):
    def post(self):
        templete_code = self.get_argument("templete_code")
        result = get_monitor_sys_indexes(templete_code)
        v_json = json.dumps(result)
        self.write(v_json)

class monitor_templete_indexes(basehandler):
    def post(self):
        templete_code = self.get_argument("templete_code")
        result = get_monitor_templete_indexes(templete_code)
        v_json = json.dumps(result)
        self.write(v_json)


'''任务管理'''
class monitortaskquery(basehandler):
    @tornado.web.authenticated
    def get(self):
        self.render("./monitor_task.html",
                    gather_servers  = get_sync_server(),
                    templete_names  = get_templete_names(),
                    task_db_servers = get_sync_db_server(),
                    gather_tasks    = get_gather_tasks()
                    )

class monitortask_query(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        task_tag     = self.get_argument("task_tag")
        v_list       = query_task(task_tag)
        v_json       = json.dumps(v_list)
        self.write(v_json)


class monitortaskadd_save_gather(basehandler):
    @tornado.web.authenticated
    def post(self):
        d_task = {}
        d_task['add_gather_task_tag']           = self.get_argument("add_gather_task_tag")
        d_task['add_gather_task_desc']          = self.get_argument("add_gather_task_desc")
        d_task['add_gather_server']             = self.get_argument("add_gather_server")
        d_task['add_gather_task_db_server']     = self.get_argument("add_gather_task_db_server")
        d_task['add_gather_task_templete_name'] = self.get_argument("add_gather_task_templete_name")
        d_task['add_gather_task_run_time']      = self.get_argument("add_gather_task_run_time")
        d_task['add_gather_task_python3_home']  = self.get_argument("add_gather_task_python3_home")
        d_task['add_gather_task_script_base']   = self.get_argument("add_gather_task_script_base")
        d_task['add_gather_task_script_name']   = self.get_argument("add_gather_task_script_name")
        d_task['add_gather_task_api_server']    = self.get_argument("add_gather_task_api_server")
        d_task['add_gather_task_status']        = self.get_argument("add_gather_task_status")
        print('monitortaskadd_save_gather=',d_task)
        result=save_gather_task(d_task)
        self.write({"code": result['code'], "message": result['message']})

class monitortaskadd_save_monitor(basehandler):
    @tornado.web.authenticated
    def post(self):
        d_task = {}
        d_task['add_gather_task_tag'] = self.get_argument("add_gather_task_tag")
        d_task['add_gather_task_desc'] = self.get_argument("add_gather_task_desc")
        d_task['add_gather_server'] = self.get_argument("add_gather_server")
        d_task['add_gather_task_db_server'] = self.get_argument("add_gather_task_db_server")
        d_task['add_gather_task_templete_name'] = self.get_argument("add_gather_task_templete_name")
        d_task['add_gather_task_run_time'] = self.get_argument("add_gather_task_run_time")
        d_task['add_gather_task_python3_home'] = self.get_argument("add_gather_task_python3_home")
        d_task['add_gather_task_script_base'] = self.get_argument("add_gather_task_script_base")
        d_task['add_gather_task_script_name'] = self.get_argument("add_gather_task_script_name")
        d_task['add_gather_task_api_server'] = self.get_argument("add_gather_task_api_server")
        d_task['add_gather_task_status'] = self.get_argument("add_gather_task_status")
        print('monitortaskadd_save_gather=', d_task)
        result = save_gather_task(d_task)
        self.write({"code": result['code'], "message": result['message']})

class monitortaskedit_save(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        d_task = {}
        d_task['add_gather_task_tag'] = self.get_argument("add_gather_task_tag")
        d_task['add_gather_task_desc'] = self.get_argument("add_gather_task_desc")
        d_task['add_gather_server'] = self.get_argument("add_gather_server")
        d_task['add_gather_task_db_server'] = self.get_argument("add_gather_task_db_server")
        d_task['add_gather_task_templete_name'] = self.get_argument("add_gather_task_templete_name")
        d_task['add_gather_task_run_time'] = self.get_argument("add_gather_task_run_time")
        d_task['add_gather_task_python3_home'] = self.get_argument("add_gather_task_python3_home")
        d_task['add_gather_task_script_base'] = self.get_argument("add_gather_task_script_base")
        d_task['add_gather_task_script_name'] = self.get_argument("add_gather_task_script_name")
        d_task['add_gather_task_api_server'] = self.get_argument("add_gather_task_api_server")
        d_task['add_gather_task_status'] = self.get_argument("add_gather_task_status")
        print('monitortaskadd_save_gather=', d_task)
        result = save_gather_task(d_task)
        self.write({"code": result['code'], "message": result['message']})

class monitortaskedit_del(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        archive_id  = self.get_argument("archiveid")
        result=del_archive(archive_id)
        self.write({"code": result['code'], "message": result['message']})

class monitortaskedit_clone(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        archive_id  = self.get_argument("archiveid")
        result=del_archive(archive_id)
        self.write({"code": result['code'], "message": result['message']})

class monitortask_push(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        tag    = self.get_argument("tag")
        api    = self.get_argument("api")
        v_list = push_monitor_task(tag, api)
        v_json = json.dumps(v_list)
        self.write(v_json)

class monitortask_run(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        tag    = self.get_argument("tag")
        api    = self.get_argument("api")
        v_list = run_monitor_task(tag, api)
        v_json = json.dumps(v_list)
        self.write(v_json)

class monitortask_stop(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        tag    = self.get_argument("tag")
        api    = self.get_argument("api")
        v_list = stop_monitor_task(tag, api)
        v_json = json.dumps(v_list)
        self.write(v_json)

#图表展示
class monitorgraphquery(basehandler):
    @tornado.web.authenticated
    def get(self):
        self.render("./monitor_log_analyze.html",
                    gather_server=get_sync_server(),
                    monitor_indexes=get_monitor_indexes2(''),
                    begin_date=get_day_nday_ago(now(), 0),
                    end_date=get_day_nday_ago(now(), 0)
                    )

class monitorgraph_query(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        d_list = {}
        server_id        = self.get_argument("server_id")
        index_code       = self.get_argument("index_code")
        begin_date       = self.get_argument("begin_date")
        end_date         = self.get_argument("end_date")
        v_list1          = query_monitor_log_analyze(server_id,index_code,begin_date, end_date)
        d_list['data1']  = v_list1
        v_json = json.dumps(d_list)
        #print('monitorgraph_query=', v_json)
        self.write(v_json)
