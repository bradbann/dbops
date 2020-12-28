#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/1 7:14
# @Author  : 马飞
# @File    : t_xtqx.py
# @Software: PyCharm

import traceback
import json
from web.utils.common    import current_rq,get_connection_ds_sqlserver
from web.utils.common    import get_connection,get_connection_ds,get_connection_ds_dict
from web.model.t_user    import get_user_by_loginame,get_user_by_userid
from web.model.t_ds      import get_ds_by_dsid
from web.model.t_sql     import get_mysql_proxy_result,get_sqlserver_proxy_result

def upd_menu(p_menu):
    result={}
    try:
        db = get_connection()
        cr = db.cursor()
        menuid       = p_menu['menuid']
        name         = p_menu['name']
        status       = p_menu['status']
        url          = p_menu['url']
        parent_id    = p_menu['parent_id']
        sql="""update t_xtqx 
                  set  name      ='{0}',                      
                       status    ='{1}' ,
                       url       ='{2}' ,
                       parent_id ='{3}',
                       last_update_date ='{4}' ,
                       updator='{5}'
                where id='{6}'""".format(name,status,url,parent_id,current_rq(),'DBA',menuid)
        cr.execute(sql)
        cr.close()
        db.commit()
        result['code']='0'
        result['message']='更新成功！'
    except :
        result['code'] = '-1'
        result['message'] = '更新失败！'
    return result

def upd_func(p_func):
    result={}
    try:
        db = get_connection()
        cr = db.cursor()
        funcid       = p_func['funcid']
        func_name    = p_func['func_name']
        func_url     = p_func['func_url']
        priv_id      = p_func['priv_id']
        status       = p_func['status']
        sql="""update t_func 
                  set  func_name  ='{0}',       
                       func_url   ='{1}' ,    
                       priv_id    ='{2}' ,        
                       status     ='{3}' ,                  
                       last_update_date ='{4}' ,
                       updator='{5}'
                where id='{6}'""".format(func_name,func_url,priv_id,status,current_rq(),'DBA',funcid)
        cr.execute(sql)
        cr.close()
        db.commit()
        result['code']='0'
        result['message']='更新成功！'
    except :
        result['code'] = '-1'
        result['message'] = '更新失败！'
    return result

def get_child_count(menuid):
    db = get_connection()
    cr = db.cursor()
    sql="select count(0) from t_xtqx  where parent_id='{0}'".format(menuid)
    cr.execute(sql)
    rs=cr.fetchone()
    cr.close()
    db.commit()
    return rs[0]

def del_menu(menuid):
    result={}
    try:
        db = get_connection()
        cr = db.cursor()
        if get_child_count(menuid)>0:
            result['code'] = '-1'
            result['message'] = '父菜单下有子菜单，不能删除!'
            return result

        sql="delete from t_xtqx  where id='{0}'".format(menuid)
        cr.execute(sql)
        cr.close()
        db.commit()
        result={}
        result['code']='0'
        result['message']='删除成功！'
        return result
    except :
        result['code'] = '-1'
        result['message'] = '删除失败！'
        return result

def del_func(funcid):
    result={}
    try:
        db = get_connection()
        cr = db.cursor()
        sql="delete from t_func  where id='{0}'".format(funcid)
        cr.execute(sql)
        cr.close()
        db.commit()
        result={}
        result['code']='0'
        result['message']='删除成功！'
        return result
    except :
        result['code'] = '-1'
        result['message'] = '删除失败！'
        return result


def get_menu_by_menuid(p_menuid):
    db = get_connection()
    cr = db.cursor()
    sql="select id,name,status,url,parent_id,creation_date,creator,last_update_date,updator from t_xtqx where id={0}".format(p_menuid)
    cr.execute(sql)
    rs = cr.fetchall()
    cr.close()
    db.commit()
    d_menu={}
    d_menu['menuid']    = rs[0][0]
    d_menu['name']      = rs[0][1]
    d_menu['status']    = rs[0][2]
    d_menu['url']       = rs[0][3]
    d_menu['parent_id'] = rs[0][4]
    return d_menu

def get_func_by_funcid(p_funcid):
    db = get_connection()
    cr = db.cursor()
    sql="select id,func_name,func_url,priv_id,status from t_func where id={0}".format(p_funcid)
    print('get_func_by_funcid=',sql)
    cr.execute(sql)
    rs = cr.fetchall()
    cr.close()
    db.commit()
    d_func = {}
    d_func['funcid']     = rs[0][0]
    d_func['func_name']  = rs[0][1]
    d_func['func_url']   = rs[0][2]
    d_func['priv_id']    = rs[0][3]
    d_func['status']     = rs[0][4]
    return d_func

def get_url_by_userid(p_userid):
    db = get_connection()
    cr = db.cursor()
    # sql="""SELECT url_privs
    #         FROM t_xtqx
    #            WHERE STATUS='1'
    #          AND id IN(SELECT b.priv_id
    #                FROM t_user_role a ,t_role_privs b
    #                WHERE a.role_id=b.role_id
    #                  AND a.user_id='{0}')
    #         ORDER BY id""".format(p_userid)
    sql ="""SELECT url
             FROM t_xtqx
              WHERE STATUS='1'
                 AND id IN(SELECT b.priv_id
                   FROM t_user_role a ,t_role_privs b
                   WHERE a.role_id=b.role_id
                     AND a.user_id='{0}')
            UNION
            SELECT func_url
              FROM t_func
                   WHERE STATUS='1'
                 AND id IN(SELECT b.func_id
                       FROM t_user_role a ,t_role_func_privs b
                       WHERE a.role_id=b.role_id
                         AND a.user_id='{1}')
         """.format(p_userid,p_userid)
    print('get_url_by_userid=',sql)
    cr.execute(sql)
    rs = cr.fetchall()
    cr.close()
    db.commit()
    uris = []
    for i in range(len(rs)):
        if rs[i][0] is not None:
            for j in rs[i][0].split(','):
               uris.append(j)
    return uris

def check_url(userid,uri):
    uuri = get_url_by_userid(userid)
    print('check_url=',uuri,get_user_by_userid(userid)['loginname'])

    if get_user_by_userid(userid)['loginname'] =='admin':
       return True

    if uri not in uuri:
        return False
    else:
        return True


def init_menu():
    db = get_connection()
    cr = db.cursor()
    sql = """SELECT   id,
                      CONCAT(REPEAT('&nbsp;',(LENGTH(id)-2)*8),NAME) AS NAME,
                      url,
                      CASE STATUS WHEN '1' THEN '是'  WHEN '0' THEN '否'  END  STATUS,
                      creator,DATE_FORMAT(creation_date,'%Y-%m-%d')    creation_date,
                      updator,DATE_FORMAT(last_update_date,'%Y-%m-%d') last_update_date           
            FROM t_xtqx 
             WHERE id<>'0' 
            ORDER BY id,NAME
          """
    cr.execute(sql)
    v_list = []
    for r in cr.fetchall():
        v_list.append(list(r))
    cr.close()
    cr.close()
    db.commit()
    return v_list

def get_menuid(p_parent_id):
    db = get_connection()
    cr = db.cursor()
    sql="SELECT count(0),CAST(CONCAT('0',MAX(id)+1) AS CHAR) AS ID FROM t_xtqx WHERE parent_id='{0}'".format(p_parent_id)
    cr.execute(sql)
    rs = cr.fetchone()
    cr.close()
    db.commit()
    if rs[0]==0:
        return str(p_parent_id)+'01'
    else:
        return rs[1]


def save_menu(p_menu):
    result = {}
    try:
        db        = get_connection()
        cr        = db.cursor()
        name      = p_menu['name']
        url       = p_menu['url']
        status    = p_menu['status']
        parent_id = p_menu['parent_id']
        menu_id = get_menuid(parent_id)
        print("menu_id="+menu_id)
        sql="""insert into t_xtqx(id,name,url,status,parent_id,creation_date,creator,last_update_date,updator) 
                    values('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}')
            """.format(menu_id,name,url,status,parent_id,current_rq(),'DBA',current_rq(),'DBA')
        cr.execute(sql)
        cr.close()
        db.commit()
        result={}
        result['code']='0'
        result['message']='保存成功！'
        return result
    except:
        print(traceback.format_exc())
        result['code'] = '-1'
        result['message'] = '保存失败！'
    return result

def save_func(p_func):
    result = {}
    val = check_func(p_func)
    if val['code'] == '-1':
        return val
    try:
        db          = get_connection()
        cr          = db.cursor()

        sql="""insert into t_func(func_name,func_url,priv_id,status,creation_date,creator,last_update_date,updator) 
                    values('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}')
            """.format(p_func['func_name'],p_func['func_url'],p_func['priv_id'],p_func['status'],current_rq(),'DBA',current_rq(),'DBA')
        cr.execute(sql)
        cr.close()
        db.commit()
        result={}
        result['code']='0'
        result['message']='保存成功！'
        return result
    except:
        print(traceback.format_exc())
        result['code'] = '-1'
        result['message'] = '保存失败！'
    return result

def get_privs():
    db = get_connection()
    cr = db.cursor()
    sql="""select cast(a.id as char) as id,
                  CONCAT((SELECT NAME FROM t_xtqx b WHERE b.id=a.parent_id),'=>',NAME) AS NAME 
           from t_xtqx a where a.status='1' AND a.url !=''"""
    cr.execute(sql)
    v_list = []
    for r in cr.fetchall():
        v_list.append(list(r))
    cr.close()
    db.commit()
    return v_list

def get_func_privs():
    db = get_connection()
    cr = db.cursor()
    sql="""SELECT  id,func_name AS NAME FROM t_func a WHERE a.status='1' ORDER BY id"""
    cr.execute(sql)
    v_list = []
    for r in cr.fetchall():
        v_list.append(list(r))
    cr.close()
    db.commit()
    return v_list


def get_privs_sys(p_roleid):
    db = get_connection()
    cr = db.cursor()
    sql="""select cast(a.id as char) as id,
                  CONCAT((SELECT NAME FROM t_xtqx c WHERE c.id=a.parent_id),'=>',NAME) AS NAME  
           from t_xtqx a
           where a.status='1' AND a.url !=''
             and a.id not in(select priv_id from t_role_privs b where b.role_id='{0}')      
        """.format(p_roleid)
    cr.execute(sql)
    v_list = []
    for r in cr.fetchall():
        v_list.append(list(r))
    cr.close()
    db.commit()
    return v_list

def get_privs_role(p_roleid):
    db = get_connection()
    cr = db.cursor()
    sql="""select cast(a.id as char) as id,
                  CONCAT((SELECT NAME FROM t_xtqx c WHERE c.id=a.parent_id),'=>',NAME) AS NAME  
           from t_xtqx a
            where a.status='1'  AND url !=''
              AND a.id in(select priv_id from t_role_privs b where b.role_id='{0}')
        """.format(p_roleid)
    cr.execute(sql)
    v_list = []
    for r in cr.fetchall():
        v_list.append(list(r))
    cr.close()
    db.commit()
    return v_list

def get_privs_func(p_roleid):
    db = get_connection()
    cr = db.cursor()
    sql="""SELECT  id,func_name AS NAME 
            FROM t_func a
            WHERE a.status='1'
            and a.id not in(select func_id from t_role_func_privs b where b.role_id='{0}')
        """.format(p_roleid)
    cr.execute(sql)
    v_list = []
    for r in cr.fetchall():
        v_list.append(list(r))
    cr.close()
    db.commit()
    return v_list

def get_privs_func_role(p_roleid):
    db = get_connection()
    cr = db.cursor()
    sql="""SELECT  id,func_name AS NAME 
            FROM t_func a
            WHERE a.status='1'
            and a.id  in(select func_id from t_role_func_privs b where b.role_id='{0}')
        """.format(p_roleid)
    cr.execute(sql)
    v_list = []
    for r in cr.fetchall():
        v_list.append(list(r))
    cr.close()
    db.commit()
    return v_list


def get_parent_menus():
    db = get_connection()
    cr = db.cursor()
    sql="select cast(id as char) as id,name from t_xtqx where status='1' AND url ='' order by id"
    cr.execute(sql)
    v_list = []
    for r in cr.fetchall():
        v_list.append(list(r))
    cr.close()
    db.commit()
    return v_list

def get_tree_by_userid(p_username):
    try:
        result = {}
        v_html = ""
        d_user = get_user_by_loginame(p_username)
        db     = get_connection()
        cr     = db.cursor()
        sql1 = """select id,name,icon
                from t_xtqx 
                 where parent_id ='0' and status='1'
                  and  id in(select distinct parent_id from t_xtqx 
                             where id in(select b.priv_id 
                                        from t_user_role a ,t_role_privs b,t_role c
                                         where a.role_id=b.role_id                                          
                                           and a.role_id=c.id and c.status='1'
                                           and a.user_id='{0}' 
                                         ))
                order by id""".format(d_user['userid'])

        sql2 = """select id,name,url 
                    from t_xtqx 
                       where parent_id ='{0}' and status='1'
                         and id IN(select b.priv_id 
                                   from t_user_role a ,t_role_privs b,t_role c
                                   where a.role_id=b.role_id
                                     and a.role_id=c.id and c.status='1'
                                     and a.user_id='{1}')
                        order by id"""

        cr.execute(sql1)
        rs1 = cr.fetchall()
        v_menu_header="""
                      <li class="has_sub">
                         <a href="javascript:void(0);" class="waves-effect"><i class="{0}"></i><span>{1}</span> <span class="menu-arrow"></span></a>
                         <ul class="list-unstyled">
                      """
        v_menu_footer="""</ul>
                      </li>
                      """
        for i in range(len(rs1)):
            cr.execute(sql2.format(rs1[i][0],d_user['userid']))
            rs2 = cr.fetchall()
            v_node = v_menu_header.format(rs1[i][2],rs1[i][1])
            v_html = v_html+v_node
            for j in range(len(rs2)):
                v_node = """<li><a id="{0}" class="file" href="#">{1}</a></li>""".format(rs2[j][2],rs2[j][1])
                v_html = v_html + "\n" + v_node;
            v_html=v_html+"\n"+v_menu_footer+"\n"
        #print('get_tree_by_userid=',v_html)
        #sys.exit(0)
        cr.close()
        result['code'] = '0'
        result['message'] = v_html
    except:
        result['code'] = '-1'
        result['message'] = '加载失败！'
    return result

def get_tab_ddl_by_tname(dbid,tab,cur_db):
    try:
        result = {}
        v_node = ""
        v_html = ""
        p_ds   = get_ds_by_dsid(dbid)
        p_ds['service'] = cur_db
        print('get_tab_ddl_by_tname(p_ds)=>',p_ds)
        db     = get_connection_ds(p_ds)
        cr     = db.cursor()
        sql    = """show create table {0}""".format(tab)
        cr.execute(sql)
        rs=cr.fetchone()
        cr.close()
        result['code'] = '0'
        result['message'] = rs[1]
        print('rs=',rs,rs[1])
    except Exception as e:
        print('get_tab_ddl_by_tname.ERROR:',str(e))
        result['code'] = '-1'
        result['message'] = '获取表定义失败！'
    return result

def get_db_name(dbid):
    try:
        result = {}
        p_ds   = get_ds_by_dsid(dbid)
        db     = get_connection_ds(p_ds)
        cr     = db.cursor()
        sql    = """SELECT schema_name FROM information_schema.`SCHEMATA` 
                       WHERE schema_name NOT IN('information_schema','mysql','performance_schema')
                     ORDER BY schema_name"""
        cr.execute(sql)
        rs=cr.fetchall()
        v_list = []
        for r in rs:
            v_list.append(r[0])
        cr.close()
        result['code'] = '0'
        result['message'] = v_list
    except Exception as e:
        print('get_db_name.ERROR:',str(e))
        result['code'] = '-1'
        result['message'] = '获取数据库名失败！'
    return result

def get_tab_name(dbid,db_name):
    try:
        result = {}
        p_ds   = get_ds_by_dsid(dbid)
        db     = get_connection_ds(p_ds)
        cr     = db.cursor()
        sql    = """SELECT table_name FROM information_schema.tables
                       WHERE table_schema='{0}'
                     ORDER BY table_name""".format(db_name)
        cr.execute(sql)
        rs=cr.fetchall()
        v_list = []
        for r in rs:
            v_list.append(r[0])
        cr.close()
        result['code'] = '0'
        result['message'] = v_list
    except Exception as e:
        print('get_db_name.ERROR:',str(e))
        result['code'] = '-1'
        result['message'] = '获取数据库名失败！'
    return result


def get_tab_columns(dbid,db_name,tab_name):
    try:
        result = {}
        p_ds   = get_ds_by_dsid(dbid)
        db     = get_connection_ds(p_ds)
        cr     = db.cursor()
        sql    = """
                    SELECT column_name,column_comment 
                     FROM information_schema.columns
                    WHERE table_schema='{0}'  AND table_name='{1}'
                      ORDER BY ordinal_position
                 """.format(db_name,tab_name)
        cr.execute(sql)
        rs=cr.fetchall()
        v_list = []
        for r in rs:
            v_list.append(r)
        cr.close()
        result['code'] = '0'
        result['message'] = v_list
    except Exception as e:
        print('get_db_name.err:',str(e))
        result['code'] = '-1'
        result['message'] = '获取数据库列名失败！'
    return result


def get_tab_keys(dbid,db_name,tab_name):
    try:
        result = {}
        p_ds   = get_ds_by_dsid(dbid)
        db     = get_connection_ds(p_ds)
        cr     = db.cursor()
        sql    = """
                    SELECT GROUP_CONCAT(column_name)
                     FROM information_schema.columns
                    WHERE table_schema='{0}'  AND table_name='{1}'
                       AND column_key='PRI'
                      ORDER BY ordinal_position
                 """.format(db_name,tab_name)
        cr.execute(sql)
        rs=cr.fetchone()
        result['code'] = '0'
        result['message'] = rs[0]
    except Exception as e:
        print('get_tab_keys.err:',str(e))
        result['code'] = '-1'
        result['message'] = '获取数据库列名失败！'
    return result


def query_ds(dsid):
    try:
        result = {}
        result['code'] = '0'
        result['message'] = get_ds_by_dsid(dsid)
    except Exception as e:
        print('get_tab_keys.err:',str(e))
        result['code'] = '-1'
        result['message'] = '获取数据源信息失败！'
    return result



def get_tab_incr_col(dbid,db_name,tab_name):
    try:
        result = {}
        p_ds   = get_ds_by_dsid(dbid)
        db     = get_connection_ds(p_ds)
        cr     = db.cursor()
        sql    = """
                    SELECT column_name,column_comment 
                     FROM information_schema.columns
                    WHERE table_schema='{0}'  AND table_name='{1}'
                       AND data_type IN('timestamp','datetime','date')
                      ORDER BY ordinal_position
                 """.format(db_name,tab_name)
        cr.execute(sql)
        rs = cr.fetchall()
        v_list = []
        for r in rs:
            v_list.append(r)
        cr.close()
        result['code'] = '0'
        result['message'] = v_list
    except Exception as e:
        print('get_db_name.err:', str(e))
        result['code'] = '-1'
        result['message'] = '获取数据库列名失败！'
    return result


def get_tab_structure(dbid,db_name,tab_name):
    result = {}
    p_ds   = get_ds_by_dsid(dbid)
    db     = get_connection_ds(p_ds)
    cr     = db.cursor()
    sql    = """SELECT c.column_name,
                       c.column_comment,
                       c.data_type,
                       CASE WHEN c.extra='auto_increment' THEN '自增' ELSE '' END AS col_incr,
                       CASE WHEN c.column_key='PRI' THEN '主键' ELSE '' END AS col_pk,
                       CASE WHEN c.is_nullable='NO' THEN '非空' ELSE '' END AS col_null      
                FROM information_schema.columns c
                WHERE c.table_schema='{0}'  
                  AND c.table_name='{1}'
                ORDER BY c.ordinal_position
             """.format(db_name,tab_name)
    print(sql)
    cr.execute(sql)
    v_list = []
    for r in cr.fetchall():
        v_list.append(list(r))
    cr.close()
    db.commit()
    return v_list


def get_tab_idx_by_tname(dbid,tab):
    try:
        result = {}
        p_ds   = get_ds_by_dsid(dbid)
        db     = get_connection_ds(p_ds)
        cr     = db.cursor()
        sql    = '''SHOW INDEXES FROM {0}'''.format(tab)
        cr.execute(sql)
        rs=cr.fetchall()
        print('get_tab_idx_by_tname=',rs)
        v_idx_sql = ''
        v_idx_pks = ''
        for i in rs:
            print('r=', i)
            v_idx_name = i[2]
            v_idx_type = i[10]
            v_idx_cols = i[4]
            print('v_idx_name=',v_idx_name,'v_idx_type=',v_idx_type,'v_idx_cols=',v_idx_cols)
            if v_idx_name=='PRIMARY':
               v_idx_pks=v_idx_pks+v_idx_cols+','
            else:
               v_idx_sql = v_idx_sql+ 'create index {0} on {1}({2}) using {3}'.format(v_idx_name,tab,v_idx_cols,v_idx_type)+';\n'
            print('get_tab_idx_by_tname=',v_idx_sql)

        if v_idx_pks!='':
           v_idx_sql =  'alter table {0} add primary key({1});\n'.format(tab,v_idx_pks[0:-1])+v_idx_sql[0:-1]

        cr.close()
        result['code'] = '0'
        result['message'] = v_idx_sql
        print('rs=',rs,rs[1])
    except Exception as e:
        print('get_tab_idx_by_tname.ERROR:',str(e))
        result['code'] = '-1'
        result['message'] = '未找到索引定义!'
    return result


def get_tab_idx_by_tname(dbid,tab,cur_db):
    try:
        result = {}
        p_ds   = get_ds_by_dsid(dbid)
        p_ds['service'] = cur_db
        db     = get_connection_ds(p_ds)
        cr     = db.cursor()
        sql    = '''SHOW INDEXES FROM {0}'''.format(tab)
        cr.execute(sql)
        rs=cr.fetchall()
        print('get_tab_idx_by_tname=',rs)
        v_idx_sql = ''
        v_idx_pks = ''
        for i in rs:
            print('r=', i)
            v_idx_name = i[2]
            v_idx_type = i[10]
            v_idx_cols = i[4]
            print('v_idx_name=',v_idx_name,'v_idx_type=',v_idx_type,'v_idx_cols=',v_idx_cols)
            if v_idx_name=='PRIMARY':
               v_idx_pks=v_idx_pks+v_idx_cols+','
            else:
               v_idx_sql = v_idx_sql+ 'create index {0} on {1}({2}) using {3}'.format(v_idx_name,tab,v_idx_cols,v_idx_type)+';\n'
            print('get_tab_idx_by_tname=',v_idx_sql)

        if v_idx_pks!='':
           v_idx_sql =  'alter table {0} add primary key({1});\n'.format(tab,v_idx_pks[0:-1])+v_idx_sql[0:-1]

        cr.close()
        result['code'] = '0'
        result['message'] = v_idx_sql
        print('rs=',rs,rs[1])
    except Exception as e:
        print('get_tab_idx_by_tname.ERROR:',str(e))
        result['code'] = '-1'
        result['message'] = '未找到索引定义!'
    return result


def alt_tab_desc(dbid,tab):
    result = {}
    result['code'] = '-1'
    result['message'] = '已列入开发计划...'
    return result

def get_tree_by_dbid(dbid):
    try:
        result = {}
        v_node = ""
        v_html = ""
        p_ds   = get_ds_by_dsid(dbid)
        db     = get_connection_ds(p_ds)
        cr     = db.cursor()
        sql1 = """SELECT schema_name FROM information_schema.SCHEMATA order by 1"""

        sql2 = """SELECT table_name
                   FROM information_schema.tables WHERE table_schema='{0}' order by 1
               """
        cr.execute(sql1)
        rs1 = cr.fetchall()
        for i in range(len(rs1)):
            cr.execute(sql2.format(rs1[i][0]))
            rs2 = cr.fetchall()
            v_node = """<li><span class="folder">{0}</span><ul>""".format(rs1[i][0])
            v_html=v_html+v_node
            for j in range(len(rs2)):
                v_node = """<li><span class="file">{0}<div style="display:none">{1}</div></span></li>""".format(rs2[j][0],rs2[j][0])
                v_html = v_html + "\n" + v_node;
            v_html=v_html+"\n"+"</ul></li>"+"\n"

        cr.close()
        result['code'] = '0'
        result['message'] = v_html
        result['desc']    = p_ds['db_desc']
        result['db_url']  = p_ds['db_desc']  #p_ds['url']
        print(v_html)
    except Exception as e:
        print('get_tree_by_dbid.ERROR:',str(e))
        result['code'] = '-1'
        result['message'] = '加载失败！'
    return result

def get_tree_by_dbid_layui(dbid):
    try:
        result = {}
        p_ds   = get_ds_by_dsid(dbid)
        db     = get_connection_ds_dict(p_ds)
        cr1    = db.cursor()
        cr2    = db.cursor()
        sql1   = """SELECT schema_name FROM information_schema.SCHEMATA order by 1"""
        sql2   = """SELECT table_name  FROM information_schema.tables WHERE table_schema='{0}' order by 1"""
        cr1.execute(sql1)
        rs1   = cr1.fetchall()
        v_list = []
        for r in rs1:
            v_db = {}
            v_db['title'] = r['schema_name']
            #print('sql2=', sql2.format(r['schema_name']))
            cr2.execute(sql2.format(r['schema_name']))
            rs2 = cr2.fetchall()
            #print('rs2=', rs2)
            v_children = []
            for c in rs2:
                v_children.append({"title": c['table_name']})
            v_db['children'] = v_children
            #print('v_children=', v_children)
            #print('v_db=', v_db)
            v_list.append(v_db)
            #print('v_list=', v_list)
        cr1.close()
        cr2.close()
        db.commit()
        result['code'] = '0'
        result['message'] = json.dumps(v_list)
        # result['desc']    = p_ds['db_desc']
        # result['db_url']  = p_ds['db_desc']

    except Exception as e:
        print('get_tree_by_dbid.ERROR:',str(e))
        result['code'] = '-1'
        result['message'] = '加载失败！'
    return result

def get_tree_by_dbid_mssql(dbid):
    print('get_tree_by_dbid_mssql=',dbid)
    try:
        db     = ''
        sql1   = ''
        result = {}
        v_html = ''
        p_ds   = get_ds_by_dsid(dbid)
        print('p_ds=',p_ds)

        if p_ds['proxy_status'] == '0':
           db  = get_connection_ds_sqlserver(p_ds)
        else:
           p_ds['ip']   = p_ds['proxy_server'].split(':')[0]
           p_ds['port'] = p_ds['proxy_server'].split(':')[1]
           db = get_connection_ds_sqlserver(p_ds)

        print('db=',db)
        cr = db.cursor()
        if p_ds['service'] == '':
           sql1 = """ SELECT name FROM Master..SysDatabases  ORDER BY Name"""
        else:
           sql1 = """ SELECT name FROM Master..SysDatabases where name= DB_NAME() ORDER BY Name"""

        sql2 = """SELECT OBJECT_SCHEMA_NAME(id)+'.'+Name FROM SysObjects Where XType='U' ORDER BY Name
               """
        cr.execute(sql1)
        rs1 = cr.fetchall()
        for i in range(len(rs1)):
            cr.execute('use {}'.format(rs1[i][0]))
            cr.execute(sql2.format(rs1[i][0]))
            rs2 = cr.fetchall()
            v_node = """<li><span class="folder">{0}</span><ul>""".format(rs1[i][0])
            v_html=v_html+v_node
            for j in range(len(rs2)):
                v_node = """<li><span class="file">{0}<div style="display:none">{1}</div></span></li>""".format(rs2[j][0],rs2[j][0])
                v_html = v_html + "\n" + v_node;
            v_html=v_html+"\n"+"</ul></li>"+"\n"

        cr.close()
        result['code'] = '0'
        result['message'] = v_html
        result['desc']    = p_ds['db_desc']
        result['db_url']  = p_ds['db_desc']
        #print(v_html)
    except Exception as e:
        print('get_tree_by_instid_mssql=>error:',str(e))
        result['code'] = '-1'
        result['message'] = '加载失败！'
        result['desc'] = ''
        result['db_url'] = ''
    return result

def get_tree_by_dbid_proxy(dbid):
    try:
        result = {}
        v_html = ''
        p_ds   = get_ds_by_dsid(dbid)
        sql1   = "SELECT schema_name FROM information_schema.SCHEMATA order by 1"
        sql2   = "SELECT table_name  FROM information_schema.tables WHERE table_schema='{0}' order by 1"
        ret1   = get_mysql_proxy_result(p_ds,sql1,p_ds['service'])
        print('ret1=', ret1)
        if ret1['status'] == '1':
            result['code'] = '-1'
            result['message'] = '加载失败！'
            result['desc'] = ''
            result['db_url'] = ''
            return result
        rs1 = ret1['data']
        print('rs1=',rs1,type(rs1))
        for i in range(len(rs1)):
            print('i=',i)
            ret2 = get_mysql_proxy_result(p_ds, sql2.format(rs1[i][0]),p_ds['service'])
            print('ret2=', ret2)
            if ret1['status'] == '1':
                result['code'] = '-1'
                result['message'] = '加载失败！'
                result['desc'] = ''
                result['db_url'] = ''
                return result
            rs2 = ret2['data']

            v_node = """<li><span class="folder">{0}</span><ul>""".format(rs1[i][0])
            v_html=v_html+v_node
            for j in range(len(rs2)):
                v_node = """<li><span class="file">{0}<div style="display:none">{1}</div></span></li>
                         """.format(rs2[j][0],rs2[j][0])
                v_html = v_html + "\n" + v_node;
            v_html=v_html+"\n"+"</ul></li>"+"\n"
        result['code'] = '0'
        result['message'] = v_html
        result['desc']    = p_ds['db_desc']
        result['db_url']  = p_ds['db_desc']
        print(v_html)
    except Exception as e:
        print('get_tree_by_dbid_proxy.ERROR:',str(e))
        result['code'] = '-1'
        result['message'] = '加载失败！'
    return result

def get_tree_by_dbid_mssql_proxy(dbid):
    try:
        result = {}
        v_html = ''
        p_ds = get_ds_by_dsid(dbid)

        if p_ds['service'] == '':
            sql1 = """ SELECT name FROM Master..SysDatabases  ORDER BY Name"""
        else:
            sql1 = """ SELECT name FROM Master..SysDatabases where name= DB_NAME() ORDER BY Name"""

        sql2 = """use {};SELECT OBJECT_SCHEMA_NAME(id)+'.'+Name FROM SysObjects Where XType='U' order by name"""

        ret1 = get_sqlserver_proxy_result(p_ds, sql1, p_ds['service'])

        if ret1['status'] == '1':
            result['code'] = '-1'
            result['message'] = '加载失败！'
            result['desc'] = ''
            result['db_url'] = ''
            return  result
        rs1 = ret1['data']

        for i in range(len(rs1)):
            ret2 = get_sqlserver_proxy_result(p_ds, sql2.format(rs1[i][0]),p_ds['service'])

            if ret1['status'] == '1':
                result['code'] = '-1'
                result['message'] = '加载失败！'
                result['desc'] = ''
                result['db_url'] = ''
                return result
            rs2 = ret2['data']
            v_node = """<li><span class="folder">{0}</span><ul>""".format(rs1[i][0])
            v_html = v_html + v_node
            for j in range(len(rs2)):
                v_node = """<li><span class="file">{0}<div style="display:none">{1}</div></span></li>
                         """.format(rs2[j][0],rs2[j][0])
                v_html = v_html + "\n" + v_node;
            v_html = v_html + "\n" + "</ul></li>" + "\n"

        result['code']    = '0'
        result['message'] = v_html
        result['desc']    = p_ds['db_desc']
        result['db_url']  = p_ds['db_desc']
    except Exception as e:
        print('get_tree_by_dbid_mssql_proxy=>error:', str(e))
        result['code']    = '-1'
        result['message'] = '加载失败！'
        result['desc']    = ''
        result['db_url']  = ''
    return result

def query_menu(p_name):
    db = get_connection()
    cr = db.cursor()
    sql=''
    if p_name == "":
        sql = """SELECT   id,
                      CONCAT(REPEAT('&nbsp;',(LENGTH(id)-2)*8),NAME) AS NAME,
                      url,
                      CASE STATUS WHEN '1' THEN '是'  WHEN '0' THEN '否'  END  STATUS,
                      creator,DATE_FORMAT(creation_date,'%Y-%m-%d')    creation_date,
                      updator,DATE_FORMAT(last_update_date,'%Y-%m-%d') last_update_date 
                 from t_xtqx
                 WHERE id<>'0' 
                 order by id,name""".format(p_name)
    else:
        sql = """SELECT   id,
                      CONCAT(REPEAT('&nbsp;',(LENGTH(id)-2)*8),NAME) AS NAME,
                      url,
                      CASE STATUS WHEN '1' THEN '是'  WHEN '0' THEN '否'  END  STATUS,
                      creator,DATE_FORMAT(creation_date,'%Y-%m-%d')    creation_date,
                      updator,DATE_FORMAT(last_update_date,'%Y-%m-%d') last_update_date 
                 from t_xtqx 
                where id<>'0' and ( binary name like '%{0}%' or ID like  '%{1}%')             
                 order by id,name""".format(p_name,p_name)
    print(sql)
    cr.execute(sql)
    v_list = []
    for r in cr.fetchall():
        v_list.append(list(r))
    cr.close()
    db.commit()
    return v_list

def query_func(p_name):
    db = get_connection()
    cr = db.cursor()
    sql=''
    if p_name == "":
        sql = """SELECT   id,
                      func_name,
                      func_url,
                      CASE STATUS WHEN '1' THEN '是'  WHEN '0' THEN '否'  END  STATUS,
                      creator,DATE_FORMAT(creation_date,'%Y-%m-%d')    creation_date,
                      updator,DATE_FORMAT(last_update_date,'%Y-%m-%d') last_update_date 
                 from t_func              
                 order by id"""
    else:
        sql = """SELECT   id,
                      func_name,
                      func_url,
                      CASE STATUS WHEN '1' THEN '是'  WHEN '0' THEN '否'  END  STATUS,
                      creator,DATE_FORMAT(creation_date,'%Y-%m-%d')    creation_date,
                      updator,DATE_FORMAT(last_update_date,'%Y-%m-%d') last_update_date 
                 from t_func 
                where  ( binary func_name like '%{0}%' or func_url like  '%{1}%')             
                 order by id""".format(p_name,p_name)
    print(sql)
    cr.execute(sql)
    v_list = []
    for r in cr.fetchall():
        v_list.append(list(r))
    cr.close()
    db.commit()
    return v_list

def if_exists_menu(p_name):
    db = get_connection()
    cr = db.cursor()
    sql="select count(0) from t_xtqx where upper(name)='{0}'".format(p_name.upper())
    cr.execute(sql)
    rs = cr.fetchone()
    cr.close()
    if rs[0]==0:
        return False
    else:
        return True

def check_menu(p_menu):
    result = {}
    result['code'] = '0'
    result['message'] = '验证通过'

    if p_menu["name"]=="":
        result['code']='-1'
        result['message']='菜单名称不能为空！'
        return result

    if  if_exists_menu(p_menu["name"]):
        result['code'] = '-1'
        result['message'] = '菜单名称已存在！'
        return result
    return result


def if_exists_func(p_func):
    db = get_connection()
    cr = db.cursor()
    sql="""select count(0) from t_func 
            where func_url='{0}'""".format(p_func['func_url'])
    cr.execute(sql)
    rs = cr.fetchone()
    cr.close()
    if rs[0]==0:
        return False
    else:
        return True

def check_func(p_func):
    result = {}
    result['code'] = '0'
    result['message'] = '验证通过'

    if p_func["priv_id"]=="":
        result['code']='-1'
        result['message']='功能模块不能为空！'
        return result

    if p_func["func_name"]=="":
        result['code']='-1'
        result['message']='功能名称不能为空！'
        return result

    if p_func["func_url"] == "":
        result['code'] = '-1'
        result['message'] = '功能URL不能为空！'
        return result

    # if  if_exists_func(p_func):
    #     result['code'] = '-1'
    #     result['message'] = '功能链接已存在！'
    #     return result

    return result
