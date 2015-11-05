/*
Navicat MySQL Data Transfer

Source Server         : 55
Source Server Version : 50621
Source Host           : 192.168.8.55:3306
Source Database       : poi

Target Server Type    : MYSQL
Target Server Version : 50621
File Encoding         : 65001

Date: 2015-11-05 12:45:26
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for site
-- ----------------------------
DROP TABLE IF EXISTS `site`;
CREATE TABLE `site` (
  `site_id` int(11) NOT NULL,
  `site_name` varchar(255) NOT NULL,
  `site_url` varchar(255) NOT NULL,
  PRIMARY KEY (`site_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of site
-- ----------------------------
INSERT INTO `site` VALUES ('1', '天涯社区', 'http://www.tianya.cn/');
INSERT INTO `site` VALUES ('2', '网易', 'http://blog.163.com/');
INSERT INTO `site` VALUES ('3', '百度', 'http://tieba.baidu.com');
INSERT INTO `site` VALUES ('4', '知乎', 'http://www.zhihu.com');
INSERT INTO `site` VALUES ('5', '猫扑', 'http://www.mop.com/');
INSERT INTO `site` VALUES ('6', '世纪佳缘', 'http://www.jiayuan.com/');
INSERT INTO `site` VALUES ('7', '人人网', 'http://www.renren.com/');
INSERT INTO `site` VALUES ('8', '豆瓣', 'http://www.douban.com/');
INSERT INTO `site` VALUES ('9', '珍爱网', 'http://www.zhenai.com/');
INSERT INTO `site` VALUES ('10', '我在找你', 'http://www.95195.com/');
INSERT INTO `site` VALUES ('11', '玫瑰情人网', 'http://www.qingrenw.com/');
INSERT INTO `site` VALUES ('12', '百合网', 'http://www.baihe.com');
INSERT INTO `site` VALUES ('13', '易动网', 'http://www.easydong.com/');
INSERT INTO `site` VALUES ('14', '若邻网', 'http://www.wealink.com/');
