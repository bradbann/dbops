#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/12/2 11:57
# @Author : 马飞
# @File : t_sql_check.py.py
# @Software: PyCharm

import re,sys
from web.model.t_ds    import get_ds_by_dsid,get_ds_by_dsid_by_cdb
from web.utils.common  import get_connection_dict,get_connection,get_connection_ds,format_sql,format_exception
import traceback

def process_result(v):
    if isinstance(v, tuple):
        if len(v)==1:
           return str(v)
        else:
           return 'code:{0},error:{1}'.format(str(v[0]),str(v[1]))
    else:
        return v

def query_check_result(user):
    db = get_connection()
    cr = db.cursor()
    sql = 'select rule_id,obj_name,error from  t_sql_audit_rule_err where user_id={} order by id'.format(user['userid'])
    print(sql)
    cr.execute(sql)
    v_list = []
    for r in cr.fetchall():
        v_list.append(list(r))
    cr.close()
    db.commit()
    return v_list

def del_check_results(db,user):
    cr  = db.cursor()
    sql = 'delete from t_sql_audit_rule_err where user_id={}'.format(user['userid'])
    cr.execute(sql)
    db.commit()

def get_obj_name(p_sql):
    if p_sql.upper().count("CREATE") > 0 and p_sql.upper().count("TABLE") > 0 \
        or p_sql.upper().count("ALTER") > 0 and p_sql.upper().count("TABLE") > 0 \
          or p_sql.upper().count("DROP") > 0 and p_sql.upper().count("TABLE") > 0 \
            or  p_sql.upper().count("CREATE")>0 and p_sql.upper().count("VIEW")>0 \
              or p_sql.upper().count("CREATE") > 0 and p_sql.upper().count("FUNCTION") > 0 \
                or p_sql.upper().count("CREATE") > 0 and p_sql.upper().count("PROCEDURE") > 0 \
                  or p_sql.upper().count("CREATE") > 0 and p_sql.upper().count("INDEX") > 0 \
                    or p_sql.upper().count("CREATE") > 0 and p_sql.upper().count("TRIGGER") > 0  :

       if p_sql.upper().count("CREATE") > 0 and p_sql.upper().count("INDEX") > 0 and p_sql.upper().count("UNIQUE") > 0:
           obj = re.split(r'\s+', p_sql)[3].replace('`', '')
       else:
           obj=re.split(r'\s+', p_sql)[2].replace('`', '')

       if ('(') in obj:
          return obj.split('(')[0]
       else:
          return obj
    else:
       return ''

def get_obj_type(p_sql):
    if p_sql.upper().count("CREATE") > 0 and p_sql.upper().count("TABLE") > 0 \
       or p_sql.upper().count("ALTER") > 0 and p_sql.upper().count("TABLE") > 0 \
         or p_sql.upper().count("DROP") > 0 and p_sql.upper().count("TABLE") > 0 \
            or  p_sql.upper().count("CREATE")>0 and p_sql.upper().count("VIEW")>0 \
              or p_sql.upper().count("CREATE") > 0 and p_sql.upper().count("FUNCTION") > 0 \
                or p_sql.upper().count("CREATE") > 0 and p_sql.upper().count("PROCEDURE") > 0 \
                   or p_sql.upper().count("CREATE") > 0 and p_sql.upper().count("INDEX") > 0 \
                     or p_sql.upper().count("CREATE") > 0 and p_sql.upper().count("TRIGGER") > 0:

       if p_sql.upper().count("CREATE") > 0 and p_sql.upper().count("INDEX") > 0 and p_sql.upper().count("UNIQUE") > 0:
           obj = 'UNIQUE-INDEX'
       elif p_sql.upper().count("CREATE") > 0 and p_sql.upper().count("INDEX") > 0 and len(p_sql.upper().split('ON')[1].split('(')[1].replace(')','').split(','))>1:
           obj = 'COMPOSITE-INDEX'
       else:
           obj=re.split(r'\s+', p_sql)[1].replace('`', '')

       if ('(') in obj:
          return obj.split('(')[0].upper()
       else:
          return obj.upper()
    else:
       return ''

def get_obj_op(p_sql):
    if re.split(r'\s+', p_sql)[0].upper() in('CREATE','DROP') and re.split(r'\s+', p_sql)[1].upper()=='TABLE':
       return re.split(r'\s+', p_sql)[0].upper()+'_'+re.split(r'\s+', p_sql)[1].upper()
    if re.split(r'\s+', p_sql)[0].upper()== 'ALTER' and re.split(r'\s+', p_sql)[1].upper()=='TABLE' and  re.split(r'\s+', p_sql)[3].upper() in('ADD','DROP'):
       return re.split(r'\s+', p_sql)[0].upper()+'_'+re.split(r'\s+', p_sql)[1].upper()+'_'+re.split(r'\s+', p_sql)[3].upper()


def get_obj_pk_name(p_curdb,p_sql):
    cr  = p_curdb.cursor()
    cr.execute(p_sql)
    cr.execute('''SELECT column_name
                     FROM  information_schema.columns   
                    WHERE UPPER(table_schema)=DATABASE()  
                      AND UPPER(table_name)=upper('{}')
                      AND column_key='PRI'
               '''.format(get_obj_name(p_sql)))
    rs  = cr.fetchone()
    col = rs[0]
    cr.execute('drop table {}'.format(get_obj_name(p_sql)))
    return col

def get_obj_pk_name_multi(p_curdb,p_sql,config):
    try:
        cr  = p_curdb.cursor()
        op  = get_obj_op(p_sql)
        if op == 'CREATE_TABLE':
            sql='''SELECT count(0)
                             FROM  information_schema.columns   
                            WHERE UPPER(table_schema)=DATABASE()  
                              AND UPPER(table_name)=upper('{}')
                              AND column_key='PRI'
                              and column_name='id'
                 '''.format(get_obj_name(p_sql))
            cr.execute(sql)
            rs  = cr.fetchone()
            config[get_obj_name(p_sql)] = 'drop table {}'.format(get_obj_name(p_sql))
            return rs[0]
    except Exception as e:
        print(traceback.print_exc())
        return str(e)


def f_get_table_ddl(p_curdb,tab):
    cr_source = p_curdb.cursor()
    v_sql     ="""show create table {0}""".format(tab)
    cr_source.execute(v_sql)
    rs=cr_source.fetchone()
    return rs[1]

def get_obj_privs_grammar(p_curdb,p_sql):
    try:
        op = get_obj_op(p_sql)
        cr  = p_curdb.cursor()
        if op == 'CREATE_TABLE':
            cr.execute(p_sql)
            cr.execute('drop table {}'.format(get_obj_name(p_sql)))
        elif op in('ALTER_TABLE_ADD','ALTER_TABLE_DROP'):
            try:
                cr.execute(f_get_table_ddl(p_curdb,get_obj_name(p_sql)).replace(get_obj_name(p_sql),'dbops_'+get_obj_name(p_sql)))
            except Exception as e:
                cr.execute('drop table {0}'.format('dbops_' + get_obj_name(p_sql)))
                cr.execute(f_get_table_ddl(p_curdb, get_obj_name(p_sql)).replace(get_obj_name(p_sql),'dbops_' + get_obj_name(p_sql)))
            try:
                cr.execute(p_sql.replace(get_obj_name(p_sql),'dbops_'+get_obj_name(p_sql)))
                cr.execute('drop table {0}'.format('dbops_'+get_obj_name(p_sql)))
            except Exception as e:
                cr.execute('drop table {0}'.format('dbops_' + get_obj_name(p_sql)))
                return str(e)
        return '0'
    except Exception as e:
        return str(e)

def get_obj_privs_grammar_multi(p_curdb,p_sql,config):
    try:
        op = get_obj_op(p_sql)
        cr  = p_curdb.cursor()
        if op == 'CREATE_TABLE':
            cr.execute(p_sql)
            config[get_obj_name(p_sql)] = 'drop table {}'.format(get_obj_name(p_sql))
        elif op in('ALTER_TABLE_ADD','ALTER_TABLE_DROP'):
            if config.get('dbops_' + get_obj_name(p_sql)) is None:
               cr.execute(f_get_table_ddl(p_curdb,get_obj_name(p_sql)).replace(get_obj_name(p_sql),'dbops_'+get_obj_name(p_sql)))
            cr.execute(p_sql.replace(get_obj_name(p_sql), 'dbops_' + get_obj_name(p_sql)))
            cr.execute('drop table {0}'.format('dbops_' + get_obj_name(p_sql)))
            cr.execute(f_get_table_ddl(p_curdb, get_obj_name(p_sql)).replace(get_obj_name(p_sql),'dbops_' + get_obj_name(p_sql)))
            config['dbops_' +get_obj_name(p_sql)] = 'drop table {0}'.format('dbops_' + get_obj_name(p_sql))
        return '0'
    except Exception as e:
        return str(e)

def get_tab_comment(p_curdb,p_sql):
    cr  = p_curdb.cursor()
    cr.execute(p_sql)
    cr.execute('''SELECT CASE WHEN table_comment!='' THEN 1 ELSE 0 END 
                    FROM  information_schema.tables   
                    WHERE UPPER(table_schema)=DATABASE()  
                     AND UPPER(table_name) =upper('{}')
               '''.format(get_obj_name(p_sql)))
    rs  = cr.fetchone()
    col = rs[0]
    cr.execute('drop table {}'.format(get_obj_name(p_sql)))
    return col

def get_tab_comment_multi(p_curdb,p_sql,config):
    try:
        cr  = p_curdb.cursor()
        op  = get_obj_op(p_sql)
        if op == 'CREATE_TABLE':
            cr.execute('''SELECT CASE WHEN table_comment!='' THEN 1 ELSE 0 END 
                            FROM  information_schema.tables   
                            WHERE UPPER(table_schema)=DATABASE()  
                              AND UPPER(table_name) =upper('{}')
                       '''.format(get_obj_name(p_sql)))
            rs  = cr.fetchone()
            config[get_obj_name(p_sql)] = 'drop table {}'.format(get_obj_name(p_sql))
            return rs[0]
    except Exception as e:
        return str(e)

def get_col_comment(p_curdb,p_sql):
    try:
        cr = p_curdb.cursor()
        op = get_obj_op(p_sql)
        if op == 'CREATE_TABLE':
            try:
                cr.execute(p_sql)
                cr.execute('''SELECT table_name,column_name,
                                     CASE WHEN column_comment!='' THEN 1 ELSE 0 END 
                               FROM  information_schema.columns   
                               WHERE UPPER(table_schema)=DATABASE()  
                                 AND UPPER(table_name) = upper('{}')
                              '''.format(get_obj_name(p_sql)))
                rs  = cr.fetchall()
                col = rs
                cr.execute('drop table {}'.format(get_obj_name(p_sql)))
                return col
            except Exception as e:
                cr.execute('drop table {}'.format(get_obj_name(p_sql)))
                return str(e)

        elif op == 'ALTER_TABLE_ADD':
            try:
                cr.execute(f_get_table_ddl(p_curdb, get_obj_name(p_sql)).replace(get_obj_name(p_sql),'dbops_' + get_obj_name(p_sql)))
            except Exception as e:
                cr.execute('drop table {0}'.format('dbops_' + get_obj_name(p_sql)))
                cr.execute(f_get_table_ddl(p_curdb, get_obj_name(p_sql)).replace(get_obj_name(p_sql), 'dbops_' + get_obj_name(p_sql)))

            try:
                cr.execute(p_sql.replace(get_obj_name(p_sql),'dbops_' + get_obj_name(p_sql)))
                cr.execute('''SELECT table_name,column_name,
                                      CASE WHEN column_comment!='' THEN 1 ELSE 0 END 
                                   FROM  information_schema.columns   
                                   WHERE UPPER(table_schema)=DATABASE()  
                                     AND UPPER(table_name) = upper('{}')
                              '''.format('dbops_' + get_obj_name(p_sql)))
                rs = cr.fetchall()
                col = rs
                cr.execute('drop table {0}'.format('dbops_' + get_obj_name(p_sql)))
                return col
            except Exception as e:
                cr.execute('drop table {0}'.format('dbops_' + get_obj_name(p_sql)))
                return str(e)

    except Exception as e:
        return str(e)

def get_col_comment_multi(p_curdb,p_sql,config):
    try:
        cr = p_curdb.cursor()
        op = get_obj_op(p_sql)
        if op == 'CREATE_TABLE':
            try:
                cr.execute('''SELECT table_name,
                                     column_name,
                                     CASE WHEN column_comment!='' THEN 1 ELSE 0 END 
                               FROM  information_schema.columns   
                               WHERE UPPER(table_schema)=DATABASE()  
                                 AND UPPER(table_name) = upper('{}')
                              '''.format(get_obj_name(p_sql)))
                rs  = cr.fetchall()
                config[get_obj_name(p_sql)] = 'drop table {}'.format(get_obj_name(p_sql))
                return rs
            except Exception as e:
                return str(e)

        elif op == 'ALTER_TABLE_ADD':
            if config.get('dbops_' + get_obj_name(p_sql)) is None:
               cr.execute(f_get_table_ddl(p_curdb, get_obj_name(p_sql)).replace(get_obj_name(p_sql),'dbops_' + get_obj_name(p_sql)))

            try:
                cr.execute(p_sql.replace(get_obj_name(p_sql),'dbops_' + get_obj_name(p_sql)))
                cr.execute('''SELECT table_name,
                                    column_name,
                                      CASE WHEN column_comment!='' THEN 1 ELSE 0 END 
                                   FROM  information_schema.columns   
                                   WHERE UPPER(table_schema)=DATABASE()  
                                     AND UPPER(table_name) = upper('{}')
                              '''.format('dbops_' + get_obj_name(p_sql)))
                rs = cr.fetchall()
                cr.execute('drop table {0}'.format('dbops_' + get_obj_name(p_sql)))
                cr.execute(f_get_table_ddl(p_curdb, get_obj_name(p_sql)).replace(get_obj_name(p_sql),'dbops_' + get_obj_name(p_sql)))
                config['dbops_' + get_obj_name(p_sql)] = 'drop table {0}'.format('dbops_' + get_obj_name(p_sql))
                return rs
            except Exception as e:
                return process_result(str(e))

    except Exception as e:
        return process_result(str(e))


def get_col_default_value(p_curdb,p_sql):
    try:
        cr  = p_curdb.cursor()
        op  = get_obj_op(p_sql)
        if op == 'CREATE_TABLE':
            try:
                cr.execute(p_sql)
                cr.execute('''SELECT table_name,column_name,
                                       CASE WHEN column_default is NULL AND is_nullable='NO' THEN 0 ELSE 1 END 
                                FROM  information_schema.columns   
                                WHERE UPPER(table_schema)=DATABASE()  
                                  AND column_key!='PRI'
                                  AND UPPER(table_name) = upper('{}')
                           '''.format(get_obj_name(p_sql)))
                rs  = cr.fetchall()
                col = rs
                cr.execute('drop table {}'.format(get_obj_name(p_sql)))
                return col
            except Exception as e:
                cr.execute('drop table {}'.format(get_obj_name(p_sql)))
                return str(e)

        elif op == 'ALTER_TABLE_ADD':
            try:
                cr.execute(f_get_table_ddl(p_curdb, get_obj_name(p_sql)).replace(get_obj_name(p_sql),'dbops_' + get_obj_name(p_sql)))
            except Exception as e:
                cr.execute('drop table {0}'.format('dbops_' + get_obj_name(p_sql)))
                cr.execute(f_get_table_ddl(p_curdb, get_obj_name(p_sql)).replace(get_obj_name(p_sql),'dbops_' + get_obj_name(p_sql)))

            try:
                cr.execute(p_sql.replace(get_obj_name(p_sql), 'dbops_' + get_obj_name(p_sql)))
                v_sql ='''SELECT table_name,column_name,
                                     CASE WHEN column_default is NULL AND is_nullable='NO' THEN 0 ELSE 1 END 
                                FROM  information_schema.columns   
                                WHERE UPPER(table_schema)=DATABASE()  
                                  AND column_key!='PRI'
                                  AND UPPER(table_name) = upper('{}')
                           '''.format('dbops_' + get_obj_name(p_sql))
                cr.execute(v_sql)
                rs = cr.fetchall()
                col = rs
                cr.execute('drop table {0}'.format('dbops_' + get_obj_name(p_sql)))
                return col
            except Exception as e:
                cr.execute('drop table {0}'.format('dbops_' + get_obj_name(p_sql)))
                return str(e)

    except Exception as e:
        return str(e)

def get_col_default_value_multi(p_curdb,p_sql,config):
    try:
        cr  = p_curdb.cursor()
        op  = get_obj_op(p_sql)
        if op == 'CREATE_TABLE':
            cr.execute('''SELECT table_name,column_name,
                                   CASE WHEN column_default is NULL AND is_nullable='NO' THEN 0 ELSE 1 END 
                            FROM  information_schema.columns   
                            WHERE UPPER(table_schema)=DATABASE()  
                              AND column_key!='PRI'
                              AND UPPER(table_name) = upper('{}')
                       '''.format(get_obj_name(p_sql)))
            rs  = cr.fetchall()
            config[get_obj_name(p_sql)] = 'drop table {}'.format(get_obj_name(p_sql))
            return rs
        elif op == 'ALTER_TABLE_ADD':
            if config.get('dbops_' + get_obj_name(p_sql)) is None:
                cr.execute(f_get_table_ddl(p_curdb, get_obj_name(p_sql))
                           .replace(get_obj_name(p_sql),'dbops_' + get_obj_name(p_sql)))

            try:
                cr.execute(p_sql.replace(get_obj_name(p_sql), 'dbops_' + get_obj_name(p_sql)))
                v_sql ='''SELECT table_name,column_name,
                                     CASE WHEN column_default is NULL AND is_nullable='NO' THEN 0 ELSE 1 END 
                            FROM  information_schema.columns   
                            WHERE UPPER(table_schema)=DATABASE()  
                              AND column_key!='PRI'
                              AND UPPER(table_name) = upper('{}')
                           '''.format('dbops_' + get_obj_name(p_sql))
                cr.execute(v_sql)
                rs = cr.fetchall()
                cr.execute('drop table {0}'.format('dbops_' + get_obj_name(p_sql)))
                cr.execute(f_get_table_ddl(p_curdb, get_obj_name(p_sql)).replace(get_obj_name(p_sql),'dbops_' + get_obj_name(p_sql)))
                config['dbops_' + get_obj_name(p_sql)] = 'drop table {0}'.format('dbops_' + get_obj_name(p_sql))
                return rs
            except Exception as e:
                return process_result(str(e))

    except Exception as e:
        return process_result(str(e))

def get_time_col_default_value(p_curdb,p_sql):
    cr  = p_curdb.cursor()
    cr.execute(p_sql)
    sql ='''SELECT 
                    table_name,
                    column_name,
                    'CURRENT_TIMESTAMP',
                    CASE WHEN column_default='CURRENT_TIMESTAMP'  THEN  1 ELSE 0 END
              FROM  information_schema.columns   
              WHERE UPPER(table_schema)=DATABASE()  
               AND data_type IN('datetime','timestamp')
               AND column_key!='PRI'
               AND UPPER(table_name) = upper('{0}')
               AND column_name='create_time'
              union all  
              SELECT 
                    table_name,
                    column_name,
                    'CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP',
                    CASE WHEN column_default='CURRENT_TIMESTAMP' AND extra='on update CURRENT_TIMESTAMP' THEN  1 ELSE 0 END
              FROM  information_schema.columns   
              WHERE UPPER(table_schema)=DATABASE()  
               AND data_type IN('datetime','timestamp')
               AND column_key!='PRI'
               AND UPPER(table_name) = upper('{0}')
               AND column_name='update_time'
           '''.format(get_obj_name(p_sql),get_obj_name(p_sql))
    cr.execute(sql)
    rs  = cr.fetchall()
    col = rs
    cr.execute('drop table {}'.format(get_obj_name(p_sql)))
    return col

def get_time_col_default_value_multi(p_curdb,p_sql,config):
    try:
        cr = p_curdb.cursor()
        op = get_obj_op(p_sql)

        if op == 'CREATE_TABLE':
            try:
                sql = '''SELECT 
                              table_name,
                              column_name,
                              'CURRENT_TIMESTAMP',
                              CASE WHEN column_default='CURRENT_TIMESTAMP'  THEN  1 ELSE 0 END
                           FROM  information_schema.columns   
                           WHERE UPPER(table_schema)=DATABASE()  
                            AND data_type IN('datetime','timestamp')
                            AND column_key!='PRI'
                            AND UPPER(table_name) = upper('{0}')
                            AND column_name='create_time'
                           union all  
                           SELECT 
                                 table_name,
                                 column_name,
                                 'CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP',
                                 CASE WHEN column_default='CURRENT_TIMESTAMP' AND extra='on update CURRENT_TIMESTAMP' THEN  1 ELSE 0 END
                           FROM  information_schema.columns   
                           WHERE UPPER(table_schema)=DATABASE()  
                             AND data_type IN('datetime','timestamp')
                             AND column_key!='PRI'
                             AND UPPER(table_name) = upper('{0}')
                             AND column_name='update_time'
                      '''.format(get_obj_name(p_sql), get_obj_name(p_sql))
                cr.execute(sql)
                rs = cr.fetchall()
                config[get_obj_name(p_sql)] = 'drop table {}'.format(get_obj_name(p_sql))
                return rs
            except Exception as e:
                return process_result(str(e))

        elif op == 'ALTER_TABLE_ADD':
            if config.get('dbops_' + get_obj_name(p_sql)) is None:
                cr.execute(f_get_table_ddl(p_curdb, get_obj_name(p_sql))
                           .replace(get_obj_name(p_sql),'dbops_' + get_obj_name(p_sql)))
            try:
                cr.execute(p_sql.replace(get_obj_name(p_sql), 'dbops_' + get_obj_name(p_sql)))
                sql = '''SELECT 
                             table_name,
                             column_name,
                             'CURRENT_TIMESTAMP',
                             CASE WHEN column_default='CURRENT_TIMESTAMP'  THEN  1 ELSE 0 END
                           FROM  information_schema.columns   
                           WHERE UPPER(table_schema)=DATABASE()  
                            AND data_type IN('datetime','timestamp')
                            AND column_key!='PRI'
                            AND UPPER(table_name) = upper('{0}')
                            AND column_name='create_time'
                           union all  
                           SELECT 
                                 table_name,
                                 column_name,
                                 'CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP',
                                 CASE WHEN column_default='CURRENT_TIMESTAMP' AND extra='on update CURRENT_TIMESTAMP' THEN  1 ELSE 0 END
                           FROM  information_schema.columns   
                           WHERE UPPER(table_schema)=DATABASE()  
                            AND data_type IN('datetime','timestamp')
                            AND column_key!='PRI'
                            AND UPPER(table_name) = upper('{0}')
                            AND column_name='update_time'
                      '''.format('dbops_' + get_obj_name(p_sql), 'dbops_' + get_obj_name(p_sql))
                cr.execute(sql)
                cr.execute('drop table {0}'.format('dbops_' + get_obj_name(p_sql)))
                cr.execute(f_get_table_ddl(p_curdb, get_obj_name(p_sql)).replace(get_obj_name(p_sql),'dbops_' + get_obj_name(p_sql)))
                rs = cr.fetchall()
                config['dbops_' + get_obj_name(p_sql)] = 'drop table {0}'.format('dbops_' + get_obj_name(p_sql))
                return rs
            except Exception as e:
                return process_result(str(e))

    except Exception as e:
        return process_result(str(e))

def get_tab_char_col_len(p_curdb,p_sql,rule):
    cr  = p_curdb.cursor()
    cr.execute(p_sql)
    cr.execute('''SELECT 
                    table_name,column_name,
                    CASE WHEN character_maximum_length<={0} THEN 1 ELSE 0 END AS val
                  FROM  information_schema.columns   
                  WHERE UPPER(table_schema)=DATABASE()  
                   AND data_type IN('varchar','char')
                   AND column_key!='PRI'
                   AND UPPER(table_name) = upper('{1}')
               '''.format(rule['rule_value'],get_obj_name(p_sql)))
    rs  = cr.fetchall()
    col = rs
    cr.execute('drop table {}'.format(get_obj_name(p_sql)))
    return col

def get_tab_char_col_len_multi(p_curdb,p_sql,rule,config):
    try:
        cr  = p_curdb.cursor()
        op = get_obj_op(p_sql)
        if op == 'CREATE_TABLE':
            cr.execute('''SELECT 
                            table_name,column_name,
                            CASE WHEN character_maximum_length<={0} THEN 1 ELSE 0 END AS val
                          FROM  information_schema.columns   
                          WHERE UPPER(table_schema)=DATABASE()  
                           AND data_type IN('varchar','char')
                           AND column_key!='PRI'
                           AND UPPER(table_name) = upper('{1}')
                       '''.format(rule['rule_value'],get_obj_name(p_sql)))
            rs  = cr.fetchall()
            config[get_obj_name(p_sql)] = 'drop table {}'.format(get_obj_name(p_sql))
            return rs
        elif op == 'ALTER_TABLE_ADD':
            if config.get('dbops_' + get_obj_name(p_sql)) is None:
                cr.execute(f_get_table_ddl(p_curdb, get_obj_name(p_sql)).
                           replace(get_obj_name(p_sql),'dbops_' + get_obj_name(p_sql)))
            try:
                cr.execute('''SELECT 
                                  table_name,column_name,
                                  CASE WHEN character_maximum_length<={0} THEN 1 ELSE 0 END AS val
                              FROM  information_schema.columns   
                              WHERE UPPER(table_schema)=DATABASE()  
                               AND data_type IN('varchar','char')
                               AND column_key!='PRI'
                               AND UPPER(table_name) = upper('{1}')
                           '''.format(rule['rule_value'], 'dbops_' + get_obj_name(p_sql)))
                rs = cr.fetchall()
                cr.execute('drop table {0}'.format('dbops_' + get_obj_name(p_sql)))
                cr.execute(f_get_table_ddl(p_curdb, get_obj_name(p_sql)).replace(get_obj_name(p_sql),'dbops_' + get_obj_name(p_sql)))
                config['dbops_' + get_obj_name(p_sql)] = 'drop table {0}'.format('dbops_' + get_obj_name(p_sql))
                return rs
            except Exception as e:
                return process_result(str(e))
    except Exception as e:
        return process_result(str(e))

def get_tab_has_fields(p_curdb,p_sql,rule):
    cr  = p_curdb.cursor()
    cr.execute(p_sql)
    cr.execute('''SELECT table_name,'create_time' AS column_name 
                     FROM  information_schema.tables a  
                    WHERE a.table_schema=DATABASE()  
                      AND a.table_name= LOWER('{0}')
                      AND NOT EXISTS(SELECT 1 FROM information_schema.columns b
                                     WHERE a.table_schema=b.table_schema
                                       AND b.table_schema=DATABASE()
                                       AND a.table_name=b.table_name
                                       AND b.column_name='create_time')
                    UNION ALL
                    SELECT table_name,'update_time' AS column_name 
                     FROM  information_schema.tables a  
                    WHERE a.table_schema=DATABASE()  
                      AND a.table_name = LOWER('{1}')
                      AND NOT EXISTS(SELECT 1 FROM information_schema.columns b
                                     WHERE a.table_schema=b.table_schema
                                       AND b.table_schema=DATABASE()
                                       AND a.table_name=b.table_name
                                       AND b.column_name='update_time')
               '''.format(get_obj_name(p_sql),get_obj_name(p_sql)))
    rs  = cr.fetchall()
    col = rs
    cr.execute('drop table {}'.format(get_obj_name(p_sql)))
    return col

def get_tab_has_fields_multi(p_curdb,p_sql,config):
    try:
        cr = p_curdb.cursor()
        op = get_obj_op(p_sql)
        if op == 'CREATE_TABLE':
            cr.execute('''SELECT table_name,'create_time' AS column_name 
                             FROM  information_schema.tables a  
                            WHERE a.table_schema=DATABASE()  
                              AND a.table_name= LOWER('{0}')
                              AND NOT EXISTS(SELECT 1 FROM information_schema.columns b
                                             WHERE a.table_schema=b.table_schema
                                               AND b.table_schema=DATABASE()
                                               AND a.table_name=b.table_name
                                               AND b.column_name='create_time')
                            UNION ALL
                            SELECT table_name,'update_time' AS column_name 
                             FROM  information_schema.tables a  
                            WHERE a.table_schema=DATABASE()  
                              AND a.table_name = LOWER('{1}')
                              AND NOT EXISTS(SELECT 1 FROM information_schema.columns b
                                             WHERE a.table_schema=b.table_schema
                                               AND b.table_schema=DATABASE()
                                               AND a.table_name=b.table_name
                                               AND b.column_name='update_time')
                       '''.format(get_obj_name(p_sql),get_obj_name(p_sql)))
            rs  = cr.fetchall()
            config[get_obj_name(p_sql)] = 'drop table {}'.format(get_obj_name(p_sql))
            return rs

        elif op == 'ALTER_TABLE_ADD':
            if config.get('dbops_' + get_obj_name(p_sql)) is None:
                cr.execute(f_get_table_ddl(p_curdb, get_obj_name(p_sql))
                           .replace(get_obj_name(p_sql),'dbops_' + get_obj_name(p_sql)))

            try:
                cr.execute(p_sql.replace(get_obj_name(p_sql), 'dbops_' + get_obj_name(p_sql)))
                cr.execute('''SELECT table_name,'create_time' AS column_name 
                                 FROM  information_schema.tables a  
                                WHERE a.table_schema=DATABASE()  
                                  AND a.table_name= LOWER('{0}')
                                  AND NOT EXISTS(SELECT 1 FROM information_schema.columns b
                                                 WHERE a.table_schema=b.table_schema
                                                   AND b.table_schema=DATABASE()
                                                   AND a.table_name=b.table_name
                                                   AND b.column_name='create_time')
                                UNION ALL
                                SELECT table_name,'update_time' AS column_name 
                                 FROM  information_schema.tables a  
                                WHERE a.table_schema=DATABASE()  
                                  AND a.table_name = LOWER('{1}')
                                  AND NOT EXISTS(SELECT 1 FROM information_schema.columns b
                                                 WHERE a.table_schema=b.table_schema
                                                   AND b.table_schema=DATABASE()
                                                   AND a.table_name=b.table_name
                                                   AND b.column_name='update_time')
                           '''.format('dbops_' + get_obj_name(p_sql),'dbops_' + get_obj_name(p_sql)))
                rs = cr.fetchall()
                cr.execute('drop table {0}'.format('dbops_' + get_obj_name(p_sql)))
                cr.execute(f_get_table_ddl(p_curdb, get_obj_name(p_sql))
                           .replace(get_obj_name(p_sql),'dbops_' + get_obj_name(p_sql)))
                config['dbops_' + get_obj_name(p_sql)] = 'drop table {0}'.format('dbops_' + get_obj_name(p_sql))
                return rs
            except Exception as e:
                return process_result(str(e))
    except Exception as e:
        return process_result(str(e))


def get_tab_tcol_datetime(p_curdb,p_sql,rule):
    cr  = p_curdb.cursor()
    cr.execute(p_sql)
    cr.execute('''SELECT table_name,
                           'create_time' AS column_name
                     FROM  information_schema.tables a  
                    WHERE a.table_schema=DATABASE()  
                      AND a.table_name= LOWER('{0}')
                      AND EXISTS(SELECT 1 FROM information_schema.columns b
                                     WHERE a.table_schema=b.table_schema
                                       AND b.table_schema=DATABASE()
                                       AND a.table_name=b.table_name
                                       AND b.column_name='create_time'
                                       AND b.data_type!='datetime')   
                    UNION ALL
                    SELECT table_name,
                           'update_time' AS column_name
                     FROM  information_schema.tables a  
                    WHERE a.table_schema=DATABASE()  
                      AND a.table_name= LOWER('{1}')
                      AND EXISTS(SELECT 1 FROM information_schema.columns b
                                     WHERE a.table_schema=b.table_schema
                                       AND b.table_schema=DATABASE()
                                       AND a.table_name=b.table_name
                                       AND b.column_name='update_time'
                                       AND b.data_type!='datetime') 
               '''.format(get_obj_name(p_sql),get_obj_name(p_sql)))
    rs  = cr.fetchall()
    col = rs
    cr.execute('drop table {}'.format(get_obj_name(p_sql)))
    return col

def get_tab_tcol_datetime_multi(p_curdb,p_sql,config):
    try:
        cr  = p_curdb.cursor()
        op = get_obj_op(p_sql)
        if op == 'CREATE_TABLE':
            cr.execute('''SELECT   table_name,
                                   'create_time' AS column_name
                             FROM  information_schema.tables a  
                            WHERE a.table_schema=DATABASE()  
                              AND a.table_name= LOWER('{0}')
                              AND EXISTS(SELECT 1 FROM information_schema.columns b
                                             WHERE a.table_schema=b.table_schema
                                               AND b.table_schema=DATABASE()
                                               AND a.table_name=b.table_name
                                               AND b.column_name='create_time'
                                               AND b.data_type!='datetime')   
                            UNION ALL
                            SELECT table_name,
                                   'update_time' AS column_name
                             FROM  information_schema.tables a  
                            WHERE a.table_schema=DATABASE()  
                              AND a.table_name= LOWER('{1}')
                              AND EXISTS(SELECT 1 FROM information_schema.columns b
                                             WHERE a.table_schema=b.table_schema
                                               AND b.table_schema=DATABASE()
                                               AND a.table_name=b.table_name
                                               AND b.column_name='update_time'
                                               AND b.data_type!='datetime') 
                       '''.format(get_obj_name(p_sql),get_obj_name(p_sql)))
            rs  = cr.fetchall()
            config[get_obj_name(p_sql)] = 'drop table {}'.format(get_obj_name(p_sql))
            return rs

        elif op == 'ALTER_TABLE_ADD':
            if config.get('dbops_' + get_obj_name(p_sql)) is None:
                cr.execute(f_get_table_ddl(p_curdb, get_obj_name(p_sql))
                           .replace(get_obj_name(p_sql),'dbops_' + get_obj_name(p_sql)))

            try:
                cr.execute(p_sql.replace(get_obj_name(p_sql), 'dbops_' + get_obj_name(p_sql)))
                cr.execute('''SELECT table_name,
                                      'create_time' AS column_name
                                FROM  information_schema.tables a  
                               WHERE a.table_schema=DATABASE()  
                                 AND a.table_name= LOWER('{0}')
                                 AND EXISTS(SELECT 1 FROM information_schema.columns b
                                                WHERE a.table_schema=b.table_schema
                                                  AND b.table_schema=DATABASE()
                                                  AND a.table_name=b.table_name
                                                  AND b.column_name='create_time'
                                                  AND b.data_type!='datetime')   
                               UNION ALL
                               SELECT table_name,
                                      'update_time' AS column_name
                                FROM  information_schema.tables a  
                               WHERE a.table_schema=DATABASE()  
                                 AND a.table_name= LOWER('{1}')
                                 AND EXISTS(SELECT 1 FROM information_schema.columns b
                                                WHERE a.table_schema=b.table_schema
                                                  AND b.table_schema=DATABASE()
                                                  AND a.table_name=b.table_name
                                                  AND b.column_name='update_time'
                                                  AND b.data_type!='datetime') 
                          '''.format('dbops_' + get_obj_name(p_sql),'dbops_' + get_obj_name(p_sql)))
                rs = cr.fetchall()
                cr.execute('drop table {0}'.format('dbops_' + get_obj_name(p_sql)))
                cr.execute(f_get_table_ddl(p_curdb, get_obj_name(p_sql)).replace(get_obj_name(p_sql),
                                                                                 'dbops_' + get_obj_name(p_sql)))
                config['dbops_' + get_obj_name(p_sql)] = 'drop table {0}'.format('dbops_' + get_obj_name(p_sql))
                return rs
            except Exception as e:
                return process_result(str(e))
    except Exception as e:
        return process_result(str(e))

def get_col_not_null(p_curdb,p_sql):
    try:
        cr  = p_curdb.cursor()
        op = get_obj_op(p_sql)
        if op == 'CREATE_TABLE':
            cr.execute(p_sql)
            cr.execute('''SELECT table_name,column_name,
                               CASE WHEN is_nullable='YES' THEN 0 ELSE 1 END 
                            FROM  information_schema.columns   
                            WHERE UPPER(table_schema)=DATABASE()  
                              AND UPPER(table_name) = upper('{}')
                       '''.format(get_obj_name(p_sql)))
            rs  = cr.fetchall()
            col = rs
            cr.execute('drop table {}'.format(get_obj_name(p_sql)))
            return col
        elif op == 'ALTER_TABLE_ADD':
            try:
                cr.execute(f_get_table_ddl(p_curdb, get_obj_name(p_sql)).replace(get_obj_name(p_sql),
                                                                                 'dbops_' + get_obj_name(p_sql)))
            except Exception as e:
                cr.execute('drop table {0}'.format('dbops_' + get_obj_name(p_sql)))
                cr.execute(f_get_table_ddl(p_curdb, get_obj_name(p_sql)).replace(get_obj_name(p_sql),
                                                                                 'dbops_' + get_obj_name(p_sql)))

            try:
                cr.execute(p_sql.replace(get_obj_name(p_sql), 'dbops_' + get_obj_name(p_sql)))
                cr.execute('''SELECT table_name,column_name,
                               CASE WHEN is_nullable='YES' THEN 0 ELSE 1 END 
                              FROM  information_schema.columns   
                               WHERE UPPER(table_schema)=DATABASE()  
                                 AND UPPER(table_name) = upper('{}')
                                          '''.format('dbops_' + get_obj_name(p_sql)))
                rs = cr.fetchall()
                col = rs
            except Exception as e:
                cr.execute('drop table {0}'.format('dbops_' + get_obj_name(p_sql)))
                return str(e)

            return col
    except Exception as e:
        return str(e)

def get_col_not_null_multi(p_curdb,p_sql,config):
    try:
        cr  = p_curdb.cursor()
        op = get_obj_op(p_sql)
        if op == 'CREATE_TABLE':
            cr.execute('''SELECT table_name,column_name,
                               CASE WHEN is_nullable='YES' THEN 0 ELSE 1 END 
                            FROM  information_schema.columns   
                              WHERE UPPER(table_schema)=DATABASE()  
                                AND UPPER(table_name) = upper('{}')
                       '''.format(get_obj_name(p_sql)))
            rs  = cr.fetchall()
            config[get_obj_name(p_sql)] = 'drop table {}'.format(get_obj_name(p_sql))
            return rs
        elif op == 'ALTER_TABLE_ADD':
            if config.get('dbops_' + get_obj_name(p_sql)) is None:
                cr.execute(f_get_table_ddl(p_curdb, get_obj_name(p_sql))
                           .replace(get_obj_name(p_sql),'dbops_' + get_obj_name(p_sql)))

            try:
                cr.execute(p_sql.replace(get_obj_name(p_sql), 'dbops_' + get_obj_name(p_sql)))
                cr.execute('''SELECT table_name,column_name,
                               CASE WHEN is_nullable='YES' THEN 0 ELSE 1 END 
                              FROM  information_schema.columns   
                               WHERE UPPER(table_schema)=DATABASE()  
                                 AND UPPER(table_name) = upper('{}')
                                          '''.format('dbops_' + get_obj_name(p_sql)))
                rs = cr.fetchall()
                cr.execute('drop table {0}'.format('dbops_' + get_obj_name(p_sql)))
                cr.execute(f_get_table_ddl(p_curdb, get_obj_name(p_sql)).replace(get_obj_name(p_sql),'dbops_' + get_obj_name(p_sql)))
                config['dbops_' + get_obj_name(p_sql)] = 'drop table {0}'.format('dbops_' + get_obj_name(p_sql))
                return rs
            except Exception as e:
                cr.execute('drop table {0}'.format('dbops_' + get_obj_name(p_sql)))
                return process_result(str(e))
    except Exception as e:
        return process_result(str(e))

def get_obj_pk_exists_auto_incr(p_curdb,p_sql):
    cr  = p_curdb.cursor()
    cr.execute(p_sql)
    cr.execute('''SELECT count(0)
                     FROM  information_schema.columns   
                    WHERE UPPER(table_schema)=DATABASE()  
                      AND UPPER(table_name)='{}'
                      AND column_key='PRI'
                      AND extra='auto_increment'
               '''.format(get_obj_name(p_sql)))
    rs  = cr.fetchone()
    col = rs[0]
    cr.execute('drop table {}'.format(get_obj_name(p_sql)))
    return rs[0]

def get_obj_pk_exists_auto_incr_multi(p_curdb,p_sql,config):
    try:
        cr  = p_curdb.cursor()
        op  = get_obj_op(p_sql)
        if op == 'CREATE_TABLE':
            cr.execute('''SELECT count(0)
                             FROM  information_schema.columns   
                            WHERE UPPER(table_schema)=DATABASE()  
                              AND UPPER(table_name)='{}'
                              AND column_key='PRI'
                              AND extra='auto_increment'
                       '''.format(get_obj_name(p_sql)))
            rs  = cr.fetchone()
            config[get_obj_name(p_sql)] = 'drop table {}'.format(get_obj_name(p_sql))
            return rs[0]
    except Exception as e:
        print(traceback.print_exc())
        return str(e)

def get_obj_pk_type_not_int_bigint(p_curdb,p_sql):
    val = 0
    cr  = p_curdb.cursor()
    cr.execute(p_sql)
    cr.execute('''SELECT data_type
                     FROM  information_schema.columns   
                    WHERE UPPER(table_schema)=DATABASE()  
                      AND UPPER(table_name)='{}'
                      AND column_key='PRI'
               '''.format(get_obj_name(p_sql)))
    rs  = cr.fetchall()
    for i in rs:
        if i[0] not in('int','bigint'):
           val=1
           break
    cr.execute('drop table {}'.format(get_obj_name(p_sql)))
    return val

def get_obj_pk_type_not_int_bigint_multi(p_curdb,p_sql,config):
    try:
        val = 0
        cr  = p_curdb.cursor()
        op  = get_obj_op(p_sql)
        if op == 'CREATE_TABLE':
            cr.execute('''SELECT data_type
                             FROM  information_schema.columns   
                            WHERE UPPER(table_schema)=DATABASE()  
                              AND UPPER(table_name)='{}'
                              AND column_key='PRI'
                       '''.format(get_obj_name(p_sql)))
            rs  = cr.fetchall()
            for i in rs:
                if i[0] not in('int','bigint'):
                   val=1
                   break
            config[get_obj_name(p_sql)] = 'drop table {}'.format(get_obj_name(p_sql))
            return val
    except Exception as e:
        print(traceback.print_exc())
        return str(e)

def get_obj_exists_auto_incr_not_1(p_curdb,p_sql):
    cr  = p_curdb.cursor()
    cr.execute(p_sql)
    cr.execute('''SELECT  AUTO_INCREMENT
                     FROM  information_schema.tables   
                    WHERE UPPER(table_schema)=upper(DATABASE())
                      AND UPPER(table_name)=upper('{}')
               '''.format(get_obj_name(p_sql)))
    rs  = cr.fetchone()
    col = rs[0]
    cr.execute('drop table {}'.format(get_obj_name(p_sql)))
    return rs[0]

def get_obj_exists_auto_incr_not_1_multi(p_curdb,p_sql,config):
    try:
        cr  = p_curdb.cursor()
        op  = get_obj_op(p_sql)
        if op == 'CREATE_TABLE':
            cr.execute('''SELECT  count(0)
                             FROM  information_schema.tables   
                            WHERE UPPER(table_schema)=upper(DATABASE())
                              AND UPPER(table_name)=upper('{}')
                              and AUTO_INCREMENT=1
                       '''.format(get_obj_name(p_sql)))
            rs  = cr.fetchone()
            config[get_obj_name(p_sql)] = 'drop table {}'.format(get_obj_name(p_sql))
            return rs[0]
    except Exception as e:
        print(traceback.print_exc())
        return str(e)

def process_single_ddl(p_dbid,p_cdb,p_sql,p_user):
    result = True
    ds_cur = get_ds_by_dsid_by_cdb(p_dbid, p_cdb)
    db_cur = get_connection_ds(ds_cur)
    db_ops = get_connection_dict()
    cr_ops = db_ops.cursor()
    ops_sql = """select id,rule_code,rule_name,rule_value,error from t_sql_audit_rule where status='1' order by id"""
    cr_ops.execute(ops_sql)
    rs_ops = cr_ops.fetchall()

    print('输出检测项...')
    print('-'.ljust(150, '-'))
    for r in rs_ops:
        print(r)

    #清空检查表
    del_check_results(db_ops, p_user)

    #检查语句
    for rule in rs_ops:

        rule['error'] = format_sql(rule['error'])

        if rule['rule_code'] == 'switch_check_ddl' and rule['rule_value'] == 'true':
            if get_obj_type(p_sql) == 'TABLE':
                print('检测DDL语法及权限...')
                v = get_obj_privs_grammar(db_cur, p_sql.strip())
                if v != '0':
                    rule['error'] = format_sql(format_exception(v))
                    save_check_results(db_ops, rule, p_user, p_sql.strip())
                    result = False

        if rule['rule_code'] == 'switch_tab_not_exists_pk' and rule['rule_value'] == 'true':
            if get_obj_op(p_sql) == 'CREATE_TABLE':
                print('检查表必须为主键...')
                if get_obj_type(p_sql.strip()) == 'TABLE' and not (
                        p_sql.upper().count('PRIMARY') > 0 and p_sql.upper().count('KEY') > 0):

                    rule['error'] = rule['error'].format(get_obj_name(p_sql.strip()))
                    save_check_results(db_ops, rule, p_user, p_sql.strip())
                    result = False

        if rule['rule_code'] == 'switch_tab_pk_id' and rule['rule_value'] == 'true':
            if get_obj_op(p_sql) == 'CREATE_TABLE':
                print('强制主键名为ID...')
                if get_obj_type(p_sql) == 'TABLE' and (p_sql.upper().count('PRIMARY') > 0 \
                                                       and p_sql.upper().count('KEY') > 0) and get_obj_pk_name(db_cur,
                                                                                                               p_sql) != 'id':
                    rule['error'] = rule['error'].format(get_obj_name(p_sql.strip()))
                    save_check_results(db_ops, rule, p_user, p_sql)
                    result = False

        if rule['rule_code'] == 'switch_tab_pk_auto_incr' and rule['rule_value'] == 'true':
            if get_obj_op(p_sql) == 'CREATE_TABLE':
                print('强制主键为自增列...')
                if get_obj_type(p_sql) == 'TABLE' and (p_sql.upper().count('PRIMARY') > 0 \
                                                       and p_sql.upper().count(
                            'KEY') > 0) and get_obj_pk_exists_auto_incr(db_cur, p_sql) == 0:
                    rule['error'] = rule['error'].format(get_obj_name(p_sql.strip()))
                    save_check_results(db_ops, rule, p_user, p_sql)
                    result = False

        if rule['rule_code'] == 'switch_tab_pk_autoincrement_1' and rule['rule_value'] == 'true':
            if get_obj_op(p_sql) == 'CREATE_TABLE':
                print('强制自增列初始值为1...')
                if get_obj_type(p_sql) == 'TABLE' \
                        and (p_sql.upper().count('PRIMARY') > 0  and p_sql.upper().count('KEY') > 0) \
                           and get_obj_exists_auto_incr_not_1(db_cur, p_sql) != 1:
                    rule['error'] = rule['error'].format(get_obj_name(p_sql.strip()))
                    save_check_results(db_ops, rule, p_user, p_sql)
                    result = False

        if rule['rule_code'] == 'switch_pk_not_int_bigint' and rule['rule_value'] == 'false':
            if get_obj_op(p_sql) == 'CREATE_TABLE':
                print('不允许主键类型非int/bigint...')
                if get_obj_type(p_sql) == 'TABLE' and (p_sql.upper().count('PRIMARY') > 0 \
                                                       and p_sql.upper().count(
                            'KEY') > 0) and get_obj_pk_type_not_int_bigint(db_cur, p_sql) > 0:
                    rule['error'] = rule['error'].format(get_obj_name(p_sql.strip()))
                    save_check_results(db_ops, rule, p_user, p_sql)
                    result = False

        if rule['rule_code'] == 'switch_tab_comment' and rule['rule_value'] == 'true':
            if get_obj_op(p_sql) == 'CREATE_TABLE':
                print('检查表注释...')
                if get_obj_type(p_sql) == 'TABLE' and get_tab_comment(db_cur, p_sql) == 0:
                    rule['error'] = rule['error'].format(get_obj_name(p_sql.strip()))
                    save_check_results(db_ops, rule, p_user, p_sql)
                    result = False

        if rule['rule_code'] == 'switch_col_comment' and rule['rule_value'] == 'true' and get_obj_type(
                p_sql) == 'TABLE':
            if get_obj_op(p_sql) in ('CREATE_TABLE', 'ALTER_TABLE_ADD'):
                print('检查列注释...')
                v = get_col_comment(db_cur, p_sql)
                e = rule['error']
                for i in v:
                    if i[2] == 0:
                        result = False
                        rule['error'] = e.format(i[0].replace('dbops_' + get_obj_name(p_sql), get_obj_name(p_sql)),
                                                 i[1])
                        save_check_results(db_ops, rule, p_user, p_sql)

        if rule['rule_code'] == 'switch_col_not_null' and rule['rule_value'] == 'true' and get_obj_type(
                p_sql) == 'TABLE':
            if get_obj_op(p_sql) in ('CREATE_TABLE', 'ALTER_TABLE_ADD'):
                print('检查列是否为空...')
                v = get_col_not_null(db_cur, p_sql)
                e = rule['error']
                for i in v:
                    if i[2] == 0:
                        result = False
                        rule['error'] = e.format(i[0].replace('dbops_' + get_obj_name(p_sql), get_obj_name(p_sql)),
                                                 i[1])
                        save_check_results(db_ops, rule, p_user, p_sql)

        if rule['rule_code'] == 'switch_col_default_value' and rule['rule_value'] == 'true' and get_obj_type(
                p_sql) == 'TABLE':
            if get_obj_op(p_sql) in ('CREATE_TABLE', 'ALTER_TABLE_ADD'):
                print('检查列默认值...')
                v = get_col_default_value(db_cur, p_sql)
                e = rule['error']
                if v is not None:
                    for i in v:
                        if i[2] == 0:
                            result = False
                            rule['error'] = e.format(i[0].
                                              replace('dbops_' + get_obj_name(p_sql), get_obj_name(p_sql)),i[1])
                            save_check_results(db_ops, rule, p_user, p_sql)

        if rule['rule_code'] == 'switch_time_col_default_value' and rule['rule_value'] == 'true' and get_obj_type(
                p_sql) == 'TABLE':
            if get_obj_op(p_sql) in ('CREATE_TABLE'):
                print('检查时间字段默认值...')
                v = get_time_col_default_value(db_cur, p_sql)
                e = rule['error']
                for i in v:
                    if i[3] == 0:
                        result = False
                        rule['error'] = e.format(i[0], i[1], i[2])
                        save_check_results(db_ops, rule, p_user, p_sql)

        if rule['rule_code'] == 'switch_char_max_len' and get_obj_type(p_sql) == 'TABLE':
            if get_obj_op(p_sql) == 'CREATE_TABLE':
                print('字符字段最大长度...')
                v = get_tab_char_col_len(db_cur, p_sql, rule)
                e = rule['error']
                for i in v:
                    if i[2] == 0:
                        result = False
                        rule['error'] = e.format(i[0], i[1], rule['rule_value'])
                        save_check_results(db_ops, rule, p_user, p_sql)

        if rule['rule_code'] == 'switch_tab_has_time_fields' and get_obj_type(p_sql) == 'TABLE':
            if get_obj_op(p_sql) == 'CREATE_TABLE':
                print('表必须拥有字段...')
                v = get_tab_has_fields(db_cur, p_sql, rule)
                e = rule['error']
                for i in v:
                    result = False
                    rule['error'] = e.format(i[0], i[1])
                    save_check_results(db_ops, rule, p_user, p_sql)

        if rule['rule_code'] == 'switch_tab_tcol_datetime' \
                and rule['rule_value'] == 'true' and get_obj_type(p_sql) == 'TABLE':
            if get_obj_op(p_sql) == 'CREATE_TABLE':
                print('时间字段类型为datetime...')
                v = get_tab_tcol_datetime(db_cur, p_sql, rule)
                print('get_tab_tcol_datetime=', v)
                e = rule['error']
                for i in v:
                    result = False
                    rule['error'] = e.format(i[0], i[1])
                    save_check_results(db_ops, rule, p_user, p_sql)

    if result:
        rule['id'] = '0'
        rule['error'] = '检测通过!'
        save_check_results(db_ops, rule, p_user, p_sql)

    return result

def process_multi_ddl(p_dbid,p_cdb,p_sql,p_user):
    results = True
    config  = {}
    ds_cur  = get_ds_by_dsid_by_cdb(p_dbid, p_cdb)
    db_cur  = get_connection_ds(ds_cur)
    db_ops  = get_connection_dict()

    #清空检查表
    del_check_results(db_ops, p_user)

    #逐条检查语句
    for st in p_sql.split(';'):
        result = True

        if st.strip() == '':
           continue

        print('check sql :',st.strip())
        cr_ops  = db_ops.cursor()
        ops_sql = """select id,rule_code,rule_name,rule_value,error from t_sql_audit_rule where status='1' order by id"""
        cr_ops.execute(ops_sql)
        rs_ops  = cr_ops.fetchall()

        print('输出检测项...')
        print('-'.ljust(150, '-'))
        for r in rs_ops:
            print(r)

        for rule in rs_ops:

            rule['error'] = format_sql(rule['error'])

            if rule['rule_code'] == 'switch_check_ddl' and rule['rule_value'] == 'true':
                if get_obj_type(st.strip()) == 'TABLE':
                    print('检测DDL语法及权限...')
                    v = get_obj_privs_grammar_multi(db_cur, st.strip(),config)
                    if v != '0':
                        rule['error'] = format_sql(format_exception(v))
                        save_check_results(db_ops, rule, p_user, st.strip())
                        result = False

            if rule['rule_code'] == 'switch_tab_not_exists_pk' and rule['rule_value'] == 'true':
                if get_obj_op(st.strip()) == 'CREATE_TABLE':
                    print('检查表必须有主键...')
                    if get_obj_type(st.strip()) == 'TABLE' and not (
                            st.strip().upper().count('PRIMARY') > 0 and st.strip().upper().count('KEY') > 0):
                        rule['error'] =rule['error'].format(get_obj_name(st.strip()))
                        save_check_results(db_ops, rule, p_user, st.strip())
                        result = False

            if rule['rule_code'] == 'switch_tab_pk_id' and rule['rule_value'] == 'true':
                if get_obj_op(st.strip()) == 'CREATE_TABLE':
                    print('强制主键名为ID...')
                    if get_obj_type(st.strip()) == 'TABLE' \
                            and (st.strip().upper().count('PRIMARY') > 0 and st.strip().upper().count('KEY') > 0) :
                       v  = get_obj_pk_name_multi(db_cur,st.strip(),config)
                       if v == 0:
                            rule['error'] = rule['error'].format(get_obj_name(st.strip()))
                            save_check_results(db_ops, rule, p_user, st.strip())
                            result = False

                       if v not in  (0,1):
                           rule['error'] = v
                           save_check_results(db_ops, rule, p_user, st.strip())
                           result = False

            if rule['rule_code'] == 'switch_tab_pk_auto_incr' and rule['rule_value'] == 'true':
                if get_obj_op(st.strip()) == 'CREATE_TABLE':
                    print('强制主键为自增列...')
                    if get_obj_type(st.strip()) == 'TABLE' \
                            and (st.strip().upper().count('PRIMARY') > 0 and st.strip().upper().count('KEY') > 0) :
                        v =  get_obj_pk_exists_auto_incr_multi(db_cur, st.strip(),config)
                        if v == 0 :
                            rule['error'] = rule['error'].format(get_obj_name(st.strip()))
                            save_check_results(db_ops, rule, p_user, st.strip())
                            result = False

                        if v not in (0, 1):
                            rule['error'] = v
                            save_check_results(db_ops, rule, p_user, st.strip())
                            result = False


            if rule['rule_code'] == 'switch_tab_pk_autoincrement_1' and rule['rule_value'] == 'true':
                if get_obj_op(st.strip()) == 'CREATE_TABLE':
                    print('强制自增列初始值为1...')
                    if get_obj_type(st.strip()) == 'TABLE' \
                            and (st.strip().upper().count('PRIMARY') > 0  and st.strip().upper().count('KEY') > 0):
                        v =  get_obj_exists_auto_incr_not_1_multi(db_cur, st.strip(),config)
                        if v == 0:
                            rule['error'] = rule['error'].format(get_obj_name(st.strip()))
                            save_check_results(db_ops, rule, p_user, st.strip())
                            result = False

                        if v not in (0, 1):
                            rule['error'] = v
                            save_check_results(db_ops, rule, p_user, st.strip())
                            result = False

            if rule['rule_code'] == 'switch_pk_not_int_bigint' and rule['rule_value'] == 'false':
                if get_obj_op(st.strip()) == 'CREATE_TABLE':
                    print('不允许主键类型非int/bigint...')
                    if get_obj_type(st.strip()) == 'TABLE' \
                            and (st.strip().upper().count('PRIMARY') > 0 and st.strip().upper().count('KEY') > 0):
                        v =  get_obj_pk_type_not_int_bigint_multi(db_cur, st.strip(),config)
                        if v == 1 :
                            rule['error'] = rule['error'].format(get_obj_name(st.strip()))
                            save_check_results(db_ops, rule, p_user, st.strip())
                            result = False

                        if v not in (0, 1):
                            rule['error'] = v
                            save_check_results(db_ops, rule, p_user, st.strip())
                            result = False

            if rule['rule_code'] == 'switch_tab_comment' and rule['rule_value'] == 'true':
                if get_obj_op(st.strip()) == 'CREATE_TABLE':
                    print('检查表注释...')
                    if get_obj_type(st.strip()) == 'TABLE':
                        v = get_tab_comment_multi(db_cur, st.strip(),config)
                        if v ==0:
                            rule['error'] = rule['error'].format(get_obj_name(st.strip()))
                            save_check_results(db_ops, rule, p_user, st.strip())
                            result = False

                        if v not in (0, 1):
                            rule['error'] = v
                            save_check_results(db_ops, rule, p_user, st.strip())
                            result = False

            if rule['rule_code'] == 'switch_col_comment' \
                    and rule['rule_value'] == 'true' and get_obj_type(st.strip()) == 'TABLE':
                if get_obj_op(st.strip()) in ('CREATE_TABLE', 'ALTER_TABLE_ADD'):
                    print('检查列注释...')
                    v = get_col_comment_multi(db_cur, st.strip(),config)
                    print('switch_col_comment=>v=',v)
                    e = rule['error']
                    try:
                        for i in v:
                            if i[2] == 0:
                                result = False
                                rule['error'] = e.format(i[0].
                                                 replace('dbops_'+ get_obj_name(st.strip()),get_obj_name(st.strip())),i[1])
                                save_check_results(db_ops, rule, p_user, st.strip())
                    except IndexError as e:
                        result = False
                        rule['error'] = v
                        save_check_results(db_ops, rule, p_user, st.strip())
                    except:
                        result = False
                        rule['error'] = v
                        save_check_results(db_ops, rule, p_user, st.strip())

            if rule['rule_code'] == 'switch_col_not_null' \
                    and rule['rule_value'] == 'true' and get_obj_type(st.strip()) == 'TABLE':
                if get_obj_op(st.strip()) in ('CREATE_TABLE', 'ALTER_TABLE_ADD'):
                    print('检查列是否为空...')
                    v = get_col_not_null_multi(db_cur, st.strip(),config)
                    e = rule['error']
                    try:
                        for i in v:
                            if i[2] == 0:
                                result = False
                                rule['error'] = e.format(i[0].
                                                replace('dbops_' + get_obj_name(st.strip()), get_obj_name(st.strip())),i[1])
                                save_check_results(db_ops, rule, p_user, st.strip())
                    except IndexError as e:
                        result = False
                        rule['error'] = v
                        save_check_results(db_ops, rule, p_user, st.strip())
                    except:
                        result = False
                        rule['error'] = v
                        save_check_results(db_ops, rule, p_user, st.strip())


            if rule['rule_code'] == 'switch_col_default_value' \
                    and rule['rule_value'] == 'true' and get_obj_type(st.strip()) == 'TABLE':
                if get_obj_op(st.strip()) in ('CREATE_TABLE', 'ALTER_TABLE_ADD'):
                    print('检查列默认值...')
                    v = get_col_default_value_multi(db_cur, st.strip(),config)
                    e = rule['error']
                    try:
                        for i in v:
                            if i[2] == 0:
                                result = False
                                rule['error'] = e.format(
                                    i[0].replace('dbops_' + get_obj_name(st.strip()), get_obj_name(st.strip())),
                                    i[1])
                                save_check_results(db_ops, rule, p_user, st.strip())
                    except IndexError as e:
                        result = False
                        rule['error'] = v
                        save_check_results(db_ops, rule, p_user, st.strip())
                    except:
                        result = False
                        rule['error'] = v
                        save_check_results(db_ops, rule, p_user, st.strip())

            if rule['rule_code'] == 'switch_time_col_default_value' \
                    and rule['rule_value'] == 'true' and get_obj_type(st.strip()) == 'TABLE':
                if get_obj_op(st.strip()) in ('CREATE_TABLE'):
                    print('检查时间字段默认值...')
                    v = get_time_col_default_value_multi(db_cur, st.strip(),config)
                    e = rule['error']
                    try:
                        for i in v:
                            if i[3] == 0:
                                result = False
                                rule['error'] = e.format(i[0], i[1], i[2])
                                save_check_results(db_ops, rule, p_user, st.strip())
                    except IndexError as e:
                        result = False
                        rule['error'] = v
                        save_check_results(db_ops, rule, p_user, st.strip())
                    except:
                        result = False
                        rule['error'] = v
                        save_check_results(db_ops, rule, p_user, st.strip())

            if rule['rule_code'] == 'switch_char_max_len' and get_obj_type(st.strip()) == 'TABLE':
                if get_obj_op(st.strip()) == 'CREATE_TABLE':
                    print('字符字段最大长度...')
                    v = get_tab_char_col_len_multi(db_cur, st.strip(), rule,config)
                    e = rule['error']
                    try:
                        for i in v:
                            if i[2] == 0:
                                result = False
                                rule['error'] = e.format(i[0], i[1], rule['rule_value'])
                                save_check_results(db_ops, rule, p_user, st.strip())
                    except IndexError as e:
                        result = False
                        rule['error'] = v
                        save_check_results(db_ops, rule, p_user, st.strip())
                    except:
                        result = False
                        rule['error'] = v
                        save_check_results(db_ops, rule, p_user, st.strip())


            if rule['rule_code'] == 'switch_tab_has_time_fields' and get_obj_type(st.strip()) == 'TABLE':
                if get_obj_op(st.strip()) == 'CREATE_TABLE':
                    print('表必须拥有字段...')
                    v = get_tab_has_fields_multi(db_cur, st.strip(),config)
                    e = rule['error']
                    try:
                        for i in v:
                            result = False
                            rule['error'] = e.format(i[0], i[1])
                            save_check_results(db_ops, rule, p_user, p_sql)
                    except IndexError as e:
                        result = False
                        rule['error'] = v
                        save_check_results(db_ops, rule, p_user, st.strip())
                    except:
                        result = False
                        rule['error'] = v
                        save_check_results(db_ops, rule, p_user, st.strip())

            if rule['rule_code'] == 'switch_tab_tcol_datetime' \
                    and rule['rule_value'] == 'true' and get_obj_type(st.strip()) == 'TABLE':
                if get_obj_op(st.strip()) == 'CREATE_TABLE':
                    print('时间字段类型为datetime...')
                    v = get_tab_tcol_datetime_multi(db_cur, st.strip(),config)
                    e = rule['error']
                    try:
                        for i in v:
                            result = False
                            rule['error'] = e.format(i[0], i[1])
                            save_check_results(db_ops, rule, p_user, st.strip())
                    except IndexError as e:
                        result = False
                        rule['error'] = v
                        save_check_results(db_ops, rule, p_user, st.strip())
                    except:
                        result = False
                        rule['error'] = v
                        save_check_results(db_ops, rule, p_user, st.strip())

        cr_ops.close()

        print('result=',result,get_obj_name(st.strip()))
        if result:
           rule['id'] = '0'
           rule['error'] = '检测通过!'
           save_check_results(db_ops, rule, p_user, st.strip())

        results =results and  result

    print('删除临时表...')
    print('config=', config, type(config))
    print('-'.ljust(150, '-'))
    cr = db_cur.cursor()
    for key in config:
       try:
          print(config[key])
          cr.execute(config[key])
       except Exception as e:
         print(traceback.format_exc())
    print('-'.ljust(150, '-')+'\n')
    return results

def check_mysql_ddl(p_dbid,p_cdb,p_sql,p_user):
    if p_sql.count(';') in(0,1):
        print('process_single_ddl....')
        return process_single_ddl(p_dbid,p_cdb,p_sql.strip(),p_user)
    else:
        print('process_multi_ddl....')
        return process_multi_ddl(p_dbid, p_cdb, p_sql.strip(), p_user)


def save_check_results(db,rule,user,psql):
    cr  = db.cursor()
    print('检查结果：')
    print('-'.ljust(150, '-'))
    obj = get_obj_name(psql)
    sql = '''insert into t_sql_audit_rule_err(rule_id,user_id,obj_name,error) values ({},{},'{}','{}')
          '''.format(rule['id'],user['userid'],obj,rule['error'])
    print(sql)
    cr.execute(sql)
    db.commit()