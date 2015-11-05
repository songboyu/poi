/*
Navicat MySQL Data Transfer

Source Server         : 55
Source Server Version : 50621
Source Host           : 192.168.8.55:3306
Source Database       : poi

Target Server Type    : MYSQL
Target Server Version : 50621
File Encoding         : 65001

Date: 2015-11-05 12:45:22
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for poi
-- ----------------------------
DROP TABLE IF EXISTS `poi`;
CREATE TABLE `poi` (
  `site_id` int(11) NOT NULL,
  `user_id` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `location` varchar(255) DEFAULT NULL,
  `last_login_time` datetime DEFAULT NULL,
  `reg_time` datetime DEFAULT NULL,
  `login_num` int(11) DEFAULT NULL,
  `score` int(11) DEFAULT NULL,
  `level` varchar(255) DEFAULT NULL,
  `post_num` int(11) DEFAULT NULL,
  `reply_num` int(11) DEFAULT NULL,
  `followers` int(11) DEFAULT NULL,
  `following` int(11) DEFAULT NULL,
  `description` varchar(3000) DEFAULT NULL,
  `gender` char(1) DEFAULT NULL COMMENT 'M=男 F=女',
  `avatar` varchar(255) DEFAULT NULL,
  `marital_status` char(1) DEFAULT NULL COMMENT 'S=单身 M=已婚 D=离异',
  `education_level` char(1) DEFAULT NULL COMMENT 'A=博士及以上 B=硕士 C=本科 D=大专 E=中专/技校 F=中学',
  `occupation` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `qq` varchar(255) DEFAULT NULL,
  `cellphone` varchar(255) DEFAULT NULL,
  `last_update_time` datetime DEFAULT NULL,
  `birthday` datetime DEFAULT NULL,
  `hometown` varchar(255) DEFAULT NULL,
  `telephone` varchar(255) DEFAULT NULL,
  `salary` varchar(255) DEFAULT NULL,
  `speciality` varchar(255) DEFAULT NULL,
  `personality` varchar(255) DEFAULT NULL,
  `favorites` varchar(3000) DEFAULT NULL,
  `experience` varchar(3000) DEFAULT NULL,
  `weight` varchar(255) DEFAULT NULL,
  `height` varchar(255) DEFAULT NULL,
  `body_size` varchar(255) DEFAULT NULL,
  `looks` varchar(255) DEFAULT NULL,
  `blood_type` char(1) DEFAULT NULL,
  PRIMARY KEY (`site_id`,`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
