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
from   web.model.t_monitor   import query_monitor_index,save_index,upd_index,del_index
from   web.model.t_monitor   import get_monitor_indexes,query_monitor_templete,save_templete,upd_templete,del_templete
from   web.model.t_monitor   import get_monitor_sys_indexes,get_monitor_templete_indexes,save_gather_task,query_task
from   web.utils.basehandler import basehandler
from   web.model.t_dmmx import get_dmm_from_dm,get_sync_server,get_templete_names,get_sync_db_server,get_gather_tasks

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
        print('monitorindexadd_save=',d_index)
        result=save_index(d_index)
        self.write({"code": result['code'], "message": result['message']})

# class archivechange(basehandler):
#     @tornado.web.authenticated
#     def get(self):
#         self.render("./archive_change.html")

class monitorindexedit_save(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
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
        d_archive = {}
        d_archive['archive_tag']          = self.get_argument("archive_tag")
        d_archive['task_desc']            = self.get_argument("task_desc")
        d_archive['archive_server']       = self.get_argument("archive_server")
        d_archive['archive_db_type']      = self.get_argument("archive_db_type")
        d_archive['sour_db_server']       = self.get_argument("sour_db_server")
        d_archive['sour_db_name']         = self.get_argument("sour_db_name")
        d_archive['sour_tab_name']        = self.get_argument("sour_tab_name")
        d_archive['archive_time_col']     = self.get_argument("archive_time_col")
        d_archive['archive_rentition']    = self.get_argument("archive_rentition")
        d_archive['rentition_time']       = self.get_argument("rentition_time")
        d_archive['rentition_time_type']  = self.get_argument("rentition_time_type")
        d_archive['if_cover']             = self.get_argument("if_cover")
        d_archive['dest_db_server']       = self.get_argument("dest_db_server")
        d_archive['dest_db_name']         = self.get_argument("dest_db_name")
        d_archive['python3_home']         = self.get_argument("python3_home")
        d_archive['script_base']          = self.get_argument("script_base")
        d_archive['script_name']          = self.get_argument("script_name")
        d_archive['run_time']             = self.get_argument("run_time")
        d_archive['batch_size']           = self.get_argument("batch_size")
        d_archive['api_server']           = self.get_argument("api_server")
        d_archive['status']               = self.get_argument("status")
        print('archiveadd_save=',d_archive)
        result=save_archive(d_archive)
        self.write({"code": result['code'], "message": result['message']})

class monitortaskedit_save(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        d_archive = {}
        d_archive['archive_id']          = self.get_argument("archive_id")
        d_archive['archive_tag']         = self.get_argument("archive_tag")
        d_archive['task_desc']           = self.get_argument("task_desc")
        d_archive['archive_server']      = self.get_argument("archive_server")
        d_archive['archive_db_type']     = self.get_argument("archive_db_type")
        d_archive['sour_db_server']      = self.get_argument("sour_db_server")
        d_archive['sour_db_name']        = self.get_argument("sour_db_name")
        d_archive['sour_tab_name']       = self.get_argument("sour_tab_name")
        d_archive['archive_time_col']    = self.get_argument("archive_time_col")
        d_archive['archive_rentition']   = self.get_argument("archive_rentition")
        d_archive['rentition_time']      = self.get_argument("rentition_time")
        d_archive['rentition_time_type'] = self.get_argument("rentition_time_type")
        d_archive['if_cover']            = self.get_argument("if_cover")
        d_archive['dest_db_server']      = self.get_argument("dest_db_server")
        d_archive['dest_db_name']        = self.get_argument("dest_db_name")
        d_archive['python3_home']        = self.get_argument("python3_home")
        d_archive['script_base']         = self.get_argument("script_base")
        d_archive['script_name']         = self.get_argument("script_name")
        d_archive['run_time']            = self.get_argument("run_time")
        d_archive['batch_size']          = self.get_argument("batch_size")
        d_archive['api_server']          = self.get_argument("api_server")
        d_archive['status']              = self.get_argument("status")
        print(d_archive)
        result=upd_archive(d_archive)
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
        archive_id  = self.get_argument("archiveid")
        result=del_archive(archive_id)
        self.write({"code": result['code'], "message": result['message']})

class monitortask_run(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        archive_id  = self.get_argument("archiveid")
        result=del_archive(archive_id)
        self.write({"code": result['code'], "message": result['message']})

class monitortask_stop(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        archive_id  = self.get_argument("archiveid")
        result=del_archive(archive_id)
        self.write({"code": result['code'], "message": result['message']})

#图表展示
class monitorgraphquery(basehandler):
    @tornado.web.authenticated
    def get(self):
        self.render("./monitor_task.html")

class monitorgraph_query(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        archive_tag  = self.get_argument("archive_tag")
        v_list       = query_archive(archive_tag)
        v_json       = json.dumps(v_list)
        self.write(v_json)
