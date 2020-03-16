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
from   web.model.t_archive import query_archive,save_archive,get_archive_by_archiveid,upd_archive,del_archive
from   web.model.t_archive import query_archive_log,push_archive_task,run_archive_task,stop_archive_task,query_archive_detail
from   web.model.t_dmmx import get_dmm_from_dm,get_sync_server,get_sync_db_server,get_sync_db_server_by_type
from   web.utils.common import current_rq2
from   web.utils.basehandler import basehandler


class transferquery(basehandler):
    @tornado.web.authenticated
    def get(self):
        self.render("./transfer_query.html"
                    )

class transfer_query(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        archive_tag   = self.get_argument("archive_tag")
        v_list   = query_archive(archive_tag)
        v_json   = json.dumps(v_list)
        self.write(v_json)

class archive_query_detail(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        archive_id   = self.get_argument("archive_id")
        v_list    = query_archive_detail(archive_id)
        v_json    = json.dumps(v_list)
        print('archive_query_detail=',v_json)
        self.write({"code": 0, "message": v_json})


class archiveadd(basehandler):
    @tornado.web.authenticated
    def get(self):
        self.render("./archive_add.html",
                    archive_server=get_sync_server(),
                    dm_db_type=get_dmm_from_dm('02'),
                    dm_archive_type=get_dmm_from_dm('09'),
                    dm_archive_time_type=get_dmm_from_dm('20'),
                    dm_archive_rentition=get_dmm_from_dm('21'),
                    )

class archiveadd_save(basehandler):
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
        d_archive['dest_db_server']       = self.get_argument("dest_db_server")
        d_archive['dest_db_name']         = self.get_argument("dest_db_name")
        d_archive['python3_home']         = self.get_argument("python3_home")
        d_archive['script_base']          = self.get_argument("script_base")
        d_archive['script_name']          = self.get_argument("script_name")
        d_archive['batch_size']           = self.get_argument("batch_size")
        d_archive['api_server']           = self.get_argument("api_server")
        d_archive['status']               = self.get_argument("status")
        print('archiveadd_save=',d_archive)
        result=save_archive(d_archive)
        self.write({"code": result['code'], "message": result['message']})

class archivechange(basehandler):
    @tornado.web.authenticated
    def get(self):
        self.render("./archive_change.html")

class archiveedit(basehandler):
    @tornado.web.authenticated
    def get(self):
        archive_id   = self.get_argument("archiveid")
        d_archive    = get_archive_by_archiveid(archive_id)
        self.render("./transfer_edit.html",
                    archive_server       = get_sync_server(),
                    dm_archive_type      = get_dmm_from_dm('09'),
                    db_server            = get_sync_db_server(),
                    archive_id           = archive_id,
                    transfer_tag         = d_archive['archive_tag'],
                    transfer_db_type     = d_archive['transfer_type'],
                    task_desc            = d_archive['task_desc'],
                    server_id            = d_archive['server_id'],
                    sour_db_id           = d_archive['sour_db_id'],
                    sour_schema          = d_archive['sour_schema'],
                    sour_table           = d_archive['sour_table'],
                    sour_where           = d_archive['sour_where'],
                    dest_db_id           = d_archive['dest_db_id'],
                    dest_schema          = d_archive['dest_schema'],
                    script_path          = d_archive['script_path'],
                    script_name          = d_archive['script_file'],
                    python3_home         = d_archive['python3_home'],
                    batch_size           = d_archive['batch_size'],
                    api_server           = d_archive['api_server'],
                    status               = d_archive['status'],
                    )

class archiveedit_save(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        d_archive = {}
        d_archive['transfer_id']     = self.get_argument("archive_id")
        d_archive['transfer_tag']    = self.get_argument("archive_tag")
        d_archive['task_desc']       = self.get_argument("task_desc")
        d_archive['transfer_server'] = self.get_argument("archive_server")
        d_archive['transfer_type']   = self.get_argument("archive_type")
        d_archive['sour_db_server']  = self.get_argument("sour_db_server")
        d_archive['sour_db_name']    = self.get_argument("sour_db_name")
        d_archive['sour_tab_name']   = self.get_argument("sour_tab_name")
        d_archive['sour_tab_where']  = self.get_argument("sour_tab_where")
        d_archive['dest_db_server']  = self.get_argument("dest_db_server")
        d_archive['dest_db_name']    = self.get_argument("dest_db_name")
        d_archive['python3_home']    = self.get_argument("python3_home")
        d_archive['script_base']     = self.get_argument("script_base")
        d_archive['script_name']     = self.get_argument("script_name")
        d_archive['batch_size']      = self.get_argument("batch_size")
        d_archive['api_server']      = self.get_argument("api_server")
        d_archive['status']          = self.get_argument("status")
        print(d_archive)
        result=upd_archive(d_archive)
        self.write({"code": result['code'], "message": result['message']})

class archiveedit_del(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        transfer_id  = self.get_argument("transferid")
        result=del_archive(transfer_id)
        self.write({"code": result['code'], "message": result['message']})

class archivelogquery(basehandler):
    @tornado.web.authenticated
    def get(self):
        self.render("./archive_log_query.html",
                    dm_proj_type=get_dmm_from_dm('05'),
                    dm_sync_ywlx=get_dmm_from_dm('08'),
                    begin_date=current_rq2(),
                    end_date=current_rq2()
                    )

class archive_log_query(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        archive_tag    = self.get_argument("archive_tag")
        market_id   = self.get_argument("market_id")
        archive_ywlx   = self.get_argument("archive_ywlx")
        begin_date  = self.get_argument("begin_date")
        end_date    = self.get_argument("end_date")
        v_list      = query_archive_log(archive_tag,market_id,archive_ywlx,begin_date,end_date)
        v_json      = json.dumps(v_list)
        self.write(v_json)

class archiveedit_push(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        tag    = self.get_argument("tag")
        api    = self.get_argument("api")
        v_list = push_archive_task(tag,api)
        v_json = json.dumps(v_list)
        self.write(v_json)

class archiveedit_run(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        tag    = self.get_argument("tag")
        api    = self.get_argument("api")
        v_list = run_archive_task(tag,api)
        v_json = json.dumps(v_list)
        self.write(v_json)

class archiveedit_stop(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        tag    = self.get_argument("tag")
        api    = self.get_argument("api")
        v_list = stop_archive_task(tag,api)
        v_json = json.dumps(v_list)
        self.write(v_json)

class archiveclone(basehandler):
    @tornado.web.authenticated
    def get(self):
        transfer_id   = self.get_argument("transfer_id")
        d_transfer    = get_archive_by_archiveid(transfer_id)
        self.render("./archive_clone.html",
                    archive_server   = get_sync_server(),
                    dm_archive_type  = get_dmm_from_dm('09'),
                    db_server         = get_sync_db_server(),
                    archive_id       = transfer_id,
                    archive_tag      = d_transfer['archive_tag'].split('_v')[0]+'_v'+str(int(d_transfer['transfer_tag'].split('_v')[1])+1),
                    archive_db_type  = d_transfer['archive_type'],
                    task_desc         = d_transfer['task_desc'].split('_v')[0]+'_v'+str(int(d_transfer['task_desc'].split('_v')[1])+1),
                    server_id         = d_transfer['server_id'],
                    sour_db_id        = d_transfer['sour_db_id'],
                    sour_schema       = d_transfer['sour_schema'],
                    sour_table        = d_transfer['sour_table'],
                    sour_where        = d_transfer['sour_where'],
                    dest_db_id        = d_transfer['dest_db_id'],
                    dest_schema       = d_transfer['dest_schema'],
                    script_path       = d_transfer['script_path'],
                    script_name       = d_transfer['script_file'],
                    python3_home      = d_transfer['python3_home'],
                    batch_size        = d_transfer['batch_size'],
                    api_server        = d_transfer['api_server'],
                    status            = d_transfer['status'],

        )

class archiveclone_save(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        d_archive = {}
        d_archive['archive_tag']    = self.get_argument("archive_tag")
        d_archive['task_desc']       = self.get_argument("task_desc")
        d_archive['archive_server'] = self.get_argument("archive_server")
        d_archive['archive_type']   = self.get_argument("archivetype")
        d_archive['sour_db_server']  = self.get_argument("sour_db_server")
        d_archive['sour_db_name']    = self.get_argument("sour_db_name")
        d_archive['sour_tab_name']   = self.get_argument("sour_tab_name")
        d_archive['sour_tab_where']  = self.get_argument("sour_tab_where")
        d_archive['dest_db_server']  = self.get_argument("dest_db_server")
        d_archive['dest_db_name']    = self.get_argument("dest_db_name")
        d_archive['python3_home']    = self.get_argument("python3_home")
        d_archive['script_base']     = self.get_argument("script_base")
        d_archive['script_name']     = self.get_argument("script_name")
        d_archive['batch_size']      = self.get_argument("batch_size")
        d_archive['api_server']      = self.get_argument("api_server")
        d_archive['status']          = self.get_argument("status")
        print('d_archiveclone_save=', d_archive)
        result = save_archive(d_archive)
        self.write({"code": result['code'], "message": result['message']})

class archivelogquery(basehandler):
    @tornado.web.authenticated
    def get(self):
        self.render("./transfer_log_query.html",
                    begin_date=current_rq2(),
                    end_date=current_rq2()
                    )

class archive_log_query(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        archive_tag    = self.get_argument("archive_tag")
        begin_date      = self.get_argument("begin_date")
        end_date        = self.get_argument("end_date")
        task_status     = self.get_argument("task_status")
        v_list          = query_archive_log(archive_tag,begin_date,end_date,task_status)
        v_json          = json.dumps(v_list)
        self.write(v_json)