#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/30 15:46
# @Author  : 马飞
# @File    : t_user.py
# @Software: PyCharm
from web.utils.common import format_sql,aes_encrypt,aes_decrypt
from web.utils.common import exception_info,get_connection
from web.utils.common import current_rq
import traceback
import xlrd,xlwt
import os,zipfile

def query_db_user(user_name):
    db = get_connection()
    cr = db.cursor()
    v_where =''
    if user_name != '':
       v_where = "  and ( b.db_user like '%{0}%' or b.db_user like '%{1}%')".format(user_name,user_name)

    sql = """SELECT  a.inst_name,
                     (select dmmc from t_dmmx x where x.dm='02' and x.dmm=a.inst_type) as inst_type,
                     b.db_user,
                     (select dmmc from t_dmmx x where x.dm='25' and x.dmm=b.status) as STATUS,
                     b.description,
                     date_format(b.created_date,'%Y-%m-%d %h:%i:%s')  as created_date
            FROM  t_db_inst a,t_db_user b
            where  a.id=b.inst_id
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

def save_db_user(d_db_user):
    result = {}
    val = check_db_user(d_db_user)
    if val['code']=='-1':
        return val
    try:
        db     = get_connection()
        cr     = db.cursor()
        result = {}

        db_pass = ''
        if d_db_user['db_pass'] != '':
            db_pass    = aes_encrypt(d_db_user['db_pass'], d_db_user['db_user'])
        else:
            db_pass    = d_db_user['db_pass']
        sql="""insert into t_db_user(inst_id,db_user,db_pass,statement,status,description,created_date)
                    values('{0}','{1}','{2}','{3}','{4}','{5}',now())
            """.format(d_db_user['inst_id'],d_db_user['db_user'],db_pass,
                       format_sql(d_db_user['statement']),d_db_user['status'],d_db_user['desc'])
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

def upd_inst(d_db_user):
    result={}
    val = check_db_user(d_db_user)
    if  val['code'] == '-1':
        return val
    try:
        db   = get_connection()
        cr   = db.cursor()

        db_pass = ''
        if d_db_user['db_pass'] != '':
            db_pass = aes_encrypt(d_db_user['db_pass'], d_db_user['db_user'])
        else:
            db_pass = d_db_user['db_pass']

        sql  = """update t_db_user
                  set  
                      inst_id         ='{0}',
                      db_user         ='{1}', 
                      db_pass         ='{2}', 
                      statement       ='{3}', 
                      status          ='{4}',
                      description     ='{5}',
                      created_date    = now()
                where id={16}""".format(d_db_user['inst_id'], d_db_user['db_user'],db_pass,
                                        d_db_user['statement'],d_db_user['status'],d_db_user['desc'],
                                        d_db_user['db_user_id'])
        print(sql)
        cr.execute(sql)
        cr.close()
        db.commit()
        result={}
        result['code']='0'
        result['message']='更新成功！'
    except :
        print(traceback.format_exc())
        result['code'] = '-1'
        result['message'] = '更新失败！'
    return result

def del_db_user(p_db_userid):
    result={}
    try:
        db = get_connection()
        cr = db.cursor()
        sql="delete from t_db_user  where id='{0}'".format(p_db_userid)
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


def check_db_user_rep(p_db_user):
    db = get_connection()
    cr = db.cursor()
    sql = "select count(0) from t_db_user  where  db_user='{0}'".format(p_db_user['db_user'])
    print(sql)
    cr.execute(sql)
    rs=cr.fetchone()
    cr.close()
    db.commit()
    return rs[0]

def check_db_user(p_db_user):
    result = {}

    if p_db_user["inst_id"]=="":
        result['code']='-1'
        result['message']='实例名不能为空!'
        return result

    if p_db_user["db_user"] == "":
        result['code'] = '-1'
        result['message'] = '用户名不能为空!'
        return result

    if p_db_user["db_pass"]=="":
        result['code']='-1'
        result['message']='口令不能为空!'
        return result

    if p_db_user["statement"]=="":
        result['code']='-1'
        result['message'] ='创建语句不能为空!'
        return result

    if p_db_user["status"] == "":
        result['code'] = '-1'
        result['message'] = '用户状态不能为空!'
        return result

    if p_db_user["desc"] == "":
        result['code'] = '-1'
        result['message'] = '用户描述不能为空!'
        return result

    if check_db_user_rep(p_db_user)>0:
        result['code'] = '-1'
        result['message'] = '用户名重复!'
        return result

    result['code'] = '0'
    result['message'] = '验证通过'
    return result

def get_port_by_portid(p_portid):
    db = get_connection()
    cr = db.cursor()
    sql = """select  id,app_name,app_port,app_dev,app_desc,app_ext from t_port where id={0}
          """.format(p_portid)
    print(sql)
    cr.execute(sql)
    rs = cr.fetchall()
    d_port = {}
    d_port['id']       = rs[0][0]
    d_port['app_name'] = rs[0][1]
    d_port['app_port'] = rs[0][2]
    d_port['app_dev']  = rs[0][3]
    d_port['app_desc'] = rs[0][4]
    d_port['app_ext']  = rs[0][5]
    cr.close()
    db.commit()
    print(d_port)
    return d_port

def imp_port(p_file):
    try:
        result={}
        file  = xlrd.open_workbook(p_file)
        name  = file.sheet_names()[0]
        sheet = file.sheet_by_name(name)
        vals  = ''
        for i in range(1, sheet.nrows):
            val=''
            for j in range(0, sheet.ncols):
                val=val+"'"+str(sheet.cell(i, j).value)+"',"
            vals =vals +'('+val[0:-1]+'),'

        db = get_connection()
        cr = db.cursor()
        sql="insert into t_port(app_name,app_port,app_dev,app_desc,app_ext) values {0}".format(vals[0:-1])
        print(sql)
        cr.execute(sql)
        cr.close()
        db.commit()
        result={}
        result['code']='0'
        result['message']='导入成功！'
    except :
        result['code'] = '-1'
        result['message'] = '导入失败！'
    return result

def set_styles(fontsize):
    cell_borders   = xlwt.Borders()
    header_borders = xlwt.Borders()
    header_styles  = xlwt.XFStyle()
    cell_styles    = xlwt.XFStyle()
    # add table header style
    header_borders.left   = xlwt.Borders.THIN
    header_borders.right  = xlwt.Borders.THIN
    header_borders.top    = xlwt.Borders.THIN
    header_borders.bottom = xlwt.Borders.THIN
    header_styles.borders = header_borders
    header_pattern = xlwt.Pattern()
    header_pattern.pattern = xlwt.Pattern.SOLID_PATTERN
    header_pattern.pattern_fore_colour = 22
    # add font
    font = xlwt.Font()
    font.name = 'Times New Roman'
    font.bold = True
    font.size = fontsize
    header_styles.font = font
    #add alignment
    header_alignment = xlwt.Alignment()
    header_alignment.horz = xlwt.Alignment.HORZ_CENTER
    header_alignment.vert = xlwt.Alignment.VERT_CENTER
    header_styles.alignment = header_alignment
    header_styles.borders = header_borders
    header_styles.pattern = header_pattern
    #add col style
    cell_borders.left     = xlwt.Borders.THIN
    cell_borders.right    = xlwt.Borders.THIN
    cell_borders.top      = xlwt.Borders.THIN
    cell_borders.bottom   = xlwt.Borders.THIN
    # add alignment
    cell_alignment        = xlwt.Alignment()
    cell_alignment.horz   = xlwt.Alignment.HORZ_LEFT
    cell_alignment.vert   = xlwt.Alignment.VERT_CENTER
    cell_styles.alignment = cell_alignment
    cell_styles.borders   = cell_borders
    font2 = xlwt.Font()
    font2.name = 'Times New Roman'
    font2.size = fontsize
    cell_styles.font = font2
    return header_styles,cell_styles

def exp_port(static_path):
    db  = get_connection()
    cr  = db.cursor()
    row_data  = 0
    workbook  = xlwt.Workbook(encoding='utf8')
    worksheet = workbook.add_sheet('port')
    header_styles, cell_styles = set_styles(15)
    os.system('cd {0}'.format(static_path + '/downloads/port'))
    file_name   = static_path + '/downloads/port/exp_port_{0}.xls'.format(current_rq())
    file_name_s = 'exp_port_{0}.xls'.format(current_rq())


    sql = "SELECT  a.app_name,a.app_port,a.app_dev,a.app_desc,a.app_ext FROM  t_port a  order by a.id"
    print(sql)
    cr.execute(sql)
    rs=cr.fetchall()
    desc = cr.description

    #写表头
    for k in range(len(desc)):
        worksheet.write(row_data, k, desc[k][0], header_styles)
        if k == len(desc) - 1:
            worksheet.col(k).width = 8000
        else:
            worksheet.col(k).width = 4000

    #写单元格
    row_data = row_data + 1
    for i in rs:
        for j in range(len(i)):
            if i[j] is None:
                worksheet.write(row_data, j, '', cell_styles)
            else:
                worksheet.write(row_data, j, str(i[j]), cell_styles)
        row_data = row_data + 1

    workbook.save(file_name)
    db.commit()
    cr.close()

    print("{0} export complete!".format(file_name))

    #生成zip压缩文件
    zip_file = static_path + '/downloads/port/exp_port_{0}.zip'.format(current_rq())
    rzip_file = '/static/downloads/port/exp_port_{0}.zip'.format(current_rq())

    #若文件存在则删除
    if os.path.exists(zip_file):
        os.system('rm -f {0}'.format(zip_file))

    z = zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED, allowZip64=True)
    z.write(file_name, arcname=file_name_s)
    z.close()
    print('zip_file=', zip_file)

    # 删除json文件
    os.system('rm -f {0}'.format(file_name))
    return rzip_file