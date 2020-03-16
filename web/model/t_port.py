#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/30 15:46
# @Author  : 马飞
# @File    : t_user.py
# @Software: PyCharm

from web.utils.common import exception_info,get_connection
from web.utils.common import current_rq
import traceback
import xlrd,xlwt
import os,zipfile

def query_port(app_name):
    db = get_connection()
    cr = db.cursor()
    v_where =''
    if app_name != '':
        v_where = "  where ( t.app_name like '%{0}%' or  t.app_dev like '%{1}%')".format(app_name,app_name)

    sql = """SELECT * FROM (
                SELECT  a.id,
                     a.app_name,
                     a.app_port,
                     GROUP_CONCAT(b.name) AS app_dev,
                     a.app_desc,
                     a.app_ext        
                FROM  t_port a,t_user b
                WHERE INSTR(a.app_dev,b.id)>0   
                GROUP BY a.id,
                 a.app_name,
                 a.app_port,
                 a.app_dev,
                 a.app_desc,
                 a.app_ext) t {0}
          """.format(v_where)
    print(sql)
    cr.execute(sql)
    v_list = []
    for r in cr.fetchall():
        v_list.append(list(r))
    cr.close()
    db.commit()
    return v_list

def save_port(p_port):
    result = {}

    val=check_port(p_port)
    if val['code']=='-1':
        return val
    try:
        db               = get_connection()
        cr               = db.cursor()
        result           = {}
        app_name         = p_port['app_name']
        app_port         = p_port['app_port']
        app_dev          = p_port['app_dev']
        app_desc         = p_port['app_desc']
        app_ext          = p_port['app_ext']

        sql="""insert into t_port(app_name,app_port,app_dev,app_desc,app_ext) values('{0}','{1}','{2}','{3}','{4}')
            """.format(app_name,app_port,app_dev,app_desc,app_ext)
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

def upd_port(p_port):
    result={}
    val = check_port(p_port)
    if  val['code'] == '-1':
        return val
    try:
        db              = get_connection()
        cr              = db.cursor()
        port_id         = p_port['port_id']
        app_name        = p_port['app_name']
        app_port        = p_port['app_port']
        app_dev         = p_port['app_dev']
        app_desc        = p_port['app_desc']
        app_ext         = p_port['app_ext']

        sql="""update t_port
                  set  
                      app_name      ='{0}',
                      app_port      ='{1}', 
                      app_dev       ='{2}', 
                      app_desc      ='{3}', 
                      app_ext       ='{4}'                     
                where id={5}""".format(app_name,app_port,app_dev,app_desc,app_ext,port_id)
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

def del_port(p_portid):
    result={}
    try:
        db = get_connection()
        cr = db.cursor()
        sql="delete from t_port  where id='{0}'".format(p_portid)
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


def check_port_rep(p_port):
    db = get_connection()
    cr = db.cursor()
    sql = "select count(0) from t_port  where  instr(app_port,'{0}')>0".format(p_port['app_port'])
    print(sql)
    cr.execute(sql)
    rs=cr.fetchone()
    cr.close()
    db.commit()
    return rs[0]

def check_port(p_port):
    result = {}

    if p_port["app_name"]=="":
        result['code']='-1'
        result['message']='应用名不能为空!'
        return result

    if p_port["app_port"] == "":
        result['code'] = '-1'
        result['message'] = '端口号不能为空!'
        return result

    if p_port["app_dev"]=="":
        result['code']='-1'
        result['message']='开发者不能为空!'
        return result

    if p_port["app_desc"]=="":
        result['code']='-1'
        result['message']='应用描述不能为空!'
        return result

    if check_port_rep(p_port)>0:
        result['code'] = '-1'
        result['message'] = '端口号重复!'
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