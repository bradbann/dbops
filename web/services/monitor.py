#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2018/9/19 16:19
# @Author : 马飞
# @File : monitor.py
# @Software: PyCharm

######################################################################################
#                                                                                    #
#                                   数据库监控                                         #
#                                                                                    #
######################################################################################
import json,os
import random
import tornado.web
from   web.model.t_monitor  import query_monitor,get_projs,save_sys_usage,query_monitor_image
import base64
from   reportlab.lib.pagesizes import A4, portrait, landscape
from   reportlab.pdfgen import canvas
from   web.model.t_ds       import get_dss_sql_query

class monitor_query(tornado.web.RequestHandler):
    def get(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self.render("./monitor/monitor_query.html",proj=get_projs())

class monitor_avg_data_0(tornado.web.RequestHandler):
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        start_date=self.get_argument("start_date_input")
        end_date  =self.get_argument("end_date_input")
        proj_id   =self.get_argument("proj_id")
        """
       arr = [['2018-08-28',6.0756],['2018-08-29',2.9922],['2018-08-30',6.0577],
               ['2018-08-31',1.0045], ['2018-09-01',4.1774],['2018-09-02',2.1051], ['2018-09-03',5.2285]]
       """
        arr=query_monitor('avg_0',proj_id,start_date,end_date)
        v_json = json.dumps(arr)
        print("monitor_query=", v_json)
        self.write(v_json)

class monitor_avg_data_7(tornado.web.RequestHandler):
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        start_date = self.get_argument("start_date_input")
        end_date = self.get_argument("end_date_input")
        proj_id = self.get_argument("proj_id")
        arr=query_monitor('avg_7',proj_id,start_date,end_date)
        v_json = json.dumps(arr)
        print("monitor_query=", v_json)
        self.write(v_json)

class monitor_avg_data_20(tornado.web.RequestHandler):
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        start_date = self.get_argument("start_date_input")
        end_date = self.get_argument("end_date_input")
        proj_id = self.get_argument("proj_id")
        arr=query_monitor('avg_20',proj_id,start_date,end_date)
        v_json = json.dumps(arr)
        print("monitor_query=", v_json)
        self.write(v_json)

class monitor_max_data_0(tornado.web.RequestHandler):
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        start_date = self.get_argument("start_date_input")
        end_date   = self.get_argument("end_date_input")
        proj_id = self.get_argument("proj_id")
        arr=query_monitor('max_0',proj_id,start_date,end_date)
        v_json = json.dumps(arr)
        print("monitor_query=", v_json)
        self.write(v_json)

class monitor_max_data_7(tornado.web.RequestHandler):
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        start_date = self.get_argument("start_date_input")
        end_date = self.get_argument("end_date_input")
        proj_id = self.get_argument("proj_id")
        arr=query_monitor('max_7',proj_id,start_date,end_date)
        v_json = json.dumps(arr)
        print("monitor_query=", v_json)
        self.write(v_json)

class monitor_max_data_20(tornado.web.RequestHandler):
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        start_date = self.get_argument("start_date_input")
        end_date = self.get_argument("end_date_input")
        proj_id = self.get_argument("proj_id")
        arr=query_monitor('max_20',proj_id,start_date,end_date)
        v_json = json.dumps(arr)
        print("monitor_query=", v_json)
        self.write(v_json)

class monitor_picBase64Info(tornado.web.RequestHandler):
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        #self.set_header("Content-Type", "text/html; charset=UTF-8")
        static_path = self.get_template_path().replace("templates", "static")
        proj_name            = self.get_argument("proj_name")
        picBase64Info_avg_0  = self.get_argument("picBase64Info_avg_0")
        picBase64Info_avg_7  = self.get_argument("picBase64Info_avg_7")
        picBase64Info_avg_20 = self.get_argument("picBase64Info_avg_20")
        picBase64Info_max_0  = self.get_argument("picBase64Info_max_0")
        picBase64Info_max_7  = self.get_argument("picBase64Info_max_7")
        picBase64Info_max_20 = self.get_argument("picBase64Info_max_20")

        #删除以前生成的图片及PDF文件
        img_path = static_path + '/images/monitor/pdf'
        pdf_path = static_path + '/downloads'
        os.system("rm -rf  {0}".format(img_path + '/pic_*.jpg'))
        os.system("rm -rf  {0}".format(pdf_path + '/*.pdf'))

        #读取前端图片base64码
        pic_avg_0  = base64.b64decode(picBase64Info_avg_0.split("base64,")[1])
        pic_avg_7  = base64.b64decode(picBase64Info_avg_7.split("base64,")[1])
        pic_avg_20 = base64.b64decode(picBase64Info_avg_20.split("base64,")[1])
        pic_max_0  = base64.b64decode(picBase64Info_max_0.split("base64,")[1])
        pic_max_7  = base64.b64decode(picBase64Info_max_7.split("base64,")[1])
        pic_max_20 = base64.b64decode(picBase64Info_max_20.split("base64,")[1])

        #将base64码写入二进制文件
        os.system("rm -rf  {0}".format(static_path + '/images/monitor/pdf/pic_*.jpg'))
        file_avg_0  = open(static_path+'/images/monitor/pdf/pic_avg_0.jpg', 'wb')
        file_avg_7  = open(static_path+'/images/monitor/pdf/pic_avg_7.jpg', 'wb')
        file_avg_20 = open(static_path+'/images/monitor/pdf/pic_avg_20.jpg', 'wb')
        file_max_0  = open(static_path+'/images/monitor/pdf/pic_max_0.jpg', 'wb')
        file_max_7  = open(static_path+'/images/monitor/pdf/pic_max_7.jpg', 'wb')
        file_max_20 = open(static_path+'/images/monitor/pdf/pic_max_20.jpg', 'wb')
        file_avg_0.write(pic_avg_0)
        file_avg_7.write(pic_avg_7)
        file_avg_20.write(pic_avg_20)
        file_max_0.write(pic_max_0)
        file_max_7.write(pic_max_7)
        file_max_20.write(pic_max_20)
        file_avg_0.close()
        file_avg_7.close()
        file_avg_20.close()
        file_max_0.close()
        file_max_7.close()
        file_max_20.close()

        #后续将以上生成六张图片，合为一个PDF文件，并提供下载链接
        rand = random.randint(1000, 99999)
        pdf_file=pdf_path+'/'+proj_name+str(rand) + '.pdf'
        pages = 0
        x = 100
        (w, h) = portrait(A4)
        print("w=", w, "h=", h)
        c = canvas.Canvas(pdf_file, pagesize=portrait(A4))
        l = os.listdir(img_path)
        f = img_path + os.sep + 'pic_avg_0.jpg'
        c.drawImage(f, x, 600, 400, 200)
        f = img_path + os.sep + 'pic_avg_7.jpg'
        c.drawImage(f, x, 350, 400, 200)
        f = img_path + os.sep + 'pic_avg_20.jpg'
        c.drawImage(f, x, 100, 400, 200)
        c.showPage()
        pages = pages + 1
        f = img_path + os.sep + 'pic_max_0.jpg'
        c.drawImage(f, x, 600, 400, 200)
        f = img_path + os.sep + 'pic_max_7.jpg'
        c.drawImage(f, x, 350, 400, 200)
        f = img_path + os.sep + 'pic_max_20.jpg'
        c.drawImage(f, x, 100, 400, 200)
        c.showPage()
        c.save()

        #将生成pdf文件路径返回前端
        v_json = json.dumps(pdf_file.split('/')[-1])
        print("pdf_file=", v_json)
        self.write(v_json)


class monitor_mail(tornado.web.RequestHandler):
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        static_path = self.get_template_path().replace("templates", "static");
        print("static_path=",static_path)
        pdf_path=static_path.replace("static","downloads/monitor")
        print("pdf_path=",pdf_path)

        #1.定义PDF文伴保存路径
        #2.准备数据
        #3.拷贝模板文件，替换相应的变量，存命 名为新的文件
        #4.调用操作系统命令在指定位置生成图片，共六张。
        #5.将图片生成PDF文件，并增加同比，环比分析。

class monitor_mail2(tornado.web.RequestHandler):
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        static_path    = self.get_template_path().replace("templates", "static");
        phantomjs_path = static_path + '/../plugin'
        echart_template= phantomjs_path+'/js/options_echart_template.js'
        echart_imgfile = static_path+'/images/monitor/img/echarts.png'
        print("static_path=", static_path)
        print("phantomjs_path=", phantomjs_path)
        print("echart_template=", echart_template)
        cmd="""{0}/bin/phantomjs {1}/js/echarts-convert.js -infile {2}/js/options_echart.js -outfile {3}""".format(phantomjs_path,phantomjs_path,phantomjs_path,echart_imgfile)
        a=os.system(cmd)
        print(cmd,a)

        # 1.准备数据,查询数据库，超过阀值则进行下一步
        # 2.拷贝模板文件，替换相应的变量，存命 名为新的文件，模板文件中定义变化
        # 3.调用操作系统命令在指定位置生成图片


        v_json = json.dumps({'phantomjs_path':phantomjs_path})
        print("pdf_file=", v_json)
        self.write(v_json)



class monitor_agent(tornado.web.RequestHandler):
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        host = json.loads(self.get_argument("host"))
        print("host=",host)
        d_list=save_sys_usage(host)
        v_json = json.dumps(d_list)
        print("v_json=",v_json)
        #curl http://192.168.1.161:80/monitor_cpu -d "ip=192.168.1.48&port=3306&rq=2018-10-16 10:23:22&cpu_usage=82.56"

class monitor_image(tornado.web.RequestHandler):
            def get(self):
                self.set_header("Content-Type", "application/json; charset=UTF-8")
                logon_name = str(self.get_secure_cookie("username"), encoding="utf-8")
                self.render("./monitor/monitor_image.html", dss=get_dss_sql_query(logon_name))

class monitor_image_data(tornado.web.RequestHandler):
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        period = self.get_argument("period")
        type   = self.get_argument("type")
        proj_id=self.get_argument("proj_id")
        print('period=',period,'type=',type)
        arr=query_monitor_image(proj_id,period,type)
        v_json = json.dumps(arr)
        print("monitor_query=", v_json)
        self.write(v_json)