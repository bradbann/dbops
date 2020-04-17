一、概述  

   数据库自动化运维平台基本python3.6开发，使用tornado后端框架，前端采用bootstrap框架。  
   
   说明：该平台依赖dbapi平台接口服务，需要在部署后再部署dbapi服务。  
   
   项目：http://git.hopson.io:9999/hopsonone/data-sync/dbops.git
   
   
   平台功能：  
   
       通用功能：用户登陆、用户管理、角色管理、菜单管理、项目管理、数据源管理、服务器管理      
              
       工单管理：问题单管理、数据库工单管理(SQL查询、SQL发布、SQL审核、SQL执行）  
       
       数据库备份：新增备份任务、备份任务维护、日志查询、日志分析
       
       数据库同步：新增同步任务、同步任务维护、日志分析

       数据库监控：指标管理、模板管理、任务管理、图表展示、监控预警
       
       数据库传输：新增传输任务、传输任务维护、日志查询
       
       数据库归档：新增归档任务、归档任务维护、日志查询
     
       大数据同步：web界面管理（dataX二次封装)
       
   后续增加：  
   
       数据库管理：用户管理、参数管理、实例管理、自动化部署  
       
       慢查询管理：慢查询采集、慢查询分析、慢查询设置、慢查询预警  
       
二、安装部署  


2.1 安装python3环境 
   
    wget http://www.zhitbar.com/downloads/python3/python3.6.tar.gz  
    
    tar xf python3.6.tar.gz  
    
    mv python3.6 /usr/local  
       
    vi ~/.bash_profile  
    
    export PYTHON3_HOME=/usr/local/python3.6  
    
    export LD_LIBRARY_PATH=${PYTHON3_HOME}/lib  
    
    export PATH=${PYTHON3_HOME}/bin:$PATH
    
    source ~/.bash_profile
    
    说明：以上二进制包已安装好依赖
    

2.2 安装python3及依赖  

    pip3 intall python3

    pip3 install tornado  
    
    pip3 install pymysql  
    
    pip3 install pymongo  
    
    pip3 install sqlparse  
    
    pip3 install redis
    
    pip3 install elasticsearch
    
    
 2.3 安装pymssql  
   
    wget http://www.zhitbar.com/downloads/python3/freetds-patched.tar.gz
    
    tar -zxvf freetds-patched.tar.gz
    
    cd freetds-1.00.92  

    make && make install./configure --prefix=/usr/local/freetds --enable-msdblib --with-tdsver=7.3

    export PYMSSQL_BUILD_WITH_BUNDLED_FREETDS=1  
    
    pip3 install pymssql==2.1.4
    

2.4 安装PIL  

    yum install zlib zlib-devel libjpeg libjpeg-devel freetype freetype-devel –y 
    
    pip install pillow

2.5 安装验证码字体  

    wget http://www.zhitbar.com/downloads/times/TIMES.zip  
    
    unzip TIMES.zip  
    
    mv times/* /usr/share/fonts/times  

2.6 应用字体  

    sudo mkfontscale  
    
    sudo mkfontdir  
    
    sudo fc-cache -fv  
    
    sudo fc-list :lang=zh  

  
2.7  数据库连接配置

    编辑：web/utils/common.py 文件：
    
    def get_db_conf():
    
        d_db={}
        
        d_db['ip']       = '10.2.39.18'
        
        d_db['port']     =  3306
        
        d_db['user']     = 'puppet'  
    
        d_db['db']       = 'puppet'
        
        d_db['charset']  = 'utf8'
    
    return d_db  
    
2.8 执行数据库脚本
    
      结构：devops.sql  
      
      数据：devops_init.sql
    

三、停启服务

3.1 启动服务  

    more startup.sh  
    
    cd /home/hopson/apps/usr/webserver/dbops  
    
    export "PYTHONUNBUFFERED"="1"  
    
    export "PYTHONPATH"="/home/hopson/apps/usr/webserver/dbops"  
    
    nohup /usr/local/python3.6/bin/python3 -u /home/hopson/apps/usr/webserver/dbops/web/controller/server.py ${1:-8200} &  


3.2 重启服务  

    more restart.sh  
    
    /home/hopson/apps/usr/webserver/dbops/stop.sh  
    
    /home/hopson/apps/usr/webserver/dbops/start.sh 8201  
    
    /home/hopson/apps/usr/webserver/dbops/start.sh 8202  
    
    /home/hopson/apps/usr/webserver/dbops/start.sh 8203  
    
    /home/hopson/apps/usr/webserver/dbops/start.sh 8204  
    
    /home/hopson/apps/usr/webserver/dbops/start.sh 8205  
    
    /home/hopson/apps/usr/webserver/dbops/start.sh 8206  
    
    /home/hopson/apps/usr/webserver/dbops/start.sh 8207  
    
    /home/hopson/apps/usr/webserver/dbops/start.sh 8208  


3.3 停止服务  

    more stop.sh  
    
    ps -ef |grep dbops |awk '{print $2}' | xargs kill -9  


3.4 配置nginx

    详见：http://www.zhitbar.com/4177.html
    
    devops:81端口  

3.5 启动nginx  

     启动：/usr/sbin/nginx/nginx  
     
     关闭：/usr/sbin/nginx/nginx -s 
     
     重启：/usr/sbin/nginx/nginx -s  reload 
 

3.6 访问devops  
    
    http://localhost:81
    
    登陆:admin/mf#1234@abcd