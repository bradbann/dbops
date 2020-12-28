#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2018/9/19 15:28
# @Author : 马飞
# @File : logon.py.py
# @Software: PyCharm

######################################################################################
#                                                                                    #
#                                   用户登陆                                          #
#                                                                                    #
######################################################################################

import tornado.web
import random,os,json
import time
from web.model.t_user  import logon_user_check,check_forget_password,check_modify_password,save_forget_authention_string,check_auth_str_exist,get_userid_by_auth
from web.model.t_user  import upd_password,get_user_by_userid,get_user_by_loginame,get_user_roles,check_authcode
from web.model.t_xtqx  import get_tree_by_userid
from web.model.t_dmmx  import get_dmm_from_dm
from web.utils.common  import send_mail,get_rand_str,current_time,china_rq,china_week,welcome,china_time
from PIL import Image,ImageDraw,ImageFont
from web.utils.basehandler import basehandler

class logon(tornado.web.RequestHandler):
    def get(self):
        self.render("page-login.html")

class index(basehandler):
    @tornado.web.authenticated
    def get(self):
        username    = str(self.get_secure_cookie("username"), encoding="utf-8")
        userid      = str(self.get_secure_cookie("userid"), encoding="utf-8")
        d_user      = get_user_by_loginame(username)
        genders     = get_dmm_from_dm('04')
        depts       = get_dmm_from_dm('01')
        proj_groups = get_dmm_from_dm('18')
        print('index->userid=',userid)
        if username:
           self.render("index.html",
                       china_rq    = china_rq(),
                       china_week  = china_week(),
                       china_time  = china_time(),
                       welcome     = welcome(d_user['username']),
                       userid      = d_user['userid'],
                       loginname   = d_user['loginname'],
                       wkno        = d_user['wkno'],
                       username    = d_user['username'],
                       password    = d_user['password'],
                       gender      = d_user['gender'],
                       email       = d_user['email'],
                       phone       = d_user['phone'],
                       proj_group  = d_user['project_group'],
                       dept        = d_user['dept'],
                       expire_date = d_user['expire_date'],
                       status      = d_user['status'],
                       file_path   = d_user['file_path'],
                       file_name   = d_user['file_name'],
                       user_image  = d_user['file_path']+'/'+d_user['file_name'],
                       user_roles  = get_user_roles(userid),
                       genders     = genders,
                       depts       = depts,
                       d_user      = d_user,
                       proj_groups = proj_groups,
                       view_url    = self.get_secure_cookie("view_url")
                       )
        else:
           self.render("page-404.html")

class main(basehandler):
    @tornado.web.authenticated
    def get(self):
        self.render("main.html")

class tree(tornado.web.RequestHandler):
    def post(self):
        result={}
        msg=get_tree()
        result['code'] = 0
        result['message']=msg
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self.write({"code": result['code'], "message": result['message']})

class unlock(basehandler):
    def post(self):
        unlock_password = self.get_argument("unlock_password")
        username = str(self.get_secure_cookie("username"), encoding="utf-8")
        d_user   = get_user_by_loginame(username)
        if d_user['password']==unlock_password:
            self.set_secure_cookie("screen_lock_status", 'unlock')
            self.set_secure_cookie("heartbeat", 'health', expires=time.time() + 300)
            self.write({"code":0})
        else:
            self.write({"code":-1})

class lock(basehandler):
    def post(self):
        self.set_secure_cookie("screen_lock_status", 'locked')
        self.write({"code":0})

class heartbeat(tornado.web.RequestHandler):
    def post(self):
        status = self.get_secure_cookie("heartbeat")
        print('heartbeat=',status)
        if status is None:
            self.write({"code": 'undefined'})
        else:
            self.write({"code": str(status, encoding="utf-8")})


class lock_status(tornado.web.RequestHandler):
  def post(self):
      status = self.get_secure_cookie("screen_lock_status")
      if status is None:
         self.write({"code": 'undefined'})
      else:
         self.write({"code": str(status, encoding="utf-8")})


class get_time(tornado.web.RequestHandler):
    def post(self):
        self.write(china_time())

class logout(tornado.web.RequestHandler):
    def get(self):
        self.set_secure_cookie("username", '',expires_days=None)
        self.set_secure_cookie("userid", '', expires_days=None)
        self.set_secure_cookie("screen_lock_status", 'unlock')
        self.render("page-logout.html")

class error(tornado.web.RequestHandler):
    def get(self):
        self.render("page-500.html")

class logon_welcome(tornado.web.RequestHandler):
    def get(self):
        self.render("./main/welcome.html")

class logon_check(basehandler):
    def post(self):
        username    = self.get_argument("username")
        password    = self.get_argument("password")
        verify_code = self.get_argument("verify_code")
        verify_img  = str(self.get_secure_cookie("verify_img"), encoding="utf-8")
        result = logon_user_check(username, password, verify_code, verify_img)
        if result['code'] == '0':
            d_user=get_user_by_loginame(username)
            self.set_secure_cookie("username", username,expires=time.time() + 1800)
            self.set_secure_cookie("userid", d_user['userid'], expires=time.time() + 1800)
            self.set_secure_cookie("screen_lock_status", 'unlock')
            self.set_secure_cookie("heartbeat", 'health', expires=time.time() + 300)
        self.write({"code": result['code'], "message": result['message'], "url": result['url']})

class forget_password(tornado.web.RequestHandler):
    def get(self):
        self.render("./user/forget_password.html")

class forget_password_check_user(tornado.web.RequestHandler):
    def post(self):
        user        = self.get_argument("user")
        email       = self.get_argument("email")
        result      = check_forget_password(user,email)
        print('forget_password_check_user=',user,email,result)

        if result['code']=='0':
           auth_string = get_rand_str(64)
           while check_auth_str_exist(auth_string):
               auth_string = get_rand_str(64)
           ret = save_forget_authention_string(user,auth_string)
           # if ret['code']=='-1':
           #    self.write({"code": ret['code'], "message": result['message']})

           v_title='用户:{0} 口令变更激活邮件.{1}'.format(user,current_time())
           v_content = """<p><h4>用户名：{}</h4><p><h4>授权码：{}</h4><p><h4>有效期：1分钟</h4>""".format(user,auth_string)
           send_mail('190343@lifeat.cn', 'Hhc5HBtAuYTPGHQ8', email, v_title, v_content)

           self.write({"code": '0', "message": '授权码已发送至邮箱!'})
        else:
           self.write({"code": result['code'], "message": result['message']})

class modify_password(tornado.web.RequestHandler):
    def get(self):
        auth_str    = self.get_argument("id")
        print("auth_str=",auth_str)
        self.render("./user/modify_password.html", auth_str=auth_str)

class forget_password_check_auth(tornado.web.RequestHandler):
    def post(self):
        user     = self.get_argument("user")
        auth     = self.get_argument("auth")
        result   = check_authcode(user,auth)
        self.write({"code": result['code'], "message": result['message']})

class forget_password_check_pass(tornado.web.RequestHandler):
    def post(self):
        user    = self.get_argument("user")
        auth    = self.get_argument("auth")
        newpass = self.get_argument("newpass")
        reppass = self.get_argument("reppass")
        result  = check_modify_password(user, newpass, reppass, auth)
        if result['code'] == '-1':
            self.write({"code": result['code'], "message": result['message']})
        else:
            p_userid = get_userid_by_auth(auth)
            p_user = get_user_by_userid(p_userid)
            p_user['password'] = newpass
            result2 = upd_password(p_user)
            self.write({"code": result2['code'], "message": result2['message']})

class tree(tornado.web.RequestHandler):
    def get(self):
        self.render("./tree/tree.html")

class get_tree(tornado.web.RequestHandler):
    def post(self):
        logon_name = str(self.get_secure_cookie("username"), encoding="utf-8")
        result=get_tree_by_userid(logon_name)
        self.write({"code": result['code'], "message": result['message']})

class get_verify(tornado.web.RequestHandler):
    def post(self):
        # 定义使用Image类实例化一个长为120px,宽为30px,基于RGB的(255,255,255)颜色的图片
        img1 = Image.new(mode="RGB", size=(120, 30), color=(255, 255, 255))
        # 实例化一支画笔
        draw1 = ImageDraw.Draw(img1, mode="RGB")
        # 定义要使用的字体
        font1 = ImageFont.truetype("TIMES.TTF", 28)
        verify_img=''
        for i in range(5):
            # 每循环一次,从a到z中随机生成一个字母或数字
            # 65到90为字母的ASCII码,使用chr把生成的ASCII码转换成字符
            # str把生成的数字转换成字符串
            char1 = random.choice([chr(random.randint(65, 90)), str(random.randint(0, 9)),chr(random.randint(97, 122))])
            # 每循环一次重新生成随机颜色
            color1 = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            # 把生成的字母或数字添加到图片上
            # 图片长度为120px,要生成5个数字或字母则每添加一个,其位置就要向后移动24px
            draw1.text([i * 24, 0], char1, color1, font=font1)
            #记录生成的验证码
            verify_img=verify_img+char1

        #将验证码字符写入cookie
        self.set_secure_cookie("verify_img", verify_img, expires_days=None)

        #删除以前生成的图片
        static_path = self.get_template_path().replace("templates","static");
        os.system("rm -rf  {0}".format(static_path + '/assets/images/logon/verify*.png'))
        # 把生成的图片保存为"pic.png"格式
        rand = random.randint(1000, 99999)
        file = static_path+'/assets/images/logon/verify' + str(rand) + '.png'
        with open(file, "wb") as f:
            img1.save(f, format="png")
        v_dict = {"image":file.split('/')[-1],"verify":verify_img}
        v_json = json.dumps(v_dict)
        self.write(v_json)

class forget_password(tornado.web.RequestHandler):
    def get(self):
        self.render("./forget_password.html")

class check(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        qname = self.get_argument("qname")
        if qname == '':
            self.write('{"code":"-1","message":"用户名不能为空!"}')
        else:
            self.write('{"code":"0","message":"验证成功！"}')