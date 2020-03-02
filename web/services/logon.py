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

from web.model.t_user  import logon_user_check,check_forget_password,check_modify_password,save_forget_authention_string,check_auth_str_exist,get_userid_by_auth
from web.model.t_user  import upd_password,get_user_by_userid,get_user_by_loginame,get_user_roles
from web.model.t_xtqx  import get_tree_by_userid
from web.model.t_dmmx  import get_dmm_from_dm
from web.utils.common  import send_mail,get_rand_str,current_time,china_rq,china_week,welcome,china_time
from PIL import Image,ImageDraw,ImageFont

class logon(tornado.web.RequestHandler):
    def get(self):
        self.render("page-login.html")

class index(tornado.web.RequestHandler):
    def get(self):
        username  = str(self.get_secure_cookie("username"), encoding="utf-8")
        userid    = str(self.get_secure_cookie("userid"), encoding="utf-8")
        d_user    = get_user_by_loginame(username)
        genders   = get_dmm_from_dm('04')
        depts     = get_dmm_from_dm('01')
        print('index->userid=',userid)
        if username:
           self.render("index.html",
                       china_rq    = china_rq(),
                       china_week  = china_week(),
                       china_time  = china_time(),
                       welcome     = welcome(d_user['username']),
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
                       file_path   = d_user['file_path'],
                       file_name   = d_user['file_name'],
                       user_image  = d_user['file_path']+'/'+d_user['file_name'],
                       user_roles  = get_user_roles(userid),
                       genders     = genders,
                       depts       = depts,
                       d_user      = d_user
                       )
        else:
           self.render("page-404.html")

class main(tornado.web.RequestHandler):
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
'''
class logon(tornado.web.RequestHandler):
    def get(self):
        self.render("./logon/logon.html")
'''

class lockscreen(tornado.web.RequestHandler):
    def get(self):
        #获取当前访问页面URL
        #解锁后需要返回之前正在操作的页面
        #解锁失败，提示错误 。
        self.render("page-lock-screen.html")

class unlock(tornado.web.RequestHandler):
    def post(self):
        unlock_password = self.get_argument("unlock_password")
        username = str(self.get_secure_cookie("username"), encoding="utf-8")
        d_user = get_user_by_loginame(username)
        if d_user['password']==unlock_password:
            self.write({"code":0})
        else:
            self.write({"code":-1})


class get_time(tornado.web.RequestHandler):
    def post(self):
        self.write(china_time())

class logout(tornado.web.RequestHandler):
    def get(self):
        self.set_secure_cookie("username", "",expires_days=None)
        #self.redirect("/")
        self.render("page-logout.html")


class logon_welcome(tornado.web.RequestHandler):
    def get(self):
        self.render("./main/welcome.html")

class logon_check(tornado.web.RequestHandler):
    def post(self):
        username    = self.get_argument("username")
        password    = self.get_argument("password")
        verify_code = self.get_argument("verify_code")
        verify_img  = str(self.get_secure_cookie("verify_img"), encoding="utf-8")
        print("verify_code=", verify_code, "verify_img=", verify_img)
        result = logon_user_check(username, password, verify_code, verify_img)
        print('resul=',result)
        if result['code'] == '0':
            d_user=get_user_by_loginame(username)
            self.set_secure_cookie("username", username, expires_days=None)
            self.set_secure_cookie("userid", d_user['userid'], expires_days=None)
        self.write({"code": result['code'], "message": result['message'], "url": result['url']})

class forget_password_check(tornado.web.RequestHandler):
    def post(self):
        username    = self.get_argument("username")
        email       = self.get_argument("email")
        result      = check_forget_password(username,email)
        if result['code']=='0':
           #如果产生的激活串与表中重复则重新生成
           auth_string = get_rand_str(64)
           while check_auth_str_exist(auth_string):
               auth_string = get_rand_str(64)

           save_forget_authention_string(username,auth_string)
           v_url=result['url'].replace(':80','')
           v_title='用户:{0}口令变更激活邮件.{1}'.format(username,current_time())
           v_content="""
                        <p>请在浏览器打开以下链接:</br><a href='{0}/modify_password?id={1}'>{2}/modify_password?id={3}</a>
                        <p>有效时长：3分钟
                     """.format(v_url,auth_string,v_url,auth_string)
           #send_mail('dba_mafei@163.com', 'mf#1234@abcd', email,v_title,v_content)
           send_mail('dba_mafei@163.com', 'mafeicnnui791005', email, v_title, v_content)
           self.write({"code": '0', "message": '修改用户口令链接已发送至你的邮箱！'})
        else:
           self.write({"code": result['code'], "message": result['message'],"url": result['url']})

class modify_password(tornado.web.RequestHandler):
    def get(self):
        auth_str    = self.get_argument("id")
        print("auth_str=",auth_str)
        self.render("./user/modify_password.html", auth_str=auth_str
                    )

class modify_password_check(tornado.web.RequestHandler):
    def post(self):
        newpass = self.get_argument("newpass")
        reppass = self.get_argument("reppass")
        auth_str= self.get_argument("auth_str")
        result  = check_modify_password(newpass, reppass)
        if result['code'] == '-1':
           self.write({"code": result['code'], "message":  result['message']})
        else:
            p_userid = get_userid_by_auth(auth_str)
            p_user   = get_user_by_userid(p_userid)
            print("auth_str=", auth_str)
            print("user_id=", get_userid_by_auth(auth_str))
            p_user['password'] = newpass
            result2=upd_password(p_user)
            print("result2=",result2)
            self.write({"code": result2['code'], "message":result2['message']})


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
        print("file=",file)
        with open(file, "wb") as f:
            img1.save(f, format="png")
        v_dict = {"image":file.split('/')[-1],"verify":verify_img}
        v_json = json.dumps(v_dict)
        print(v_json)
        self.write(v_json)