#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2018/9/19 15:17
# @Author : 马飞
# @File : user.py.py
# @Software: PyCharm

######################################################################################
#                                                                                    #
#                                   用户管理                                          #
#                                                                                    #
######################################################################################

import json
import uuid
import tornado.web
from web.model.t_role  import get_roles
from web.model.t_user  import save_user,get_user_by_userid,upd_user,del_user,query_user,query_user_proj_privs
from web.model.t_user  import get_sys_roles,get_user_roles,save_user_proj_privs,init_user_proj_privs
from web.model.t_dmmx  import get_dmm_from_dm
from web.model.t_xtqx  import check_url
from web.model.t_ds    import query_project
from web.utils.common  import get_url_root

class userquery(tornado.web.RequestHandler):
    def get(self):
        userid   = str(self.get_secure_cookie("userid"), encoding="utf-8")
        if userid:
            if check_url(userid,self.request.uri):
                self.render("user_query.html")
            else:
                self.render("page-500.html")
        else:
            self.render("page-404.html")


class useradd(tornado.web.RequestHandler):
    def get(self):
        roles  = get_roles()
        gender = get_dmm_from_dm('04')
        dept   = get_dmm_from_dm('01')
        print('gender=',gender)
        print('dept=',dept)
        print('roles=',roles)
        self.render("./user_add.html",
                    roles=roles,
                    gender=gender,
                    dept=dept)

class useradd_save(tornado.web.RequestHandler):
    def post(self):
        d_user={}
        d_user['login']        = self.get_argument("login")
        d_user['user']         = self.get_argument("user")
        d_user['pass']         = self.get_argument("pass")
        d_user['gender']       = self.get_argument("gender")
        d_user['email']        = self.get_argument("email")
        d_user['phone']        = self.get_argument("phone")
        d_user['dept']         = self.get_argument("dept")
        d_user['expire_date']  = self.get_argument("expire_date")
        d_user['status']       = self.get_argument("status")
        d_user['privs']        = self.get_argument("privs").split(",")
        d_user['file_path']    = self.get_argument("file_path")
        d_user['file_name']    = self.get_argument("file_name")
        print('d_user=',d_user)
        result=save_user(d_user)
        self.write({"code": result['code'], "message": result['message']})

class useradd_save_uploadImage(tornado.web.RequestHandler):
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        static_path = self.get_template_path().replace("templates", "static")
        #username    = str(self.get_secure_cookie("username"), encoding="utf-8")
        file_metas  = self.request.files["file"]
        #username    = self.request.files["username"]
        username = self.get_argument("username")
        print('username=',username)

        try:
            for meta in file_metas:
                file_path = static_path+'/'+'assets/images/users'
                file_name=str(uuid.uuid1())+'_'+username+'.'+meta['filename'].split('.')[-1]
                print('file_path=',file_path)
                print('file_name=', file_name)
                with open(file_path+'/'+file_name, 'wb') as up:
                    up.write(meta['body'])
            self.write({"code": 0, "file_path": '/static/assets/images/users',"file_name":file_name})
        except Exception as e:
            print(e)
            self.write({"code": -1, "message": '保存图片失败'+str(e)})


class userchange(tornado.web.RequestHandler):
    def get(self):
        self.render("./user_change.html",url=get_url_root())

class useredit(tornado.web.RequestHandler):
    def get(self):
        userid  = self.get_argument("userid")
        d_user  = get_user_by_userid(userid)
        genders = get_dmm_from_dm('04')
        depts   = get_dmm_from_dm('01')
        print('sys_roles=',get_sys_roles(userid))
        print('user_roles=', get_user_roles(userid))
        self.render("./user_edit.html",
                     userid      = d_user['userid'],
                     loginname   = d_user['loginname'],
                     username    = d_user['username'],
                     password    = d_user['password'],
                     gender      = d_user['gender'],
                     email       = d_user['email'],
                     phone       = d_user['phone'],
                     dept        = d_user['dept'],
                     expire_date = d_user['expire_date'],
                     status      = d_user['status'],
                     image_path  = d_user['image_path'],
                     image_name  = d_user['image_name'],
                     user_image  = d_user['image_path']+'/'+d_user['image_name'],
                     sys_roles   = get_sys_roles(userid),
                     user_roles  = get_user_roles(userid),
                     url         = get_url_root(),
                     genders     = genders,
                     depts       = depts
                    )

class useredit_save(tornado.web.RequestHandler):
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        d_user={}
        d_user['userid']      = self.get_argument("userid")
        d_user['loginname']   = self.get_argument("loginname")
        d_user['username']    = self.get_argument("username")
        d_user['password']    = self.get_argument("password")
        d_user['gender']      = self.get_argument("gender")
        d_user['email']       = self.get_argument("email")
        d_user['phone']       = self.get_argument("phone")
        d_user['dept']        = self.get_argument("dept")
        d_user['expire_date'] = self.get_argument("expire_date")
        d_user['status']      = self.get_argument("status")
        d_user['status']      = self.get_argument("status")
        d_user['roles']       = self.get_argument("roles").split(",")
        print('useredit_save=',d_user['roles'] )
        d_user['file_path']   = self.get_argument("file_path")
        d_user['file_name']   = self.get_argument("file_name")

        result=upd_user(d_user)
        self.write({"code": result['code'], "message": result['message']})

class useredit_del(tornado.web.RequestHandler):
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        d_user={}
        d_user['userid']   = self.get_argument("userid")
        result=del_user(d_user)
        self.write({"code": result['code'], "message": result['message']})

class user_query(tornado.web.RequestHandler):
    def get(self):
        self.render("page-500.html")

    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        qname = self.get_argument("qname")
        v_list = query_user(qname)
        v_json = json.dumps(v_list)
        print(v_json)
        self.write(v_json)
        # userid = str(self.get_secure_cookie("userid"), encoding="utf-8")
        # if userid:
        #     if check_url(userid, self.request.uri):
        #         qname = self.get_argument("qname")
        #         v_list = query_user(qname)
        #         v_json = json.dumps(v_list)
        #         print(v_json)
        #         self.write(v_json)
        #     else:
        #         self.render("page-500.html")
        # else:
        #     self.render("page-500.html")



class user_init_proj_privs(tornado.web.RequestHandler):
    def get(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        dsid = self.get_argument("dsid")
        v_list=init_user_proj_privs(dsid);
        v_dict = {"data": v_list}
        v_json = json.dumps(v_dict)
        self.write(v_json)

class project_privs_query(tornado.web.RequestHandler):
    def post(self):
        print('project_privs_query,,,,,,,,,,,,,,,,,,,,,,,,,,')
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        qname = self.get_argument("qname")
        dsid  = self.get_argument("dsid")
        v_list=query_user_proj_privs(qname,dsid)
        v_json = json.dumps(v_list)
        self.write(v_json)

class check(tornado.web.RequestHandler):
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        qname = self.get_argument("qname")
        if qname == '':
            self.write('{"code":"-1","message":"用户名不能为空!"}')
        else:
            self.write('{"code":"0","message":"验证成功！"}')

class projectquery(tornado.web.RequestHandler):
    def get(self):
        #self.render("./projectquery.html",url=get_url_root())
        self.render("./projectquery.html")

class project_query(tornado.web.RequestHandler):
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        qname  = self.get_argument("qname")
        v_list = query_project(qname)
        v_json = json.dumps(v_list)
        self.write(v_json)

class projectprivs(tornado.web.RequestHandler):
    def get(self):
        dsid=self.get_argument("dsid")
        #self.render("./projectprivs.html",dsid=dsid,url=get_url_root())
        self.render("./projectprivs.html", dsid=dsid)

class projectprivs_save(tornado.web.RequestHandler):
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        d_proj={}
        d_proj['dsid']          = self.get_argument("dsid")
        d_proj['userid']        = self.get_argument("userid")
        d_proj['priv_query']    = self.get_argument("priv_query")
        d_proj['priv_release']  = self.get_argument("priv_release")
        print('d_proj=',d_proj)
        result=save_user_proj_privs(d_proj)
        self.write({"code": result['code'], "message": result['message']})

class forget_password(tornado.web.RequestHandler):
    def get(self):
        self.render("./user/forget_password.html",url=get_url_root())
