#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/12/6 9:17
# @Author : 马飞
# @File : urls.py.py
# @Software: PyCharm

from web.services.logon        import index,main,logon,logout,logon_check,get_tree,get_time,get_verify,error, lockscreen,unlock,heartbeat
from web.services.user         import userquery,useradd,useradd_save,useradd_save_uploadImage,userchange,useredit,useredit_save,useredit_del,user_query,projectquery,project_query,projectprivs_save
from web.services.role         import rolequery,roleadd,roleadd_save,role_query,rolechange,roleedit,roleedit_save,roleedit_del
from web.services.menu         import menuquery,menu_query,menuadd,menuadd_save,menuchange,menuedit,menuedit_save,menuedit_del
from web.services.func         import funcquery,func_query,funcadd,funcadd_save,funcchange,funcedit,funcedit_save,funcedit_del
from web.services.ds           import dsquery,ds_query_id,ds_query,dsadd,dsadd_save,dschange,dsedit,dsedit_save,dsedit_del,dstest,ds_check_valid,dsclone,dsclone_save,get_db_by_type
from web.services.server       import serverquery,server_query,serveradd,serveradd_save,serverchange,serveredit,serveredit_save,serveredit_del
from web.services.backup       import backupquery,backup_query,backup_case,backupadd,backupadd_save,backupchange,backupedit,backupedit_save,backupedit_del,backuplogquery
from web.services.backup       import backup_log_query,backup_log_query_detail,backupedit_push,backupedit_run,backupedit_stop,backupedit_status,backuploganalyze,backup_log_analyze,get_backup_tasks
from web.services.sync         import syncadd,syncadd_save,syncquery,sync_query,syncchange,syncedit,syncedit_save,syncclone,syncclone_save,syncedit_del,synclogquery
from web.services.sync         import sync_log_query,sync_log_query_detail,syncedit_push,syncedit_run,syncedit_stop,syncloganalyze,sync_log_analyze,get_sync_tasks
from web.services.sync         import get_sync_park,get_sync_park_real_time,get_sync_flow,get_sync_flow_real_time,get_sync_flow_device,get_sync_park_charge,get_sync_bi
from web.services.transfer     import transferadd,transferadd_save,transferchange,transferedit,transferedit_save,transferedit_del,transfer_query,transferedit_push,transferedit_run,transferedit_stop
from web.services.transfer     import transferquery,transferclone,transferclone_save,transferlogquery,transfer_log_query,transfer_query_detail
from web.services.sql          import orderquery,order_query,sqlquery,sql_query,sqlrelease,sql_check,sql_format,sql_check_result,sql_release,sqlaudit,sql_audit,sqlrun,sql_run,sql_audit_query,sql_audit_detail,sql_run_query
from web.services.sql          import get_tree_by_sql,get_tab_ddl,get_tab_idx,alt_tab,get_database,get_tables,get_columns,get_tab_stru,get_keys,get_incr_col,get_ds
from web.services.sql          import wtd_save,wtd_release,wtd_update,wtd_delete,get_order_no,wtd_query,wtd_detail,get_order_env,get_order_type,get_order_status,get_order_handler,wtd_save_uploadImage,wtd_attachment,wtd_attachment_number
from web.services.sys          import audit_rule,audit_rule_save,sys_setting,sys_code,sys_code_type_query,sys_code_detail_query,sys_test,sys_query_rule,sys_code_type_add_save,sys_code_type_upd_save,sys_code_type_del
from web.services.sys          import sys_code_detail_add_save,sys_code_detail_upd_save,sys_code_detail_del,sys_code_type
from web.services.sync_bigdata import syncadd_bigdata,syncadd_bigdata_save,syncbigdataquery,sync_bigdata_query,sync_bigdata_query_detail,sync_bigdata_query_dataxTemplete
from web.services.sync_bigdata import sync_bigdata_downloads_dataxTemplete,syncchange_bigdata,syncedit_bigdata,syncedit_save_bigdata,syncedit_del_bigdata,syncedit_push_bigdata
from web.services.sync_bigdata import syncedit_pushall_bigdata,syncedit_run_bigdata,syncedit_stop_bigdata,syncclone_bigdata,syncclone_save_bigdata,syncloganalyze_bigdata,sync_log_analyze_bigdata,get_bigdata_sync_tasks
from web.services.port         import portadd,portadd_save,portchange,portedit,portedit_save,portedit_del,port_query,portquery,portedit_imp,portedit_exp
from web.services.archive      import archiveadd,archiveadd_save,archivequery,archive_query,archive_query_detail,archivechange,archiveedit,archiveedit_save
from web.services.archive      import archiveedit_del,archiveedit_push,archiveedit_run,archiveedit_stop,archiveclone,archiveclone_save,archivelogquery,archive_log_query
from web.services.dbtools      import dict_gen,redis_migrate
from web.services.monitor      import monitorindexquery,monitorindex_query,monitorindexadd_save,monitorindexedit_save,monitorindexedit_del,monitortaskupd_save_gather,monitortaskupd_save_monitor
from web.services.monitor      import monitortempletequery,monitortemplete_query,monitortempleteadd_save,monitortempleteedit_save,monitortempleteedit_del,monitor_sys_indexes,monitor_templete_indexes
from web.services.monitor      import monitortaskquery,monitortask_query,monitortaskadd_save_gather,monitortaskadd_save_monitor,monitortaskedit_del,monitortask_push,monitortask_run,monitortask_stop
from web.services.monitor      import monitorgraphquery,monitorgraph_query,get_monitor_templete_type,get_monitor_db,get_monitor_index,get_monitor_task,get_monitor_view,get_monitor_view_sys,get_monitor_view_svr
from web.services.db_inst      import dbinstquery,db_inst_query,db_inst_save,db_inst_update,db_inst_query_by_id,dbinstmgr,get_tree_by_inst,db_inst_sql_query,db_inst_delete,get_inst_tab_ddl,get_inst_idx_ddl,drop_inst_tab
from web.services.db_inst      import dbinstcrtquery,db_inst_crt_query,db_inst_create,db_inst_destroy,db_inst_log,db_inst_manager
from web.services.db_inst      import dbinstparaquery,dbinstpara_query,dbinstparaadd_save,dbinstparaedit_save,dbinstparaedit_del,dbinstoptlogquery,dbinstoptlog_query
from web.services.db_user      import dbuserquery,db_user_query,db_user_save,db_user_update,db_user_delete,db_user_sql,db_user_dbs,db_user_info,db_user_query_by_id
from web.services.db_config    import dbinstcfgquery,db_inst_cfg_query,db_inst_cfg_update
from web.services.slow         import slowquery,slowadd,slowadd_save,slow_query,slowchange,slowedit_save,slowedit_del,slow_query_by_id,slowedit_push
from web.services.minio        import minioquery,minio_query,minioadd,minioadd_save,miniochange,minioedit,minioedit_save,minioedit_del,miniologquery,minioedit_push,minioclone


urls = [
        # 功能：主页面API
        (r"/login",                          logon),
        (r"/unlock",                         unlock),
        (r"/logout",                         logout),
        (r"/error",                          error),
        (r"/lockscreen",                     lockscreen),
        (r"/",                               index),
        (r"/main",                           main),
        (r"/tree",                           get_tree),
        (r"/get_verify",                     get_verify),
        (r"/logon_check",                    logon_check),
        (r"/time",                           get_time),
        (r"/heartbeat",                      heartbeat),

        # 功能：公用API
        (r"/get_tab_ddl",                    get_tab_ddl),
        (r"/get_tab_idx",                    get_tab_idx),
        (r"/get_database",                   get_database),
        (r"/get_tables",                     get_tables),
        (r"/get_columns",                    get_columns),
        (r"/get_keys",                       get_keys),
        (r"/get_incr_col",                   get_incr_col),
        (r"/get_tab_stru",                   get_tab_stru),
        (r"/get_ds",                         get_ds),
        (r"/alt_tab",                        alt_tab),

        # 功能：主面板API
        (r"/backup_case",                    backup_case),
        (r"/get/sync/park",                  get_sync_park),
        (r"/get/sync/park/realtime",         get_sync_park_real_time),
        (r"/get/sync/flow",                  get_sync_flow),
        (r"/get/sync/flow/realtime",         get_sync_flow_real_time),
        (r"/get/sync/flow/device",           get_sync_flow_device),
        (r"/get/sync/park/charge",           get_sync_park_charge),
        (r"/get/sync/bi",                    get_sync_bi),

        # 功能：用户管理API
        (r"/user/query",                     userquery),
        (r"/user/_query",                    user_query),
        (r"/user/add",                       useradd),
        (r"/user/add/save",                  useradd_save),
        (r"/user/add/uploadImage",           useradd_save_uploadImage),
        (r"/user/change",                    userchange),
        (r"/user/edit"  ,                    useredit),
        (r"/user/edit/save",                 useredit_save),
        (r"/user/edit/del",                  useredit_del),
        (r"/project/query",                  projectquery),
        (r"/project/_query",                 project_query),
        (r"/project/privs/save" ,            projectprivs_save),

        # 功能：角色管理API
        (r"/role/query",                     rolequery),
        (r"/role/_query",                    role_query),
        (r"/role/add"   ,                    roleadd),
        (r"/role/add/save",                  roleadd_save),
        (r"/role/change",                    rolechange),
        (r"/role/edit"  ,                    roleedit),
        (r"/role/edit/save",                 roleedit_save),
        (r"/role/edit/del" ,                 roleedit_del),

        # 功能：菜单管理API
        (r"/menu/query",                     menuquery),
        (r"/menu/_query",                    menu_query),
        (r"/menu/add",                       menuadd),
        (r"/menu/add/save",                  menuadd_save),
        (r"/menu/change",                    menuchange),
        (r"/menu/edit",                      menuedit),
        (r"/menu/edit/save",                 menuedit_save),
        (r"/menu/edit/del",                  menuedit_del),

        # 功能：功能管理API
        (r"/func/query",                     funcquery),
        (r"/func/_query",                    func_query),
        (r"/func/add",                       funcadd),
        (r"/func/add/save",                  funcadd_save),
        (r"/func/change",                    funcchange),
        (r"/func/edit",                      funcedit),
        (r"/func/edit/save",                 funcedit_save),
        (r"/func/edit/del",                  funcedit_del),

        # 功能：数据源管理API
        (r"/ds/query",                       dsquery),
        (r"/ds/query/id",                    ds_query_id),
        (r"/ds/_query",                      ds_query),
        (r"/ds/add",                         dsadd),
        (r"/ds/add/save",                    dsadd_save),
        (r"/ds/change",                      dschange),
        (r"/ds/edit",                        dsedit),
        (r"/ds/edit/save",                   dsedit_save),
        (r"/ds/clone",                       dsclone),
        (r"/ds/clone/save",                  dsclone_save),
        (r"/ds/edit/del",                    dsedit_del),
        (r"/ds/test",                        dstest),
        (r"/ds/check/valid",                 ds_check_valid),
        (r"/ds/get/db/type",                 get_db_by_type),


        # 功能：服务器管理API
        (r"/server/query",                   serverquery),
        (r"/server/_query",                  server_query),
        (r"/server/add",                     serveradd),
        (r"/server/add/save",                serveradd_save),
        (r"/server/change",                  serverchange),
        (r"/server/edit",                    serveredit),
        (r"/server/edit/save",               serveredit_save),
        (r"/server/edit/del",                serveredit_del),

        # 功能：数据库操作API
        (r"/sql/query",                      sqlquery),
        (r"/sql/_query",                     sql_query),
        (r"/sql/release",                    sqlrelease),
        (r"/sql/_release",                   sql_release),
        (r"/sql/_check",                     sql_check),
        (r"/sql/_check/result",              sql_check_result),
        (r"/sql/audit",                      sqlaudit),
        (r"/sql/_audit",                     sql_audit),
        (r"/sql/audit/query",                sql_audit_query),
        (r"/sql/audit/detail",               sql_audit_detail),
        (r"/sql/_format",                    sql_format),
        (r"/sql/run",                        sqlrun),
        (r"/sql/_run",                       sql_run),
        (r"/sql/run/query",                  sql_run_query),
        (r"/get_tree",                       get_tree_by_sql),

        # 功能：我的工单API
        (r"/order/query",                    orderquery),
        (r"/order/_query",                   order_query),
        (r"/wtd/_query",                     wtd_query),
        (r"/wtd/detail",                     wtd_detail),
        (r"/get/order/no",                   get_order_no),
        (r"/wtd/save",                       wtd_save),
        (r"/wtd/save/uploadImage",           wtd_save_uploadImage),
        (r"/wtd/release",                    wtd_release),
        (r"/wtd/update",                     wtd_update),
        (r"/wtd/delete",                     wtd_delete),
        (r"/wtd/attachment",                 wtd_attachment),
        (r"/wtd/attachment/number",          wtd_attachment_number),
        (r"/get_order_env",                  get_order_env),
        (r"/get_order_type",                 get_order_type),
        (r"/get_order_status",               get_order_status),
        (r"/get_order_handler",              get_order_handler),

        # 功能：数据库备份API
        (r"/backup/query",                   backupquery),
        (r"/backup/_query",                  backup_query),
        (r"/backup/add",                     backupadd),
        (r"/backup/add/save",                backupadd_save),
        (r"/backup/change",                  backupchange),
        (r"/backup/edit",                    backupedit),
        (r"/backup/edit/save",               backupedit_save),
        (r"/backup/edit/del",                backupedit_del),
        (r"/backup/edit/push",               backupedit_push),
        (r"/backup/edit/run" ,               backupedit_run),
        (r"/backup/edit/stop" ,              backupedit_stop),
        (r"/backup/edit/status",             backupedit_status),
        (r"/backup/log/query",               backuplogquery),
        (r"/backup/log/_query",              backup_log_query),
        (r"/backup/log/_query/detail",       backup_log_query_detail),
        (r"/backup/log/analyze",             backuploganalyze),
        (r"/backup/log/_analyze",            backup_log_analyze),
        (r"/get/backup/task"    ,            get_backup_tasks),

        # 功能：数据库同步API
        (r"/sync/query",                     syncquery),
        (r"/sync/_query",                    sync_query),
        (r"/sync/add",                       syncadd),
        (r"/sync/add/save",                  syncadd_save),
        (r"/sync/change"  ,                  syncchange),
        (r"/sync/edit"    ,                  syncedit),
        (r"/sync/edit/save",                 syncedit_save),
        (r"/sync/clone",                     syncclone),
        (r"/sync/clone/save",                syncclone_save),
        (r"/sync/edit/del" ,                 syncedit_del),
        (r"/sync/edit/push",                 syncedit_push),
        (r"/sync/edit/run" ,                 syncedit_run),
        (r"/sync/edit/stop",                 syncedit_stop),
        (r"/sync/log/query"  ,               synclogquery),
        (r"/sync/log/_query" ,               sync_log_query),
        (r"/sync/log/_query/detail",         sync_log_query_detail),
        (r"/sync/log/analyze",               syncloganalyze),
        (r"/sync/log/_analyze",              sync_log_analyze),
        (r"/get/sync/task",                  get_sync_tasks),

        # 功能：数据库传输API
        (r"/transfer/query",                 transferquery),
        (r"/transfer/_query",                transfer_query),
        (r"/transfer/_query/detail",         transfer_query_detail),
        (r"/transfer/add",                   transferadd),
        (r"/transfer/add/save",              transferadd_save),
        (r"/transfer/change"  ,              transferchange),
        (r"/transfer/edit"    ,              transferedit),
        (r"/transfer/edit/save",             transferedit_save),
        (r"/transfer/edit/del" ,             transferedit_del),
        (r"/transfer/edit/push",             transferedit_push),
        (r"/transfer/edit/run" ,             transferedit_run),
        (r"/transfer/edit/stop",             transferedit_stop),
        (r"/transfer/clone",                 transferclone),
        (r"/transfer/clone/save",            transferclone_save),
        (r"/transfer/log/query",             transferlogquery),
        (r"/transfer/log/_query",            transfer_log_query),

        # 功能：大数据管理API
        (r"/bigdata/add",                    syncadd_bigdata),
        (r"/bigdata/add/save",               syncadd_bigdata_save),
        (r"/bigdata/query",                  syncbigdataquery),
        (r"/bigdata/_query",                 sync_bigdata_query),
        (r"/bigdata/_query/detail",          sync_bigdata_query_detail),
        (r"/bigdata/_query/templete",        sync_bigdata_query_dataxTemplete),
        (r"/bigdata/_query/downloads",       sync_bigdata_downloads_dataxTemplete),
        (r"/bigdata/change",                 syncchange_bigdata),
        (r"/bigdata/edit",                   syncedit_bigdata),
        (r"/bigdata/edit/save",              syncedit_save_bigdata),
        (r"/bigdata/edit/del",               syncedit_del_bigdata),
        (r"/bigdata/clone",                  syncclone_bigdata),
        (r"/bigdata/clone/save",             syncclone_save_bigdata),
        (r"/bigdata/edit/push",              syncedit_push_bigdata),
        (r"/bigdata/edit/pushall",           syncedit_pushall_bigdata),
        (r"/bigdata/edit/run",               syncedit_run_bigdata),
        (r"/bigdata/edit/stop",              syncedit_stop_bigdata),
        (r"/bigdata/log/analyze",            syncloganalyze_bigdata),
        (r"/bigdata/log/_analyze",           sync_log_analyze_bigdata),
        (r"/get/bigdata/sync/task",          get_bigdata_sync_tasks),

        # 功能：端口管理API
        (r"/port/query",                     portquery),
        (r"/port/_query",                    port_query),
        (r"/port/add",                       portadd),
        (r"/port/add/save",                  portadd_save),
        (r"/port/change",                    portchange),
        (r"/port/edit",                      portedit),
        (r"/port/edit/save",                 portedit_save),
        (r"/port/edit/del",                  portedit_del),
        (r"/port/edit/imp",                  portedit_imp),
        (r"/port/edit/exp",                  portedit_exp),

        # 功能：系统设置API
        (r"/sys/audit_rule",                 audit_rule),
        (r"/sys/query_rule",                 sys_query_rule),
        (r"/sys/audit_rule/save",            audit_rule_save),
        (r"/sys/setting",                    sys_setting),
        (r"/sys/code",                       sys_code),
        (r"/sys/code/type/_query",           sys_code_type_query),
        (r"/sys/code/detail/_query",         sys_code_detail_query),
        (r"/sys/code/type/add/save",         sys_code_type_add_save),
        (r"/sys/code/type/upd/save",         sys_code_type_upd_save),
        (r"/sys/code/type/del",              sys_code_type_del),
        (r"/sys/code/detail/add/save",       sys_code_detail_add_save),
        (r"/sys/code/detail/upd/save",       sys_code_detail_upd_save),
        (r"/sys/code/detail/del",            sys_code_detail_del),
        (r"/sys/test",                       sys_test),
        (r"/sys/get/code/type",              sys_code_type),

        # 功能：数据库归档API
        (r"/archive/add",                    archiveadd),
        (r"/archive/add/save",               archiveadd_save),
        (r"/archive/query",                  archivequery),
        (r"/archive/_query",                 archive_query),
        (r"/archive/_query/detail",          archive_query_detail),
        (r"/archive/change",                 archivechange),
        (r"/archive/edit",                   archiveedit),
        (r"/archive/edit/save",              archiveedit_save),
        (r"/archive/edit/del",               archiveedit_del),
        (r"/archive/edit/push",              archiveedit_push),
        (r"/archive/edit/run",               archiveedit_run),
        (r"/archive/edit/stop",              archiveedit_stop),
        (r"/archive/clone",                  archiveclone),
        (r"/archive/clone/save",             archiveclone_save),
        (r"/archive/log/query",              archivelogquery),
        (r"/archive/log/_query",             archive_log_query),

        # 功能：数据库工具API
        (r"/dict/gen",                       dict_gen),
        (r"/redis/migrate",                  redis_migrate),

        # 功能：数据库监控-指标管理API
        (r"/monitor/index/query",            monitorindexquery),
        (r"/monitor/index/_query",           monitorindex_query),
        (r"/monitor/index/add/save",         monitorindexadd_save),
        (r"/monitor/index/edit/save",        monitorindexedit_save),
        (r"/monitor/index/edit/del",         monitorindexedit_del),

        # 功能：数据库监控-模板管理API
        (r"/monitor/templete/query",         monitortempletequery),
        (r"/monitor/templete/_query",        monitortemplete_query),
        (r"/monitor/templete/add/save",      monitortempleteadd_save),
        (r"/monitor/templete/edit/save",     monitortempleteedit_save),
        (r"/monitor/templete/edit/del",      monitortempleteedit_del),
        (r"/monitor/sys/indexes",            monitor_sys_indexes),
        (r"/monitor/templete/indexes",       monitor_templete_indexes),

        # 功能：数据库监控-任务管理API
        (r"/monitor/task/query",             monitortaskquery),
        (r"/monitor/task/_query",            monitortask_query),
        (r"/monitor/task/add/save/gather",   monitortaskadd_save_gather),
        (r"/monitor/task/add/save/monitor",  monitortaskadd_save_monitor),
        (r"/monitor/task/edit/save/gather",  monitortaskupd_save_gather),
        (r"/monitor/task/edit/save/monitor", monitortaskupd_save_monitor),
        (r"/monitor/task/edit/del",          monitortaskedit_del),
        (r"/monitor/task/push",              monitortask_push),
        (r"/monitor/task/run" ,              monitortask_run),
        (r"/monitor/task/stop",              monitortask_stop),
        (r"/get/monitor/templete/type",      get_monitor_templete_type),
        (r"/get/monitor/task",               get_monitor_task),

        # 功能：数据库监控-图表展示API
        (r"/monitor/graph/query",            monitorgraphquery),
        (r"/monitor/graph/_query",           monitorgraph_query),
        (r"/get/monitor/db",                 get_monitor_db),
        (r"/get/monitor/index",              get_monitor_index),
        (r"/monitor/view",                   get_monitor_view),
        (r"/monitor/view/sys",               get_monitor_view_sys),
        (r"/monitor/view/svr",               get_monitor_view_svr),

        # 功能：数据库管理-新增实例API
        (r"/db/inst/crt/query",              dbinstcrtquery),
        (r"/db/inst/crt/_query",             db_inst_crt_query),
        (r"/db/inst/save",                   db_inst_save),
        (r"/db/inst/update",                 db_inst_update),
        (r"/db/inst/del",                    db_inst_delete),
        (r"/db/inst/create",                 db_inst_create),
        (r"/db/inst/destroy",                db_inst_destroy),
        (r"/db/inst/log",                    db_inst_log),
        (r"/db/inst/manager",                db_inst_manager),


        # 功能：数据库管理-实例管理API
        (r"/db/inst/query",                  dbinstquery),
        (r"/db/inst/_query",                 db_inst_query),
        (r"/db/inst/query/id",               db_inst_query_by_id),
        (r"/db/inst/mgr",                    dbinstmgr),
        (r"/db/inst/sql/_query",             db_inst_sql_query),
        (r"/get/inst/tree",                  get_tree_by_inst),
        (r"/get/inst/tab/ddl",               get_inst_tab_ddl),
        (r"/get/inst/idx/ddl",               get_inst_idx_ddl),
        (r"/drop/inst/tab",                  drop_inst_tab),

        # 功能：数据库管理-用户管理API
        (r"/db/user/query" ,                 dbuserquery),
        (r"/db/user/query/id" ,              db_user_query_by_id),
        (r"/db/user/_query",                 db_user_query),
        (r"/db/user/save"  ,                 db_user_save),
        (r"/db/user/update",                 db_user_update),
        (r"/db/user/del",                    db_user_delete),
        (r"/db/user/sql"  ,                  db_user_sql),
        (r"/db/user/dbs"  ,                  db_user_dbs),
        (r"/db/user/info"  ,                 db_user_info),

        # 功能：数据库管理-参数管理API
        (r"/db/inst/para/query",             dbinstparaquery),
        (r"/db/inst/para/_query",            dbinstpara_query),
        (r"/db/inst/para/add/save",          dbinstparaadd_save),
        (r"/db/inst/para/edit/save",         dbinstparaedit_save),
        (r"/db/inst/para/edit/del",          dbinstparaedit_del),

        # 功能：数据库管理-操作日志API
        (r"/db/inst/opt/log/query",          dbinstoptlogquery),
        (r"/db/inst/opt/log/_query",         dbinstoptlog_query),

        # 功能：数据库管理-配置管理API
        (r"/db/inst/cfg/query",              dbinstcfgquery),
        (r"/db/inst/cfg/_query",             db_inst_cfg_query),
        (r"/db/inst/cfg/update",             db_inst_cfg_update),

        # 功能：慢日志API
        (r"/slow/query",                     slowquery),
        (r"/slow/_query",                    slow_query),
        (r"/slow/add",                       slowadd),
        (r"/slow/add/save",                  slowadd_save),
        (r"/slow/change",                    slowchange),
        (r"/slow/edit/save",                 slowedit_save),
        (r"/slow/edit/del",                  slowedit_del),
        (r"/slow/edit/push",                 slowedit_push),
        (r"/slow/query/id" ,                 slow_query_by_id),

        # 功能：MinIO图片上传API
        (r"/minio/query",                    minioquery),
        (r"/minio/_query",                   minio_query),
        (r"/minio/add",                      minioadd),
        (r"/minio/add/save",                 minioadd_save),
        (r"/minio/change",                   miniochange),
        (r"/minio/edit",                     minioedit),
        (r"/minio/edit/save",                minioedit_save),
        (r"/minio/edit/del",                 minioedit_del),
        (r"/minio/edit/push",                minioedit_push),
        (r"/minio/clone",                    minioclone),


]
