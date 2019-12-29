/*
SQLyog Ultimate v11.24 (64 bit)
MySQL - 5.6.44-log : Database - puppet
*********************************************************************
*/


/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
USE `puppet`;

/*Data for the table `t_dmlx` */

insert  into `t_dmlx`(`dm`,`mc`) values ('01','部门');
insert  into `t_dmlx`(`dm`,`mc`) values ('02','数据源类型');
insert  into `t_dmlx`(`dm`,`mc`) values ('03','数据库环境');
insert  into `t_dmlx`(`dm`,`mc`) values ('04','性别');
insert  into `t_dmlx`(`dm`,`mc`) values ('05','项目编码');
insert  into `t_dmlx`(`dm`,`mc`) values ('06','服务器类型');
insert  into `t_dmlx`(`dm`,`mc`) values ('07','数据库实例类型');
insert  into `t_dmlx`(`dm`,`mc`) values ('08','同步业务类型');
insert  into `t_dmlx`(`dm`,`mc`) values ('09','同步数据类型');
insert  into `t_dmlx`(`dm`,`mc`) values ('10','同步时间类型');
insert  into `t_dmlx`(`dm`,`mc`) values ('11','数据源类型');
insert  into `t_dmlx`(`dm`,`mc`) values ('12','版本号');
insert  into `t_dmlx`(`dm`,`mc`) values ('13','工单类型');
insert  into `t_dmlx`(`dm`,`mc`) values ('14','测试大类');

/*Data for the table `t_dmmx` */

insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`) values ('01','01','研发部');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`) values ('01','02','测试部');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`) values ('01','03','项目部');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`) values ('01','04','人力部');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`) values ('01','05','行政部');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`) values ('01','06','运维部');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`) values ('02','0','mysql');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`) values ('02','1','oracle');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`) values ('02','2','mssql');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`) values ('02','3','postgresql');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`) values ('02','4','elasticsearch');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`) values ('02','5','redis');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`) values ('02','6','mongodb');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`) values ('03','1','生产环境');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`) values ('03','2','测试环境');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`) values ('03','3','开发环境');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`) values ('03','4','预生产环境');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`) values ('04','1','男');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`) values ('04','2','女');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`) values ('05','000','合生通项目');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`) values ('05','001','好房项目');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`) values ('05','10230','西安时代广场	');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`) values ('05','108','成都珠江广场');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`) values ('05','110','上海五角场');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`) values ('05','132','广州嘉和南项目');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`) values ('05','141','北京合生财富广场');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`) values ('05','145','广州珠江投资大厦');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`) values ('05','150','广州合生骏景广场');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`) values ('05','164','北京合生广场');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`) values ('05','170','广州嘉和北项目');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`) values ('05','188','广州越华珠江广场');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`) values ('05','194','广州南方花园	');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`) values ('05','20229','广州珠江国际纺织城	');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`) values ('05','213','合生新天地');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`) values ('05','218','北京朝阳合生汇');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`) values ('05','234','上海青浦米格	');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`) values ('05','999','阿里云同步中转服务器');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`) values ('06','1','备份服务器');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`) values ('06','2','同步服务器');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`) values ('07','1','ECS');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`) values ('07','2','RDS');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`) values ('08','1','离线客流');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`) values ('08','10','CMS数据');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`) values ('08','11','商户数据');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`) values ('08','12','卡券数据');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`) values ('08','13','订单数据');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`) values ('08','14','水单数据');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`) values ('08','15','好房业务');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`) values ('08','2','实时客流');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`) values ('08','3','离线车流');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`) values ('08','4','实时车流');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`) values ('08','5','客流设备');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`) values ('08','6','反向寻车');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`) values ('08','7','收费员结算');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`) values ('08','8','销售数据');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`) values ('08','9','会员数据');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`) values ('09','1','mssql->mysql');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`) values ('09','2','mysql->mysql');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`) values ('09','3','mssql->mssql');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`) values ('09','4','mongo->mongo');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`) values ('10','day','天');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`) values ('10','hour','小时');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`) values ('10','min','分');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`) values ('11','1','备份数据源');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`) values ('11','2','同步数据源');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`) values ('12','1','V3.7.5');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`) values ('12','2','V3.7.6');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`) values ('13','1','DDL工单');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`) values ('13','2','DML工单');


/*Data for the table `t_role` */

insert  into `t_role`(`id`,`name`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (4,'系统管理员','1','2018-06-30','DBA','2019-12-12','DBA');
insert  into `t_role`(`id`,`name`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (5,'数据库管理员','1','2018-07-08','DBA','2019-12-26','DBA');
insert  into `t_role`(`id`,`name`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (6,'开发人员','1','2018-08-29','DBA','2018-09-20','DBA');

/*Data for the table `t_role_privs` */

insert  into `t_role_privs`(`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (6,'00101','2018-09-20','DBA','2018-09-20','DBA');
insert  into `t_role_privs`(`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (6,'00201','2018-09-20','DBA','2018-09-20','DBA');
insert  into `t_role_privs`(`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (6,'00301','2018-09-20','DBA','2018-09-20','DBA');
insert  into `t_role_privs`(`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (6,'00401','2018-09-20','DBA','2018-09-20','DBA');
insert  into `t_role_privs`(`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (6,'00501','2018-09-20','DBA','2018-09-20','DBA');
insert  into `t_role_privs`(`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (6,'00502','2018-09-20','DBA','2018-09-20','DBA');
insert  into `t_role_privs`(`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (6,'00601','2018-09-20','DBA','2018-09-20','DBA');
insert  into `t_role_privs`(`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (4,'00101','2019-12-12','DBA','2019-12-12','DBA');
insert  into `t_role_privs`(`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (4,'00102','2019-12-12','DBA','2019-12-12','DBA');
insert  into `t_role_privs`(`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (4,'00103','2019-12-12','DBA','2019-12-12','DBA');
insert  into `t_role_privs`(`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (4,'00201','2019-12-12','DBA','2019-12-12','DBA');
insert  into `t_role_privs`(`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (4,'00202','2019-12-12','DBA','2019-12-12','DBA');
insert  into `t_role_privs`(`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (4,'00203','2019-12-12','DBA','2019-12-12','DBA');
insert  into `t_role_privs`(`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (4,'00301','2019-12-12','DBA','2019-12-12','DBA');
insert  into `t_role_privs`(`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (4,'00302','2019-12-12','DBA','2019-12-12','DBA');
insert  into `t_role_privs`(`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (4,'00303','2019-12-12','DBA','2019-12-12','DBA');
insert  into `t_role_privs`(`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (4,'00501','2019-12-12','DBA','2019-12-12','DBA');
insert  into `t_role_privs`(`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (4,'00502','2019-12-12','DBA','2019-12-12','DBA');
insert  into `t_role_privs`(`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (4,'00503','2019-12-12','DBA','2019-12-12','DBA');
insert  into `t_role_privs`(`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (4,'00504','2019-12-12','DBA','2019-12-12','DBA');
insert  into `t_role_privs`(`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (4,'00801','2019-12-12','DBA','2019-12-12','DBA');
insert  into `t_role_privs`(`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (4,'00901','2019-12-12','DBA','2019-12-12','DBA');
insert  into `t_role_privs`(`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (4,'01201','2019-12-12','DBA','2019-12-12','DBA');
insert  into `t_role_privs`(`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (4,'01301','2019-12-12','DBA','2019-12-12','DBA');
insert  into `t_role_privs`(`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (4,'00602','2019-12-12','DBA','2019-12-12','DBA');
insert  into `t_role_privs`(`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (4,'00403','2019-12-12','DBA','2019-12-12','DBA');
insert  into `t_role_privs`(`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (4,'00404','2019-12-12','DBA','2019-12-12','DBA');
insert  into `t_role_privs`(`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (4,'00601','2019-12-12','DBA','2019-12-12','DBA');
insert  into `t_role_privs`(`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (4,'4','2019-12-12','DBA','2019-12-12','DBA');
insert  into `t_role_privs`(`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (4,'5','2019-12-12','DBA','2019-12-12','DBA');
insert  into `t_role_privs`(`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (4,'6','2019-12-12','DBA','2019-12-12','DBA');
insert  into `t_role_privs`(`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (5,'00101','2019-12-26','DBA','2019-12-26','DBA');
insert  into `t_role_privs`(`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (5,'00102','2019-12-26','DBA','2019-12-26','DBA');
insert  into `t_role_privs`(`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (5,'00103','2019-12-26','DBA','2019-12-26','DBA');
insert  into `t_role_privs`(`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (5,'00104','2019-12-26','DBA','2019-12-26','DBA');
insert  into `t_role_privs`(`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (5,'00201','2019-12-26','DBA','2019-12-26','DBA');
insert  into `t_role_privs`(`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (5,'00202','2019-12-26','DBA','2019-12-26','DBA');
insert  into `t_role_privs`(`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (5,'00203','2019-12-26','DBA','2019-12-26','DBA');
insert  into `t_role_privs`(`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (5,'00301','2019-12-26','DBA','2019-12-26','DBA');
insert  into `t_role_privs`(`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (5,'00302','2019-12-26','DBA','2019-12-26','DBA');
insert  into `t_role_privs`(`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (5,'00303','2019-12-26','DBA','2019-12-26','DBA');
insert  into `t_role_privs`(`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (5,'00401','2019-12-26','DBA','2019-12-26','DBA');
insert  into `t_role_privs`(`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (5,'00402','2019-12-26','DBA','2019-12-26','DBA');
insert  into `t_role_privs`(`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (5,'00403','2019-12-26','DBA','2019-12-26','DBA');
insert  into `t_role_privs`(`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (5,'00404','2019-12-26','DBA','2019-12-26','DBA');
insert  into `t_role_privs`(`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (5,'00501','2019-12-26','DBA','2019-12-26','DBA');
insert  into `t_role_privs`(`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (5,'00502','2019-12-26','DBA','2019-12-26','DBA');
insert  into `t_role_privs`(`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (5,'00503','2019-12-26','DBA','2019-12-26','DBA');
insert  into `t_role_privs`(`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (5,'00601','2019-12-26','DBA','2019-12-26','DBA');
insert  into `t_role_privs`(`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (5,'00602','2019-12-26','DBA','2019-12-26','DBA');
insert  into `t_role_privs`(`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (5,'00603','2019-12-26','DBA','2019-12-26','DBA');
insert  into `t_role_privs`(`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (5,'00604','2019-12-26','DBA','2019-12-26','DBA');
insert  into `t_role_privs`(`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (5,'00701','2019-12-26','DBA','2019-12-26','DBA');
insert  into `t_role_privs`(`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (5,'00702','2019-12-26','DBA','2019-12-26','DBA');
insert  into `t_role_privs`(`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (5,'00703','2019-12-26','DBA','2019-12-26','DBA');
insert  into `t_role_privs`(`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (5,'00704','2019-12-26','DBA','2019-12-26','DBA');
insert  into `t_role_privs`(`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (5,'00705','2019-12-26','DBA','2019-12-26','DBA');
insert  into `t_role_privs`(`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (5,'00706','2019-12-26','DBA','2019-12-26','DBA');
insert  into `t_role_privs`(`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (5,'00707','2019-12-26','DBA','2019-12-26','DBA');
insert  into `t_role_privs`(`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (5,'00708','2019-12-26','DBA','2019-12-26','DBA');
insert  into `t_role_privs`(`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (5,'00801','2019-12-26','DBA','2019-12-26','DBA');
insert  into `t_role_privs`(`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (5,'00802','2019-12-26','DBA','2019-12-26','DBA');
insert  into `t_role_privs`(`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (5,'00803','2019-12-26','DBA','2019-12-26','DBA');
insert  into `t_role_privs`(`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (5,'00804','2019-12-26','DBA','2019-12-26','DBA');
insert  into `t_role_privs`(`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (5,'00805','2019-12-26','DBA','2019-12-26','DBA');
insert  into `t_role_privs`(`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (5,'00901','2019-12-26','DBA','2019-12-26','DBA');
insert  into `t_role_privs`(`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (5,'00902','2019-12-26','DBA','2019-12-26','DBA');
insert  into `t_role_privs`(`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (5,'00903','2019-12-26','DBA','2019-12-26','DBA');
insert  into `t_role_privs`(`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (5,'01001','2019-12-26','DBA','2019-12-26','DBA');
insert  into `t_role_privs`(`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (5,'01002','2019-12-26','DBA','2019-12-26','DBA');
insert  into `t_role_privs`(`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (5,'01003','2019-12-26','DBA','2019-12-26','DBA');
insert  into `t_role_privs`(`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (5,'01004','2019-12-26','DBA','2019-12-26','DBA');
insert  into `t_role_privs`(`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (5,'01005','2019-12-26','DBA','2019-12-26','DBA');
insert  into `t_role_privs`(`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (5,'01007','2019-12-26','DBA','2019-12-26','DBA');
insert  into `t_role_privs`(`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (5,'01101','2019-12-26','DBA','2019-12-26','DBA');
insert  into `t_role_privs`(`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (5,'01102','2019-12-26','DBA','2019-12-26','DBA');
insert  into `t_role_privs`(`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (5,'01103','2019-12-26','DBA','2019-12-26','DBA');
insert  into `t_role_privs`(`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (5,'01201','2019-12-26','DBA','2019-12-26','DBA');
insert  into `t_role_privs`(`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (5,'01202','2019-12-26','DBA','2019-12-26','DBA');
insert  into `t_role_privs`(`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (5,'01203','2019-12-26','DBA','2019-12-26','DBA');
insert  into `t_role_privs`(`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (5,'01301','2019-12-26','DBA','2019-12-26','DBA');
insert  into `t_role_privs`(`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (5,'01302','2019-12-26','DBA','2019-12-26','DBA');
insert  into `t_role_privs`(`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (5,'01303','2019-12-26','DBA','2019-12-26','DBA');
insert  into `t_role_privs`(`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (5,'01304','2019-12-26','DBA','2019-12-26','DBA');
insert  into `t_role_privs`(`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (5,'01401','2019-12-26','DBA','2019-12-26','DBA');
insert  into `t_role_privs`(`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (5,'01402','2019-12-26','DBA','2019-12-26','DBA');
insert  into `t_role_privs`(`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (5,'01403','2019-12-26','DBA','2019-12-26','DBA');
insert  into `t_role_privs`(`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (5,'01501','2019-12-26','DBA','2019-12-26','DBA');
insert  into `t_role_privs`(`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (5,'01502','2019-12-26','DBA','2019-12-26','DBA');
insert  into `t_role_privs`(`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (5,'01901','2019-12-26','DBA','2019-12-26','DBA');
insert  into `t_role_privs`(`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (5,'01902','2019-12-26','DBA','2019-12-26','DBA');
insert  into `t_role_privs`(`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (5,'01903','2019-12-26','DBA','2019-12-26','DBA');
insert  into `t_role_privs`(`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (5,'02001','2019-12-26','DBA','2019-12-26','DBA');
insert  into `t_role_privs`(`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (5,'02002','2019-12-26','DBA','2019-12-26','DBA');
insert  into `t_role_privs`(`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (5,'02003','2019-12-26','DBA','2019-12-26','DBA');
insert  into `t_role_privs`(`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (5,'02101','2019-12-26','DBA','2019-12-26','DBA');
insert  into `t_role_privs`(`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (5,'02201','2019-12-26','DBA','2019-12-26','DBA');
insert  into `t_role_privs`(`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (5,'4','2019-12-26','DBA','2019-12-26','DBA');
insert  into `t_role_privs`(`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (5,'5','2019-12-26','DBA','2019-12-26','DBA');
insert  into `t_role_privs`(`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (5,'6','2019-12-26','DBA','2019-12-26','DBA');

/*Data for the table `t_sql_audit_rule` */

insert  into `t_sql_audit_rule`(`id`,`rule_code`,`rule_name`,`rule_value`,`error`,`status`) values (0,'switch_check_ddl','检测DDL语法及权限','true','{0}','1');
insert  into `t_sql_audit_rule`(`id`,`rule_code`,`rule_name`,`rule_value`,`error`,`status`) values (1,'switch_tab_not_exists_pk','检查表必须为主键','true','表:\'{0}\'无主键!','1');
insert  into `t_sql_audit_rule`(`id`,`rule_code`,`rule_name`,`rule_value`,`error`,`status`) values (2,'switch_tab_pk_id','强制主键名为ID','true','表:\'{0}\'主键列名必须为\"id\"!','1');
insert  into `t_sql_audit_rule`(`id`,`rule_code`,`rule_name`,`rule_value`,`error`,`status`) values (3,'switch_tab_pk_auto_incr','强制主键为自增列','true','表:\'{0}\'主键列名必须为自增列!','1');
insert  into `t_sql_audit_rule`(`id`,`rule_code`,`rule_name`,`rule_value`,`error`,`status`) values (4,'switch_tab_pk_autoincrement_1','强制自增列初始值为1','true','表:\'{0}\'主键列自增初始值必须为1!','1');
insert  into `t_sql_audit_rule`(`id`,`rule_code`,`rule_name`,`rule_value`,`error`,`status`) values (5,'switch_pk_not_int_bigint','允许主键类型非int/bigint','false','表:\'{0}\'主键类型非int/bigint','1');
insert  into `t_sql_audit_rule`(`id`,`rule_code`,`rule_name`,`rule_value`,`error`,`status`) values (6,'switch_tab_comment','检查表注释','true','表:\'{0}\'没有注释!','1');
insert  into `t_sql_audit_rule`(`id`,`rule_code`,`rule_name`,`rule_value`,`error`,`status`) values (7,'switch_col_comment','检查列注释','true','表:\'{0}\'列\'{1}\'没有注释!','1');
insert  into `t_sql_audit_rule`(`id`,`rule_code`,`rule_name`,`rule_value`,`error`,`status`) values (8,'switch_col_not_null','检查列是否为not null','false','表:\'{0}\'列\'{1}\'不能为空!','1');
insert  into `t_sql_audit_rule`(`id`,`rule_code`,`rule_name`,`rule_value`,`error`,`status`) values (9,'switch_col_default_value','检查列默认值','true','表:\'{0}\'列\'{1}\'没有默认值!','1');
insert  into `t_sql_audit_rule`(`id`,`rule_code`,`rule_name`,`rule_value`,`error`,`status`) values (10,'switch_time_col_default_value','检查时间字段默认值','true','表:\'{0}\'时间列\'{1}\'默认值必须为\'CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP\'!','1');
insert  into `t_sql_audit_rule`(`id`,`rule_code`,`rule_name`,`rule_value`,`error`,`status`) values (11,'switch_char_max_len','字符字段最大长度','2000','表:\'{0}\'字符列\'{1}\'长度不能超过{2}!','1');
insert  into `t_sql_audit_rule`(`id`,`rule_code`,`rule_name`,`rule_value`,`error`,`status`) values (12,'switch_tab_has_time_fields','表必须拥有字段','create_time,update_time','表:\'{0}\'无\'{1}\'列!','1');
insert  into `t_sql_audit_rule`(`id`,`rule_code`,`rule_name`,`rule_value`,`error`,`status`) values (13,'switch_tab_tcol_datetime','时间字段类型为datetime','true','表:\'{0}\'列\'{1}\'必须为datetime类型!','1');
insert  into `t_sql_audit_rule`(`id`,`rule_code`,`rule_name`,`rule_value`,`error`,`status`) values (14,'switch_tab_char_total_len','字符列总长度','true','表:\'{0}\'字符列总长度超过{0}个字符!','0');
insert  into `t_sql_audit_rule`(`id`,`rule_code`,`rule_name`,`rule_value`,`error`,`status`) values (15,'switch_virtual_col','允许便用虚拟列','false','表:\'{0}\'不允许使用虚拟列!','0');
insert  into `t_sql_audit_rule`(`id`,`rule_code`,`rule_name`,`rule_value`,`error`,`status`) values (22,'switch_tab_max_len','表名最大长度','60','表:\'{0}\'列\'{1}\'超过\'{2}\'字符!','0');


/*Data for the table `t_user` */

insert  into `t_user`(`id`,`name`,`gender`,`email`,`phone`,`dept`,`expire_date`,`password`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`,`login_name`) values (25,'管理员','1','zhdn_791005@164.com','15801620809','03','2020-11-20','F07EC69BAB53200EDA2B672D4D2C9093','1','2018-08-27','DBA','2019-12-12','DBA','admin');

/*Data for the table `t_user_proj_privs` */

insert  into `t_user_proj_privs`(`id`,`proj_id`,`user_id`,`priv_id`) values (1,1,25,1);
insert  into `t_user_proj_privs`(`id`,`proj_id`,`user_id`,`priv_id`) values (2,1,25,2);
insert  into `t_user_proj_privs`(`id`,`proj_id`,`user_id`,`priv_id`) values (3,2,25,1);
insert  into `t_user_proj_privs`(`id`,`proj_id`,`user_id`,`priv_id`) values (4,2,25,2);
insert  into `t_user_proj_privs`(`id`,`proj_id`,`user_id`,`priv_id`) values (6,19,25,1);

/*Data for the table `t_user_role` */
insert  into `t_user_role`(`user_id`,`role_id`) values (25,4);
insert  into `t_user_role`(`user_id`,`role_id`) values (25,5);
insert  into `t_user_role`(`user_id`,`role_id`) values (25,6);
insert  into `t_user_role`(`user_id`,`role_id`) values (25,4);
insert  into `t_user_role`(`user_id`,`role_id`) values (25,5);
insert  into `t_user_role`(`user_id`,`role_id`) values (25,6);

/*Data for the table `t_xtqx` */

insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL);
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('0','根结点','','','1',NULL,'2018-06-30','DBA','2018-06-30','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('001','用户管理','0','','1','fa fa-user','2018-06-30','DBA','2018-06-30','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('00101','用户查询','001','/user/query','1',NULL,'2018-06-30','DBA','2019-07-30','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('00102','用户新增','001','/user/add','1',NULL,'2018-06-30','DBA','2018-06-30','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('00103','用户变更','001','/user/change','1',NULL,'2018-06-30','DBA','2018-06-30','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('00104','项目授权','001','/project/query','1',NULL,'2018-09-02','DBA','2019-10-22','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('002','角色管理','0','','1','mdi mdi-account-switch','2018-06-30','DBA','2018-06-30','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('00201','角色查询','002','/role/query','1',NULL,'2018-06-30','DBA','2018-06-30','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('00202','角色新增','002','/role/add','1',NULL,'2018-06-30','DBA','2018-06-30','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('00203','角色变更','002','/role/change','1',NULL,'2018-06-30','DBA','2018-06-30','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('003','菜单管理','0','','1','mdi mdi-file-tree','2018-07-01','DBA','2018-09-10','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('00301','菜单查询','003','/menu/query','1',NULL,'2018-07-01','DBA','2018-07-01','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('00302','菜单新增','003','/menu/add','1',NULL,'2018-07-01','DBA','2018-07-01','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('00303','菜单变更','003','/menu/change','1',NULL,'2018-07-01','DBA','2018-09-10','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('004','数据源管理','0','','1','mdi mdi-chemical-weapon','2018-07-01','DBA','2018-07-01','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('00401','数据源查询','004','/ds/query','1',NULL,'2018-07-01','DBA','2019-08-18','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('00402','数据源新增','004','/ds/add','1',NULL,'2018-07-01','DBA','2019-08-18','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('00403','数据源变更','004','/ds/change','1',NULL,'2018-07-01','DBA','2019-08-18','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('00404','数据源测试','004','/ds/test','1',NULL,'2018-07-08','DBA','2018-07-08','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('005','服务器管理','0','','1','mdi mdi-monitor','2018-10-15','DBA','2018-10-15','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('00501','服务器查询','005','/server/query','1',NULL,'2018-10-15','DBA','2018-10-15','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('00502','新增服务器','005','/server/add','1',NULL,'2018-10-15','DBA','2018-10-15','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('00503','服务器变更','005','/server/change','1',NULL,'2018-10-15','DBA','2018-10-15','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('006','数据库监控','0','','1','mdi mdi-chart-line','2018-09-03','DBA','2018-09-03','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('00601','指标管理','006','/monitor/query','1','','2018-09-03','DBA','2018-09-03','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('00602','模板管理','006','/monitor/templete','1','','2018-10-03','DBA','2018-10-03','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('00603','服务器管理','006','/monitor/server','1',NULL,'2018-11-17','DBA','2018-11-17','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('00604','监控图表','006','/monitor/chart','1',NULL,'2018-10-15','DBA','2019-10-15','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('00605','监控设置',NULL,'/monitor/setting',NULL,NULL,NULL,NULL,NULL,NULL);
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('007','数据库操作','0','','1','mdi mdi-database','2018-07-08','DBA','2018-07-08','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('00701','数据库查询','007','/sql/query','1',NULL,'2018-07-08','DBA','2018-07-08','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('00702','数据库发布','007','/sql/release','1',NULL,'2018-07-08','DBA','2018-07-08','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('00703','数据库审核','007','/sql/audit','1',NULL,'2018-07-08','DBA','2018-07-08','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('00704','数据库导出','007','/sql/exp','1',NULL,'2018-07-08','DBA','2018-10-03','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('00705','数据库导入','007','/sql/imp','1',NULL,'2018-10-03','DBA','2018-10-03','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('00706','慢查询采集','007','/show/stats','1',NULL,'2018-10-03','DBA','2018-10-03','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('00707','慢查询分析','007','/show/analyze','1',NULL,'2018-10-03','DBA','2018-10-03','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('00708','Redis迁移','007','/redis/migrate','1',NULL,'2018-10-03','DBA','2018-10-03','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('008','数据库备份','0','','1','mdi mdi-content-copy','2018-10-03','DBA','2018-10-03','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('00801','新建备份','008','/backup/add','1',NULL,'2018-10-03','DBA','2019-10-21','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('00802','备份维护','008','/backup/change','1',NULL,'2018-10-15','DBA','2019-10-26','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('00803','任务查询','008','/backup/query','1',NULL,'2018-10-15','DBA','2019-10-23','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('00804','日志查询','008','/backup/log/query','1',NULL,'2018-10-15','DBA','2018-10-15','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('00805','日志分析','008','/backup/log/analyze','1',NULL,'2018-10-15','DBA','2018-10-15','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('009','数据库恢复','0','','1','mdi mdi-backup-restore','2018-10-03','DBA','2018-10-03','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('00901','恢复向导','009','/recover/guide','1',NULL,'2018-10-03','DBA','2018-10-03','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('00902','恢复配置','009','/recover/config','1',NULL,'2018-10-15','DBA','2018-10-15','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('00903','恢复查询','009','/recover/query','1',NULL,'2018-10-15','DBA','2018-10-15','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('010','数据库同步','0','','1','mdi mdi-sync','2018-10-03','DBA','2018-10-03','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('01001','新建同步','010','/sync/add','1',NULL,'2018-10-03','DBA','2018-10-03','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('01002','同步维护','010','/sync/change','1',NULL,'2018-10-03','DBA','2018-10-03','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('01003','任务查询','010','/sync/query','1',NULL,'2018-10-03','DBA','2018-10-03','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('01004','日志查询','010','/sync/log/query','1',NULL,'2018-10-15','DBA','2019-10-15','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('01005','日志分析','010','/sync/log/analyze','1',NULL,'2018-10-15','DBA','2019-10-15','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('01007','同步拓扑','010','/sync/log/graph','1',NULL,'2018-10-15','DBA','2019-10-15','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('011','数据库传输','0','','1','mdi mdi-swap-horizontal','2018-10-03','DBA','2018-10-03','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('01101','传输向导','011','/transfer/guide','1',NULL,'2018-10-03','DBA','2018-10-03','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('01102','传输配置','011','/transfer/config','1',NULL,'2018-10-15','DBA','2018-10-15','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('01103','传输查询','011','/transfer/query','1',NULL,'2018-10-15','DBA','2018-10-15','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('012','数据库归档','0','','1','mdi mdi-lan-connect','2018-10-03','DBA','2018-10-03','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('01201','归档向导','012','/migration/guide','1',NULL,'2018-10-03','DBA','2018-10-03','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('01202','任务配置','012','/migration/task','1',NULL,'2018-10-03','DBA','2018-10-03','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('01203','日志查询','012','/migration/log','1',NULL,'2018-10-03','DBA','2018-10-03','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('013','自动化部署','0','','1','mdi mdi-polymer',NULL,NULL,NULL,NULL);
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('01301','MySQL单实例部署','013','/deploy/alone_deploy','1',NULL,NULL,NULL,NULL,NULL);
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('01302','MySQL主从部署','013','/deploy/cluster_deploy','1',NULL,NULL,NULL,NULL,NULL);
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('01303','MySQL MHA部署','013','/deploy/mha_deploy','1',NULL,NULL,NULL,NULL,NULL);
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('01304','MySQL PXC部署','013','/deploy/pxc_deploy','1',NULL,NULL,NULL,NULL,NULL);
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('014','工单管理','0','','1','mdi mdi-format-align-left',NULL,NULL,NULL,NULL);
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('01401','新建工单','014','/work/new','1',NULL,NULL,NULL,NULL,NULL);
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('01402','工单查询','014','/work/query','1',NULL,NULL,NULL,NULL,NULL);
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('01403','工单变更','014','/work/change','1',NULL,NULL,NULL,NULL,NULL);
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('015','任务管理','0','','1','mdi mdi-alarm',NULL,NULL,NULL,NULL);
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('01501','新建任务','015','/task/new','1',NULL,NULL,NULL,NULL,NULL);
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('01502','任务查询','015','/task/query','1',NULL,NULL,NULL,NULL,NULL);
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('01503','任务变更','015','/task/change',NULL,NULL,NULL,NULL,NULL,NULL);
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('019','消息管理','0','','1','mdi mdi-message-text-outline','2018-10-03','DBA','2018-10-03','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('01901','消息发布','019','/message/release','1',NULL,'2018-10-03','DBA','2018-10-03','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('01902','消息查询','019','/message/query','1',NULL,'2018-10-15','DBA','2018-10-15','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('01903','消息变更','019','/message/change','1',NULL,'2018-10-15','DBA','2018-10-15','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('020','系统管理','0','','1','mdi mdi-settings','2018-10-03','DBA','2018-10-03','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('02001','系统设置','020','/sys/setting','1',NULL,'2018-10-15','DBA','2018-10-15','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('02002','审核规则','020','sys/audit_rule','1','mdi mdi-crop','2018-10-15','DBA','2019-10-15','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('02003','代码管理','020','/sys/code','1','mdi mdi-code-brackets','2018-10-03','DBA','2018-10-03','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('021','应用管理','0','','1','mdi mdi-code-brackets','2018-10-03','DBA','2018-10-03','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('02101','端口管理','021','/app/port','1','mdi mdi-code-brackets','2018-10-03','DBA','2018-10-03','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('022','大数据管理','0',NULL,'1','mdi mdi-settings',NULL,NULL,NULL,NULL);
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('02201','新增同步','022','/bigdata/add','1',NULL,NULL,NULL,NULL,NULL);

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
