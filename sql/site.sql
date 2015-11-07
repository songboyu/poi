/*
 Navicat Premium Data Transfer

 Source Server         : localhost
 Source Server Type    : MySQL
 Source Server Version : 50626
 Source Host           : 127.0.0.1
 Source Database       : poi

 Target Server Type    : MySQL
 Target Server Version : 50626
 File Encoding         : utf-8

 Date: 11/07/2015 23:59:33 PM
*/

SET NAMES utf8;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
--  Table structure for `site`
-- ----------------------------
DROP TABLE IF EXISTS `site`;
CREATE TABLE `site` (
  `site_id` int(11) NOT NULL,
  `site_name` varchar(255) NOT NULL,
  `site_url` varchar(255) NOT NULL,
  `up` int(11) DEFAULT NULL,
  `down` int(11) DEFAULT NULL,
  PRIMARY KEY (`site_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
--  Records of `site`
-- ----------------------------
BEGIN;
INSERT INTO `site` VALUES ('1', '天涯社区', 'http://www.tianya.cn/', null, null), ('2', '网易', 'http://blog.163.com/', null, null), ('3', '百度', 'http://tieba.baidu.com', null, null), ('4', '知乎', 'http://www.zhihu.com', null, null), ('5', '猫扑', 'http://www.mop.com/', null, null), ('6', '世纪佳缘', 'http://www.jiayuan.com/', null, null), ('7', '人人网', 'http://www.renren.com/', null, null), ('8', '豆瓣', 'http://www.douban.com/', null, null), ('9', '珍爱网', 'http://www.zhenai.com/', null, null), ('10', '我在找你', 'http://www.95195.com/', null, null), ('11', '玫瑰情人网', 'http://www.qingrenw.com/', null, null), ('12', '百合网', 'http://www.baihe.com', null, null), ('13', '易动网', 'http://www.easydong.com/', null, null), ('14', '若邻网', 'http://www.wealink.com/', null, null), ('15', '7651红娘网', 'http://www.7651.com/', null, null), ('16', '淘男网', 'http://www.51taonan.com/', null, null), ('17', '缘来客', 'http://www.ylike.com/', null, null), ('18', '真情在线', 'http://www.lol99.com/', null, null), ('19', '情人岛', 'http://www.7rdao.com/', null, null), ('20', '简简单单', 'http://www.jjdd.me/', null, null), ('21', '美丽情缘', 'http://www.51findlove.cn/', null, null), ('22', '中国红娘网', 'http://www.hongniang.com/', null, null), ('23', '秀色花园', 'http://www.showse.com/', null, null), ('24', '村友网', 'http://www.cunyouwang.com/', null, null), ('25', '爱真心', 'http://www.izhenxin.com/', null, null), ('26', '网易花田', 'http://love.163.com/', null, null), ('27', '久爱网', 'http://www.2177s.com/', null, null), ('28', '杭州相亲网', 'http://www.hzxq.net/', null, null), ('29', '51交友中心', 'http://www.51lover.org/', null, null), ('30', '赶集婚恋', 'http://love.ganji.com/', null, null);
COMMIT;

SET FOREIGN_KEY_CHECKS = 1;
