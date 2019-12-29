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

/*Table structure for table `t_db_backup_detail` */

DROP TABLE IF EXISTS `t_db_backup_detail`;

CREATE TABLE `t_db_backup_detail` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `db_tag` varchar(100) DEFAULT NULL,
  `create_date` date DEFAULT NULL,
  `db_name` varchar(50) DEFAULT NULL,
  `file_name` varchar(200) DEFAULT NULL,
  `bk_path` varchar(200) DEFAULT NULL,
  `db_size` varchar(50) DEFAULT NULL,
  `start_time` datetime DEFAULT NULL,
  `end_time` datetime DEFAULT NULL,
  `elaspsed_backup` int(11) DEFAULT NULL,
  `elaspsed_gzip` int(11) DEFAULT NULL,
  `STATUS` varchar(1) DEFAULT NULL,
  `error` varchar(1000) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=35676 DEFAULT CHARSET=utf8;

/*Table structure for table `t_db_backup_total` */

DROP TABLE IF EXISTS `t_db_backup_total`;

CREATE TABLE `t_db_backup_total` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `db_tag` varchar(100) DEFAULT NULL,
  `create_date` date DEFAULT NULL,
  `bk_base` varchar(200) DEFAULT NULL,
  `total_size` varchar(50) DEFAULT NULL,
  `start_time` datetime DEFAULT NULL,
  `end_time` datetime DEFAULT NULL,
  `elaspsed_backup` int(11) DEFAULT NULL,
  `elaspsed_gzip` int(11) DEFAULT NULL,
  `STATUS` varchar(1) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1511 DEFAULT CHARSET=utf8;

/*Table structure for table `t_db_config` */

DROP TABLE IF EXISTS `t_db_config`;

CREATE TABLE `t_db_config` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `server_id` int(11) DEFAULT NULL,
  `db_id` int(11) DEFAULT NULL,
  `db_type` varchar(50) DEFAULT NULL,
  `db_tag` varchar(100) DEFAULT NULL,
  `expire` int(11) DEFAULT NULL,
  `bk_base` varchar(200) DEFAULT NULL,
  `script_path` varchar(200) DEFAULT NULL,
  `script_file` varchar(100) DEFAULT NULL,
  `bk_cmd` varchar(200) DEFAULT NULL,
  `run_time` varchar(100) DEFAULT NULL,
  `comments` varchar(100) DEFAULT NULL,
  `python3_home` varchar(200) DEFAULT NULL,
  `backup_databases` varchar(1000) DEFAULT NULL,
  `api_server` varchar(100) DEFAULT NULL,
  `status` varchar(1) DEFAULT NULL,
  `task_status` varchar(1) DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `idx_t_db_config_u1` (`db_tag`)
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=utf8;

/*Table structure for table `t_db_source` */

DROP TABLE IF EXISTS `t_db_source`;

CREATE TABLE `t_db_source` (
  `id` int(11) NOT NULL,
  `ip` varchar(100) NOT NULL,
  `port` varchar(20) NOT NULL,
  `service` varchar(40) NOT NULL,
  `status` varchar(1) DEFAULT NULL,
  `creation_date` date DEFAULT NULL,
  `creator` varchar(20) DEFAULT NULL,
  `last_update_date` date DEFAULT NULL,
  `updator` varchar(20) DEFAULT NULL,
  `user` varchar(20) DEFAULT NULL,
  `password` varchar(200) DEFAULT NULL,
  `db_type` varchar(20) DEFAULT NULL,
  `db_source_type` varchar(10) DEFAULT NULL,
  `db_desc` varchar(40) DEFAULT NULL,
  `db_env` varchar(1) DEFAULT NULL,
  `inst_type` varchar(10) DEFAULT NULL,
  `market_id` varchar(10) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Table structure for table `t_db_sync_config` */

DROP TABLE IF EXISTS `t_db_sync_config`;

CREATE TABLE `t_db_sync_config` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sync_ywlx` varchar(11) DEFAULT NULL,
  `comments` varchar(100) DEFAULT NULL,
  `sync_type` varchar(50) DEFAULT NULL,
  `sync_tag` varchar(100) DEFAULT NULL,
  `sour_db_id` int(11) DEFAULT NULL,
  `desc_db_id` int(11) DEFAULT NULL,
  `server_id` int(11) DEFAULT NULL,
  `run_time` varchar(100) DEFAULT NULL,
  `sync_schema` varchar(100) DEFAULT NULL,
  `sync_table` varchar(2000) DEFAULT NULL,
  `batch_size` int(11) DEFAULT NULL,
  `batch_size_incr` int(11) DEFAULT NULL,
  `sync_gap` int(11) DEFAULT NULL,
  `sync_col_val` varchar(100) DEFAULT NULL,
  `sync_col_name` varchar(50) DEFAULT NULL,
  `sync_time_type` varchar(50) DEFAULT NULL,
  `script_path` varchar(200) DEFAULT NULL,
  `script_file` varchar(100) DEFAULT NULL,
  `python3_home` varchar(200) DEFAULT NULL,
  `api_server` varchar(100) DEFAULT NULL,
  `status` varchar(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_t_db_config_u1` (`sync_tag`),
  KEY `idx_create_date_u1` (`sync_tag`)
) ENGINE=InnoDB AUTO_INCREMENT=258 DEFAULT CHARSET=utf8;

/*Table structure for table `t_db_sync_tasks_log` */

DROP TABLE IF EXISTS `t_db_sync_tasks_log`;

CREATE TABLE `t_db_sync_tasks_log` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `sync_tag` varchar(100) NOT NULL,
  `create_date` datetime DEFAULT NULL,
  `duration` int(11) DEFAULT NULL,
  `amount` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_create_date_n1` (`create_date`),
  KEY `idx_create_date_u1` (`sync_tag`)
) ENGINE=InnoDB AUTO_INCREMENT=806734 DEFAULT CHARSET=utf8;

/*Table structure for table `t_db_sync_tasks_log_detail` */

DROP TABLE IF EXISTS `t_db_sync_tasks_log_detail`;

CREATE TABLE `t_db_sync_tasks_log_detail` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `sync_tag` varchar(100) NOT NULL,
  `create_date` datetime DEFAULT NULL,
  `sync_table` varchar(100) DEFAULT NULL,
  `sync_amount` int(11) DEFAULT NULL,
  `duration` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_create_date_n1` (`create_date`),
  KEY `idx_create_date_u1` (`sync_tag`)
) ENGINE=InnoDB AUTO_INCREMENT=2031616 DEFAULT CHARSET=utf8;

/*Table structure for table `t_dmlx` */

DROP TABLE IF EXISTS `t_dmlx`;

CREATE TABLE `t_dmlx` (
  `dm` varchar(10) NOT NULL,
  `mc` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`dm`),
  KEY `idx_t_dmlx` (`dm`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Table structure for table `t_dmmx` */

DROP TABLE IF EXISTS `t_dmmx`;

CREATE TABLE `t_dmmx` (
  `dm` varchar(10) NOT NULL DEFAULT '',
  `dmm` varchar(20) NOT NULL DEFAULT '',
  `dmmc` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`dm`,`dmm`),
  KEY `idx_t_dmmx` (`dm`,`dmm`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Table structure for table `t_forget_password` */

DROP TABLE IF EXISTS `t_forget_password`;

CREATE TABLE `t_forget_password` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `authentication_string` varchar(100) DEFAULT NULL,
  `flag` varchar(20) DEFAULT NULL,
  `creation_date` datetime DEFAULT NULL,
  `creator` varchar(20) DEFAULT NULL,
  `last_update_date` datetime DEFAULT NULL,
  `updator` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;

/*Table structure for table `t_role` */

DROP TABLE IF EXISTS `t_role`;

CREATE TABLE `t_role` (
  `id` int(11) NOT NULL,
  `name` varchar(20) DEFAULT NULL,
  `status` varchar(1) DEFAULT NULL,
  `creation_date` date DEFAULT NULL,
  `creator` varchar(20) DEFAULT NULL,
  `last_update_date` date DEFAULT NULL,
  `updator` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Table structure for table `t_role_privs` */

DROP TABLE IF EXISTS `t_role_privs`;

CREATE TABLE `t_role_privs` (
  `role_id` int(11) NOT NULL,
  `priv_id` varchar(20) DEFAULT NULL,
  `creation_date` date DEFAULT NULL,
  `creator` varchar(20) DEFAULT NULL,
  `last_update_date` date DEFAULT NULL,
  `updator` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Table structure for table `t_server` */

DROP TABLE IF EXISTS `t_server`;

CREATE TABLE `t_server` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `market_id` varchar(20) NOT NULL,
  `server_type` varchar(100) DEFAULT NULL,
  `server_desc` varchar(100) DEFAULT NULL,
  `server_ip` varchar(100) NOT NULL,
  `server_port` varchar(10) NOT NULL,
  `server_user` varchar(20) NOT NULL,
  `server_pass` varchar(200) NOT NULL,
  `server_os` varchar(100) NOT NULL,
  `server_cpu` varchar(100) NOT NULL,
  `server_mem` varchar(100) NOT NULL,
  `status` varchar(20) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=38 DEFAULT CHARSET=utf8;

/*Table structure for table `t_sql_audit_rule` */

DROP TABLE IF EXISTS `t_sql_audit_rule`;

CREATE TABLE `t_sql_audit_rule` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `rule_code` varchar(50) DEFAULT NULL,
  `rule_name` varchar(100) DEFAULT NULL,
  `rule_value` varchar(100) DEFAULT NULL,
  `error` varchar(100) DEFAULT NULL,
  `status` varchar(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_t_sql_audit_rule_u1` (`rule_code`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8;

/*Table structure for table `t_sql_audit_rule_err` */

DROP TABLE IF EXISTS `t_sql_audit_rule_err`;

CREATE TABLE `t_sql_audit_rule_err` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `rule_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `obj_name` varchar(50) DEFAULT NULL,
  `error` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=318 DEFAULT CHARSET=utf8;

/*Table structure for table `t_sql_release` */

DROP TABLE IF EXISTS `t_sql_release`;

CREATE TABLE `t_sql_release` (
  `id` int(11) NOT NULL,
  `dbid` int(11) NOT NULL,
  `sqltext` longtext,
  `status` varchar(1) DEFAULT NULL,
  `message` varchar(2000) DEFAULT NULL,
  `creation_date` datetime DEFAULT NULL,
  `creator` varchar(20) DEFAULT NULL,
  `last_update_date` datetime DEFAULT NULL,
  `updator` varchar(20) DEFAULT NULL,
  `audit_date` datetime DEFAULT NULL,
  `auditor` varchar(20) DEFAULT NULL,
  `version` varchar(20) DEFAULT NULL,
  `type` varchar(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Table structure for table `t_sql_release_results` */

DROP TABLE IF EXISTS `t_sql_release_results`;

CREATE TABLE `t_sql_release_results` (
  `id` int(11) NOT NULL,
  `release_id` int(11) DEFAULT NULL,
  `db_env` varchar(1) DEFAULT NULL,
  `db_status` varchar(1) DEFAULT NULL,
  `db_msg` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Table structure for table `t_sys_usage` */

DROP TABLE IF EXISTS `t_sys_usage`;

CREATE TABLE `t_sys_usage` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ip` varchar(15) DEFAULT NULL,
  `port` varchar(5) DEFAULT NULL,
  `rq` datetime DEFAULT NULL,
  `cpu_usage_rate` decimal(10,2) DEFAULT NULL,
  `memory_usage_rate` decimal(10,2) DEFAULT NULL,
  `disk_read_bytes` bigint(20) DEFAULT NULL,
  `disk_write_bytes` bigint(20) DEFAULT NULL,
  `net_send_bytes` bigint(20) DEFAULT NULL,
  `net_recv_bytes` bigint(20) DEFAULT NULL,
  KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Table structure for table `t_user` */

DROP TABLE IF EXISTS `t_user`;

CREATE TABLE `t_user` (
  `id` int(11) NOT NULL,
  `name` varchar(20) DEFAULT NULL,
  `gender` varchar(2) DEFAULT NULL,
  `email` varchar(40) DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `dept` varchar(20) DEFAULT NULL,
  `expire_date` date DEFAULT NULL,
  `password` varchar(200) DEFAULT NULL,
  `status` varchar(1) DEFAULT NULL,
  `creation_date` date DEFAULT NULL,
  `creator` varchar(20) DEFAULT NULL,
  `last_update_date` date DEFAULT NULL,
  `updator` varchar(20) DEFAULT NULL,
  `login_name` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Table structure for table `t_user_proj_privs` */

DROP TABLE IF EXISTS `t_user_proj_privs`;

CREATE TABLE `t_user_proj_privs` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `proj_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `priv_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;

/*Table structure for table `t_user_role` */

DROP TABLE IF EXISTS `t_user_role`;

CREATE TABLE `t_user_role` (
  `user_id` int(11) NOT NULL,
  `role_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Table structure for table `t_xtqx` */

DROP TABLE IF EXISTS `t_xtqx`;

CREATE TABLE `t_xtqx` (
  `id` varchar(10) NOT NULL DEFAULT '',
  `name` varchar(20) DEFAULT NULL,
  `parent_id` varchar(10) DEFAULT NULL,
  `url` varchar(100) DEFAULT NULL,
  `status` varchar(1) DEFAULT NULL,
  `icon` varchar(50) DEFAULT NULL,
  `creation_date` date DEFAULT NULL,
  `creator` varchar(20) DEFAULT NULL,
  `last_update_date` date DEFAULT NULL,
  `updator` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
