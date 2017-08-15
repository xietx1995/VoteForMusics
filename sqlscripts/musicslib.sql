-- MySQL dump 10.13  Distrib 5.7.19, for Win64 (x86_64)
--
-- Host: localhost    Database: musicslib
-- ------------------------------------------------------
-- Server version	5.7.19-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `musics_info`
--

DROP TABLE IF EXISTS `musics_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `musics_info` (
  `m_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `m_name` char(50) NOT NULL DEFAULT '0' COMMENT '音乐名',
  `s_happy` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '欢乐的',
  `s_miss` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '思念的',
  `s_terrified` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '恐惧的',
  `s_troubled` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '不安的',
  `s_disappointed` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '失落的',
  `s_guilty` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '内疚的',
  `s_jealous` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '妒忌的',
  `s_shy` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '害羞的',
  `s_wish` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '祝愿的',
  `s_praise` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '赞扬的',
  `s_angry` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '愤怒的',
  `s_sacred` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '神圣的',
  `s_aroused` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '激昂的',
  `s_grand` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '宏伟的',
  `s_solemn` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '庄严地',
  `s_peaceful` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '安心的',
  `s_panic` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '慌张的',
  `s_hate` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '憎恶的',
  `s_criticise` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '贬责的',
  `s_surprise` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '惊讶的',
  `s_doubt` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '怀疑的',
  `s_sad` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '悲伤的',
  `s_warm` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '温暖的',
  `s_friendship` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '友情的',
  `s_in_love` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '热恋的',
  `s_motivate` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '励志的',
  `s_blue` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '忧郁的',
  PRIMARY KEY (`m_id`),
  UNIQUE KEY `m_name_unique` (`m_name`),
  FULLTEXT KEY `m_name_fulltext` (`m_name`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8 COMMENT='音乐信息';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `musics_info`
--

LOCK TABLES `musics_info` WRITE;
/*!40000 ALTER TABLE `musics_info` DISABLE KEYS */;
INSERT INTO `musics_info` VALUES (1,'《夜色钢琴曲》爱情转移 - 赵海洋',0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0),(2,'莫扎特：土耳其进行曲',0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0),(3,'BBF - 我们万岁',0,0,1,1,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,1,1,0,0,0,0,0),(4,'Beyond - 不再犹豫',0,1,0,0,1,0,0,0,0,0,1,0,1,0,0,0,0,0,0,1,0,0,1,1,0,0,0),(5,'Beyond - 光辉岁月',0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,1,0,1,0,0,0,0),(6,'Beyond - 海阔天空',0,1,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,2,1,0,0,0,0,0,0),(7,'Beyond - 冷雨夜',0,1,1,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0),(8,'F.I.R. - 我们的爱',0,1,0,0,0,0,0,0,0,0,1,1,1,0,1,1,0,0,1,1,0,0,0,0,0,0,0),(9,'J3男团 - 万有引力',0,0,2,0,0,0,0,0,0,0,1,2,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0),(10,'M4M - 当你离开我',0,2,3,1,1,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0);
/*!40000 ALTER TABLE `musics_info` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-08-15 10:22:22
