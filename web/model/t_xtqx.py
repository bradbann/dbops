#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/1 7:14
# @Author  : 马飞
# @File    : t_xtqx.py
# @Software: PyCharm

import traceback,sys
from web.utils.common    import current_rq
from web.utils.common    import get_connection,get_connection_ds
from web.utils.common    import get_url_root
from web.model.t_user    import get_user_by_loginame
from web.utils.common    import exception_info_mysql,format_mysql_error
from web.model.t_ds      import get_ds_by_dsid

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


def del_menu(menuid):
    result={}
    try:
        db = get_connection()
        cr = db.cursor()
        sql="delete from t_xtqx  where id='{0}'".format(menuid)
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
            """.format(menu_id,name,url,status,parent_id,current_rq(),'DBA',current_rq(),'DBA');
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
    sql="select cast(id as char) as id,name from t_xtqx where status='1' AND url !=''"
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
    sql="""select cast(id as char) as id,name 
           from t_xtqx
           where status='1' AND url !=''
             and id not in(select priv_id from t_role_privs where role_id='{0}')      
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
    sql="""select cast(id as char) as id,name
           from t_xtqx 
            where status='1'  AND url !=''
              AND id in(select priv_id from t_role_privs where role_id='{0}')
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
                                        from t_user_role a ,t_role_privs b
                                         where a.role_id=b.role_id
                                           and a.user_id='{0}'
                                         ))
                order by id""".format(d_user['userid'])

        sql2 = """select id,name,url 
                    from t_xtqx 
                       where parent_id ='{0}' and status='1'
                         and id IN(select b.priv_id 
                                   from t_user_role a ,t_role_privs b
                                   where a.role_id=b.role_id
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
        print('get_tree_by_userid=',v_html)
        #sys.exit(0)
        cr.close()
        result['code'] = '0'
        result['message'] = v_html
    except:
        result['code'] = '-1'
        result['message'] = '加载失败！'
    return result

def get_tab_ddl_by_tname(dbid,tab):
    try:
        result = {}
        v_node = ""
        v_html = ""
        p_ds   = get_ds_by_dsid(dbid)
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

        sql2 = """SELECT CONCAT(table_schema,'.',table_name) 
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
