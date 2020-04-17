#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/3 15:46
# @Author  : 马飞
# @File    : t_user.py
# @Software: PyCharm

from web.utils.common      import get_connection,current_rq,aes_encrypt,aes_decrypt
from web.model.t_user_role import del_user_roles,save_user_role,upd_user_role
from web.utils.common      import get_url_main,now,get_url_root,exception_info
from web.model.t_dmmx      import get_dmmc_from_dm

def logon_user_check(login_name,password,verify_code,verify_img):
    result={}
    result['url']=''
    print(login_name,password)
    if login_name == "":
        result['code'] = '-1'
        result['message'] = '用户名不能为空！'
        return result

    if password == "":
        result['code'] = '-1'
        result['message'] = '口令不能为空！'
        return result

    if verify_code == "":
        result['code'] = '-1'
        result['message'] = '验证码不能为空！'
        return result

    if check_user_exist(login_name)==0:
        result['code'] = '-1'
        result['message'] = '用户名不存在！'
        return result

    if get_user_by_loginame(login_name)['password']!=password:
        result['code'] = '-1'
        result['message'] = '口令有误！'
        return result

    if verify_code.upper()!=verify_img.upper():
        result['code'] = '-1'
        result['message'] = '验证码不正确！'
        return result

    if get_user_by_loginame(login_name)['status']=='0':
        result['code'] = '-1'
        result['message'] = '用户已禁用，请联系管理员！'
        return result

    if get_user_by_loginame(login_name)['expire_date']<now():
        result['code'] = '-1'
        result['message'] = '该用户已过期，请联系管理员！'
        return result

    result['code'] = '0'
    result['message'] ='验证成功！'
    result['url']=get_url_main()
    return result

def check_forget_password(login_name,email):
    result={}
    result['url']=''
    if login_name == "":
        result['code'] = '-1'
        result['message'] = '用户名不能为空！'
        return result

    if email == "":
        result['code'] = '-1'
        result['message'] = '邮箱不能为空！'
        return result

    if check_user_exist(login_name)==0:
        result['code'] = '-1'
        result['message'] = '用户名不存在！'
        return result

    if check_email_exist(login_name,email) == 0:
        result['code'] = '-1'
        result['message'] = '邮箱不正确！'
        return result

    if get_user_by_loginame(login_name)['status']=='0':
        result['code'] = '-1'
        result['message'] = '用户已禁用，请联系管理员！'
        return result

    if get_user_by_loginame(login_name)['expire_date']<now():
        result['code'] = '-1'
        result['message'] = '该用户已过期，请联系管理员！'
        return result

    result['code'] = '0'
    result['message'] ='验证成功！'
    result['url']=get_url_root()
    return result

def check_modify_password(newpass,reppass):
    result={}
    result['code']='0'
    if newpass == "":
        result['code'] = '-1'
        result['message'] = '新口令不能为空！'
        return result
    if reppass == "":
        result['code'] = '-1'
        result['message'] = '重复口令不能为空！'
        return result
    if  not (newpass == reppass) :
        result['code'] = '-1'
        result['message'] = '口令输入不一致！'
        return result
    return result

def save_forget_authention_string(p_username,p_auth_string):
    result = {}
    try:
        db = get_connection()
        cr = db.cursor()
        d_user=get_user_by_loginame(p_username)
        userid = d_user['userid']
        sql = """insert into t_forget_password(user_id,authentication_string,flag,creation_date,creator) 
                       values('{0}','{1}','{2}',{3},'DBA')
               """.format(userid, p_auth_string, 'valid',current_rq());
        print(sql)
        cr.execute(sql)
        cr.close()
        db.commit()
        result = {}
        result['code'] = '0'
        result['message'] = '保存成功！'
        return result
    except:
        result['code'] = '-1'
        result['message'] = '保存失败！'
    return result

def query_user(p_name):
    db = get_connection()
    cr = db.cursor()
    if p_name == "":
        sql = """select a.id,a.login_name,
                     CONCAT(a.file_path,'/',a.file_name) as user_image,
                     a.wkno,
                     a.name,
                     (select dmmc from t_dmmx where dm='04' and dmm=a.gender) as gender,
                     a.email,a.phone,
                     (select dmmc from t_dmmx where dm='18' and dmm=a.project_group) as project_group,
                     (select dmmc from t_dmmx where dm='01' and dmm=a.dept) as dept,
                     date_format(expire_date,'%Y-%m-%d') as expire_date,
                     case status when '1' then '启用'
                                 when '0' then '禁用'
                     end  status,
                     date_format(creation_date,'%Y-%m-%d')    creation_date,
                     date_format(last_update_date,'%Y-%m-%d') last_update_date 
                 from t_user a
                 order by convert(a.name using gbk) asc""".format(p_name)
    else:
        sql = """select a.id,a.login_name,
                     CONCAT(a.file_path,'/',a.file_name) as user_image,
                     a.wkno, 
                     name,
                     (select dmmc from t_dmmx where dm='04' and dmm=a.gender) as gender,
                     a.email,a.phone,
                     (select dmmc from t_dmmx where dm='18' and dmm=a.project_group) as project_group,
                     (select dmmc from t_dmmx where dm='01' and dmm=a.dept) as dept,
                     date_format(a.expire_date,'%Y-%m-%d') as expire_date,
                     case a.status when '1' then '启用'
                                 when '0' then '禁用'
                     end  status,
                     date_format(a.creation_date,'%Y-%m-%d')    creation_date,
                     date_format(a.last_update_date,'%Y-%m-%d') last_update_date 
                 from t_user a 
                where binary name like '%{0}%' or a.login_name like '%{1}%'                
                 order by convert(name using gbk) asc""".format(p_name,p_name)
    print(sql)
    cr.execute(sql)
    v_list = []
    for r in cr.fetchall():
        v_list.append(list(r))
    cr.close()
    db.commit()
    return v_list

def query_user_proj_privs(p_name,p_dsid,is_grants):
    db = get_connection()
    cr = db.cursor()
    if p_name == "":
        sql = """select u.id,u.login_name,u.name,u.email,u.phone,u.dept,
                       (select count(0) from t_user_proj_privs 
                        where proj_id='{0}' and user_id=u.id and priv_id='1') as query_priv,
                       (select count(0) from t_user_proj_privs 
                        where proj_id='{1}' and user_id=u.id and priv_id='2') as release_priv         
              from t_user  u order by convert(name using gbk) asc""".format(p_dsid,p_dsid)
    else:
        sql = """select u.id,u.login_name,u.name,u.email,u.phone,u.dept,
                       (select count(0) from t_user_proj_privs 
                        where proj_id='{0}' and user_id=u.id and priv_id='1') as query_priv,
                       (select count(0) from t_user_proj_privs 
                        where proj_id='{1}' and user_id=u.id and priv_id='2') as release_priv  
                 from t_user u 
                where binary u.name like '%{2}%'              
                 order by convert(name using gbk) asc""".format(p_dsid,p_dsid,p_name)
    print(sql)
    cr.execute(sql)
    v_list = []
    for r in cr.fetchall():
        v_list.append(list(r))
    cr.close()
    db.commit()
    return v_list

def get_userid():
    db = get_connection()
    cr = db.cursor()
    sql="select max(id)+1 from t_user"
    cr.execute(sql)
    rs = cr.fetchone()
    cr.close()
    db.commit()
    return rs[0]

def get_userid_by_auth(v_str):
    db = get_connection()
    cr = db.cursor()
    sql="select max(user_id) from t_forget_password where authentication_string='{0}'".format(v_str)
    cr.execute(sql)
    rs = cr.fetchone()
    cr.close()
    db.commit()
    return rs[0]

def get_records():
    db = get_connection()
    cr = db.cursor()
    sql="select count(0) from t_user "
    cr.execute(sql)
    rs = cr.fetchone()
    cr.close()
    db.commit()
    return rs[0]

def check_user_exist(p_login_name):
    db = get_connection()
    cr = db.cursor()
    sql="select count(0) from t_user where login_name='{0}'".format(p_login_name)
    print(sql)
    cr.execute(sql)
    rs = cr.fetchone()
    cr.close()
    db.commit()
    return rs[0]

def check_email_exist(p_login_name,p_email):
    db = get_connection()
    cr = db.cursor()
    sql="select count(0) from t_user where login_name='{0}' and email='{1}'".format(p_login_name,p_email)
    print(sql)
    cr.execute(sql)
    rs = cr.fetchone()
    cr.close()
    db.commit()
    return rs[0]

def check_auth_str_exist(p_auth_str):
    db = get_connection()
    cr = db.cursor()
    sql="select count(0) from t_forget_password where authentication_string='{0}'".format(p_auth_str)
    print(sql)
    cr.execute(sql)
    rs = cr.fetchone()
    cr.close()
    db.commit()
    if rs[0]==0:
        return False
    else:
        return True

def get_user_by_userid(p_userid):
    db = get_connection()
    cr = db.cursor()
    sql="""select cast(id as char) as id,login_name,name,password,gender,email,phone,dept,
                  date_format(expire_date,'%Y-%m-%d') as expire_date,status,file_path,file_name,project_group,wkno
        from t_user where id={0}""".format(p_userid)

    cr.execute(sql)
    rs = cr.fetchall()
    cr.close()
    db.commit()
    d_user={}
    d_user['userid']     = rs[0][0]
    d_user['loginname']  = rs[0][1]
    d_user['username']   = rs[0][2]
    d_user['password']   = aes_decrypt(rs[0][3],rs[0][1])
    d_user['gender']     = rs[0][4]
    d_user['email']      = rs[0][5]
    d_user['phone']      = rs[0][6]
    d_user['dept']       = rs[0][7]
    d_user['expire_date']= rs[0][8]
    d_user['status']     = rs[0][9]
    d_user['image_path'] = rs[0][10] if rs[0][10] else ''
    d_user['image_name'] = rs[0][11] if rs[0][11] else ''
    d_user['project_group'] = rs[0][12]
    d_user['wkno']          = rs[0][13]
    print("get_user_by_userid=",d_user,rs[0][3],rs[0][1])
    return d_user

def get_users(p_dept):
    db  = get_connection()
    cr  = db.cursor()
    sql = """select id,name from t_user  WHERE dept='{0}' order by id""".format(p_dept)
    cr.execute(sql)
    v_list = []
    for r in cr.fetchall():
        v_list.append(list(r)) 
    cr.close()
    return v_list


def get_logon_user():
    db = get_connection()
    cr = db.cursor()
    sql="select cast(id as char) as id,login_name,name,password,gender,email,phone,dept,date_format(expire_date,'%Y-%m-%d') as expire_date,status " \
        "from t_user_logon limit 1"
    cr.execute(sql)
    rs = cr.fetchall()
    cr.close()
    db.commit()
    d_user={}
    d_user['userid']      = rs[0][0]
    d_user['loginname']   = rs[0][1]
    d_user['username']    = rs[0][2]
    d_user['password']    = aes_decrypt(rs[0][3],rs[0][1])
    d_user['gender']      = rs[0][4]
    d_user['email']       = rs[0][5]
    d_user['phone']       = rs[0][6]
    d_user['dept']        = rs[0][7]
    d_user['expire_date'] = rs[0][8]
    d_user['status']      = rs[0][9]
    print("get_logon_user=",d_user)
    return d_user

def get_user_by_loginame(p_login_name):
    db = get_connection()
    cr = db.cursor()
    sql= """select cast(id as char) as id,
                name,
                login_name,
                password,gender,
                email,
                phone,
                dept,
                date_format(expire_date,'%Y-%m-%d') as expire_date,
                status,
                file_path,
                file_name,
                project_group,
                wkno
         from t_user where login_name='{0}'
        """.format(p_login_name)
    cr.execute(sql)
    rs = cr.fetchall()
    cr.close()
    db.commit()
    d_user={}
    d_user['userid']      = str(rs[0][0])
    d_user['username']    = rs[0][1]
    d_user['loginname']   = rs[0][2]
    d_user['password']    = aes_decrypt(rs[0][3],rs[0][2])
    d_user['gender']      = rs[0][4]
    d_user['gender_cn']   = get_dmmc_from_dm('04',rs[0][4])
    d_user['email']       = rs[0][5]
    d_user['phone']       = rs[0][6]
    d_user['dept']        = rs[0][7]
    d_user['dept_cn']     = get_dmmc_from_dm('01',rs[0][7])
    d_user['expire_date'] = rs[0][8]
    d_user['status']      = rs[0][9]
    d_user['file_path']   = rs[0][10]
    d_user['file_name']   = rs[0][11]
    d_user['project_group'] = rs[0][12]
    d_user['wkno']          = rs[0][13]
    return d_user

def check_user(p_user):
    result = {}
    if p_user["login"] == "":
        result['code'] = '-1'
        result['message'] = '登陆名不能为空！'
        return result

    if p_user["user"] == "":
        result['code'] = '-1'
        result['message'] = '姓名不能为空！'
        return result

    if p_user["pass"] == "":
        result['code'] = '-1'
        result['message'] = '口令不能为空！'
        return result

    if p_user["gender"] == "":
        result['code'] = '-1'
        result['message'] = '性别不能为空！'
        return result

    if p_user["dept"] == "":
        result['code'] = '-1'
        result['message'] = '部门不能为空！'
        return result

    if p_user["email"] == "":
        result['code'] = '-1'
        result['message'] = '邮箱不能为空！'
        return result

    if p_user["phone"] == "":
        result['code'] = '-1'
        result['message'] = '联系方式不能为空！'
        return result

    if p_user["expire_date"] == "":
        result['code'] = '-1'
        result['message'] = '过期日期不能为空！'
        return result

    if p_user["privs"][0] is None or p_user["privs"][0]=='':
        result['code'] = '-1'
        result['message'] = '用户角色不能为空！'
        return result

    if check_user_exist(p_user["login"] ) > 0:
        result['code'] = '-1'
        result['message'] = '用户名已存在！'
        return result


    #登陆名不能重复,且登陆名只能是小写字母

    #姓名配汉字：姓名只能输入汉字

    #密码规则：必须含大小写字母和数字，长度必须为6位以上

    #手机号规则：11个非零打头

    #邮箱规则：配置邮箱规则

    result['code'] = '0'
    result['message'] = '验证通过'
    return result

def save_user(p_user):
    result = {}
    val = check_user(p_user)
    if val['code'] == '-1':
        return val

    try:
        db = get_connection()
        cr = db.cursor()
        userid       = get_userid()
        loginname    = p_user['login']
        wkno         = p_user['wkno']
        username     = p_user['user']
        password     = aes_encrypt(p_user['pass'],loginname)
        gender       = p_user['gender']
        email        = p_user['email']
        phone        = p_user['phone']
        proj_group   = p_user['proj_group']
        dept         = p_user['dept']
        expire_date  = p_user['expire_date']
        status       = p_user['status']
        privs        = p_user['privs']
        file_path    = p_user['file_path']
        file_name    = p_user['file_name']

        if file_path=='':
           file_path = '/static/assets/images/users'

        if  file_name=='':
            if gender=='1':
                file_name = 'boy.png'
            else:
                file_name = 'girl.png'

        print(username,wkno,password,gender,email,phone,proj_group,dept,expire_date,file_path,file_name)
        sql="""insert into t_user(id,login_name,wkno,name,password,gender,email,phone,project_group,dept,expire_date,status,file_path,file_name,creation_date,creator,last_update_date,updator) 
                    values('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}','{13}','{14}','{15}','{16}','{17}')
            """.format(userid,loginname,wkno,username,password,gender,email,phone,proj_group,dept,expire_date,status,file_path,file_name,current_rq(),'DBA',current_rq(),'DBA');
        print(sql)
        cr.execute(sql)

        save_user_role(userid,privs)
        cr.close()
        db.commit()
        result={}
        result['code']='0'
        result['message']='保存成功！'
        return result
    except Exception as e:
        print(e)
        result['code'] = '-1'
        result['message'] = '保存失败！'
        return result

def save_user_proj_privs(d_proj):
    result = {}
    dsid = d_proj['dsid']
    userid = d_proj['userid']
    priv_query   = d_proj['priv_query']
    priv_release = d_proj['priv_release']
    priv_audit   = d_proj['priv_audit']
    priv_execute = d_proj['priv_execute']
    priv_order   = d_proj['priv_order']

    try:
        db = get_connection()
        cr = db.cursor()

        #process query privs
        if priv_query=='1':
           sql = """delete from  t_user_proj_privs 
                       where proj_id='{0}' and user_id='{1}' and priv_id='1'""".format(dsid,userid)
           cr.execute(sql)
           sql = """insert into t_user_proj_privs(proj_id,user_id,priv_id) 
                        values('{0}','{1}','{2}') """.format(dsid,userid, '1')
           cr.execute(sql)
        else:
            sql = """delete from  t_user_proj_privs 
                        where proj_id='{0}' and user_id='{1}' and priv_id='1'""".format(dsid, userid)
            cr.execute(sql)

        # process release privs
        if priv_release == '1':
            sql = """delete from  t_user_proj_privs 
                        where proj_id='{0}' and user_id='{1}' and priv_id='2'""".format(dsid, userid)
            cr.execute(sql)
            sql = """insert into t_user_proj_privs(proj_id,user_id,priv_id) 
                           values('{0}','{1}','{2}') """.format(dsid, userid, '2')
            cr.execute(sql)
        else:
            sql = """delete from  t_user_proj_privs 
                         where proj_id='{0}' and user_id='{1}' and priv_id='2'""".format(dsid, userid)
            cr.execute(sql)

        # process audit privs
        if priv_audit == '1':
            sql = """delete from  t_user_proj_privs 
                           where proj_id='{0}' and user_id='{1}' and priv_id='3'""".format(dsid, userid)
            cr.execute(sql)
            sql = """insert into t_user_proj_privs(proj_id,user_id,priv_id) 
                              values('{0}','{1}','{2}') """.format(dsid, userid, '3')
            cr.execute(sql)
        else:
            sql = """delete from  t_user_proj_privs 
                            where proj_id='{0}' and user_id='{1}' and priv_id='3'""".format(dsid, userid)
            cr.execute(sql)

        #process execute privs
        if priv_execute == '1':
            sql = """delete from  t_user_proj_privs 
                         where proj_id='{0}' and user_id='{1}' and priv_id='4'""".format(dsid, userid)
            cr.execute(sql)
            sql = """insert into t_user_proj_privs(proj_id,user_id,priv_id) 
                         values('{0}','{1}','{2}') """.format(dsid, userid, '4')
            cr.execute(sql)
        else:
            sql = """delete from  t_user_proj_privs 
                          where proj_id='{0}' and user_id='{1}' and priv_id='4'""".format(dsid, userid)
            cr.execute(sql)

        #process order privs
        if priv_order == '1':
            sql = """delete from  t_user_proj_privs 
                            where proj_id='{0}' and user_id='{1}' and priv_id='5'""".format(dsid, userid)
            cr.execute(sql)
            sql = """insert into t_user_proj_privs(proj_id,user_id,priv_id) 
                            values('{0}','{1}','{2}') """.format(dsid, userid, '5')
            cr.execute(sql)
        else:
            sql = """delete from  t_user_proj_privs 
                             where proj_id='{0}' and user_id='{1}' and priv_id='5'""".format(dsid, userid)
            cr.execute(sql)

        cr.close()
        db.commit()
        result={}
        result['code']='0'
        result['message']='保存成功！'
        return result
    except:
        exception_info()
        result['code'] = '-1'
        result['message'] = '保存失败！'
    return result

def upd_user(p_user):
    result={}
    try:
        db = get_connection()
        cr = db.cursor()
        userid      = p_user['userid']
        loginname   = p_user['loginname']
        wkno        = p_user['wkno']
        username    = p_user['username']
        password    = aes_encrypt(p_user['password'],loginname)
        gender      = p_user['gender']
        email       = p_user['email']
        phone       = p_user['phone']
        proj_group  = p_user['proj_group']
        dept        = p_user['dept']
        expire_date = p_user['expire_date']
        status      = p_user['status']
        roles       = p_user['roles']
        file_path   = p_user['file_path']
        file_name   = p_user['file_name']

        if file_path == '':
            file_path = '/static/assets/images/users'

        if file_name == '':
            if gender == '1':
                file_name = 'boy.png'
            else:
                file_name = 'girl.png'

        sql="""update t_user 
                  set  name     ='{0}',
                       login_name='{1}',
                       password ='{2}',
                       gender   ='{3}',
                       email    ='{4}',
                       phone    ='{5}',
                       dept     ='{6}',
                       expire_date      ='{7}' ,
                       status           ='{8}' ,
                       last_update_date ='{9}' ,
                       updator   ='{10}',
                       file_path ='{11}',
                       file_name = '{12}',
                       project_group = '{13}',
                       wkno          = '{14}'
                where id='{15}'""".format(username,loginname,password,gender,email,phone,dept,expire_date,status,
                                          current_rq(),'DBA',file_path,file_name,proj_group,wkno,userid)
        print("upd_user=",sql)
        cr.execute(sql)
        upd_user_role(userid,roles)
        cr.close()
        db.commit()
        result={}
        result['code']='0'
        result['message']='更新成功！'
    except :
        exception_info()
        result['code'] = '-1'
        result['message'] = '更新失败！'
    return result

def upd_password(p_user):
    result={}
    try:
        db = get_connection()
        cr = db.cursor()
        userid      = p_user['userid']
        loginname   = p_user['loginname']
        password    = aes_encrypt(p_user['password'],loginname)
        sql="""update t_user 
                  set  password ='{0}',                    
                       last_update_date ='{1}' ,
                       updator='{2}'
                where id='{3}'""".format(password,current_rq(),'DBA',userid)
        print("upd_password=",sql)
        cr.execute(sql)
        cr.close()
        db.commit()
        result={}
        result['code']='0'
        result['message']='更新成功！'
    except :
        exception_info()
        result['code'] = '-1'
        result['message'] = '更新失败！'
    return result

def del_user(p_user):
    result={}
    try:
        db = get_connection()
        cr = db.cursor()
        userid   = p_user['userid']
        sql="delete from t_user  where id='{0}'".format(userid)
        print(sql)
        cr.execute(sql)
        cr.close()
        del_user_roles(userid);
        db.commit()
        result={}
        result['code']='0'
        result['message']='删除成功！'
    except :
        result['code'] = '-1'
        result['message'] = '删除失败！'
    return result

def get_sys_roles(p_userid):
    db = get_connection()
    cr = db.cursor()
    sql="""select cast(id as char) as id,name 
           from t_role
           where status='1'
             and id not in(select role_id from t_user_role where user_id='{0}')      
        """.format(p_userid)
    print(sql)
    cr.execute(sql)
    v_list = []
    for r in cr.fetchall():
        v_list.append(list(r))
    cr.close()
    db.commit()
    return v_list

def get_user_roles(p_userid):
    db = get_connection()
    cr = db.cursor()
    sql="""select cast(id as char) as id,name
           from t_role 
            where status='1'  
              and id  in(select role_id from t_user_role where user_id='{0}')    
        """.format(p_userid)
    print(sql)
    cr.execute(sql)
    v_list = []
    for r in cr.fetchall():
        v_list.append(list(r))
    cr.close()
    db.commit()
    return v_list