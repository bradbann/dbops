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

def query_inst_list():
    db = get_connection()
    cr = db.cursor()
    sql = """SELECT  a.id,a.inst_name FROM  t_db_inst a  order by a.created_date"""
    print(sql)
    cr.execute(sql)
    v_list = []
    for r in cr.fetchall():
        v_list.append(list(r))
    cr.close()
    db.commit()
    return v_list

def query_inst(inst_name):
    db = get_connection()
    cr = db.cursor()
    v_where =''
    if inst_name != '':
        v_where = "  where ( t.inst_name like '%{0}%' or  t.app_dev like '%{1}%')".format(inst_name,inst_name)

    sql = """SELECT  a.id,
                     a.inst_name,
                     a.inst_ip,
                     a.inst_port,
                     a.inst_type,
                     (select dmmc from t_dmmx x where x.dm='02' and x.dmm=a.inst_type) as inst_type,
                     date_format(a.created_date,'%Y-%m-%d %h:%i:%s')  as created_date
            FROM  t_db_inst a
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

def save_db_inst(d_inst):
    result = {}
    val=check_db_inst(d_inst)
    if val['code']=='-1':
        return val
    try:
        db               = get_connection()
        cr               = db.cursor()
        result           = {}

        inst_pass = ''
        if d_inst['mgr_pass'] != '':
            inst_pass = aes_encrypt(d_inst['mgr_pass'], d_inst['mgr_user'])
        else:
            inst_pass = d_inst['mgr_pass']

        sql="""insert into t_db_inst(inst_name,inst_ip,inst_port,inst_type,mgr_user,mgr_pass,start_script,stop_script,restart_script,auto_start_script,created_date)
                   values('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}',now())
            """.format(d_inst['inst_name'],d_inst['inst_ip'],d_inst['inst_port'],
                       d_inst['inst_type'],d_inst['mgr_user'],inst_pass,
                       d_inst['start_script'],d_inst['stop_script'],d_inst['restart_script'],
                       d_inst['auto_start_script']
                       )
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

def upd_db_inst(d_inst):
    result={}
    val = check_db_inst(d_inst)
    if  val['code'] == '-1':
        return val
    try:
        db   = get_connection()
        cr   = db.cursor()

        inst_pass = ''
        if d_inst['mgr_pass'] != '':
            inst_pass = aes_encrypt(d_inst['mgr_pass'], d_inst['mgr_user'])
        else:
            inst_pass = d_inst['mgr_pass']


        sql  = """update t_db_inst
                  set  
                      inst_name         ='{0}',
                      inst_ip           ='{1}', 
                      inst_port         ='{2}', 
                      inst_type         ='{3}', 
                      mgr_user          ='{4}',
                      mgr_pass          ='{5}',
                      start_script      ='{6}',
                      stop_script       ='{7}',
                      restart_script    ='{8}',
                      auto_start_script ='{9}',
                      created_date =now()
                where id={10}""".format(d_inst['inst_name'],d_inst['inst_ip'],d_inst['inst_port'],
                       d_inst['inst_type'],d_inst['mgr_user'],inst_pass,
                       d_inst['start_script'],d_inst['stop_script'],d_inst['arestart_script'],
                       d_inst['auto_start_script'],d_inst['inst_id'])
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

def del_db_inst(p_instid):
    result={}
    try:
        db = get_connection()
        cr = db.cursor()
        sql="delete from t_db_inst  where id='{0}'".format(p_instid)
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


def check_inst_rep(d_inst):
    db = get_connection()
    cr = db.cursor()
    sql = "select count(0) from t_db_inst  where  inst_ip='{0}' and inst_port='{1}'".\
           format(d_inst['inst_ip'],d_inst['inst_port'])
    print(sql)
    cr.execute(sql)
    rs=cr.fetchone()
    cr.close()
    db.commit()
    return rs[0]

def check_db_inst(p_inst):
    result = {}

    if p_inst["inst_name"]=="":
        result['code']='-1'
        result['message']='实例名不能为空!'
        return result

    if p_inst["inst_ip"] == "":
        result['code'] = '-1'
        result['message'] = '实例地址不能为空!'
        return result

    if p_inst["inst_port"]=="":
        result['code']='-1'
        result['message']='实例端口不能为空!'
        return result

    if p_inst["inst_type"]=="":
        result['code']='-1'
        result['message']='实例类型不能为空!'
        return result

    if check_inst_rep(p_inst)>0:
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