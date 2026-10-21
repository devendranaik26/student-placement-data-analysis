-- MySQL dump 10.13  Distrib 8.0.46, for Win64 (x86_64)
--
-- Host: localhost    Database: student_placement_db
-- ------------------------------------------------------
-- Server version	8.0.46

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `placements`
--

DROP TABLE IF EXISTS `placements`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `placements` (
  `placement_id` int NOT NULL AUTO_INCREMENT,
  `student_id` int NOT NULL,
  `company` varchar(100) NOT NULL,
  `job_role` varchar(100) NOT NULL,
  `package_lpa` decimal(5,2) DEFAULT NULL,
  `placement_date` date DEFAULT NULL,
  `status` varchar(20) NOT NULL,
  PRIMARY KEY (`placement_id`),
  UNIQUE KEY `uq_placements_student` (`student_id`),
  CONSTRAINT `placements_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `students` (`student_id`)
) ENGINE=InnoDB AUTO_INCREMENT=128 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `placements`
--

LOCK TABLES `placements` WRITE;
/*!40000 ALTER TABLE `placements` DISABLE KEYS */;
INSERT INTO `placements` VALUES (65,51,'Microsoft','ML Engineer',4.00,'2026-12-14','Placed'),(66,54,'Microsoft','ML Engineer',12.00,'2026-02-13','Placed'),(67,48,'TCS','Software Engineer',12.00,'2026-09-09','Placed'),(68,57,'Accenture','Data Analyst',12.00,'2026-10-04','Placed'),(69,56,'Accenture','ML Engineer',4.00,'2026-05-07','Placed'),(70,50,'TCS','Data Analyst',6.50,'2026-06-17','Placed'),(71,60,'Accenture','Software Engineer',8.00,'2026-05-18','Placed'),(72,59,'TCS','Data Analyst',4.00,'2026-03-06','Placed'),(73,53,'Infosys','Data Analyst',12.00,'2026-02-14','Placed'),(74,45,'Microsoft','ML Engineer',6.50,'2026-03-27','Placed'),(75,47,'Accenture','Software Engineer',6.50,'2026-04-03','Placed'),(76,52,'TCS','Software Engineer',6.50,'2026-12-24','Placed'),(77,38,'Amazon','Software Engineer',4.00,'2026-05-15','Placed'),(78,24,'Infosys','Data Analyst',8.00,'2026-04-02','Placed'),(79,27,'Google','ML Engineer',5.00,'2026-05-11','Placed'),(80,23,'Accenture','Data Analyst',12.00,'2026-11-24','Placed'),(81,22,'Infosys','Software Engineer',4.00,'2026-11-25','Placed'),(82,40,'Microsoft','ML Engineer',8.00,'2026-06-20','Placed'),(83,30,'Microsoft','Data Analyst',12.00,'2026-08-13','Placed'),(84,29,'Infosys','Data Analyst',6.50,'2026-08-19','Placed'),(85,33,'Accenture','ML Engineer',8.00,'2026-03-21','Placed'),(86,31,'Google','Software Engineer',8.00,'2026-08-06','Placed'),(87,35,'TCS','Software Engineer',12.00,'2026-08-04','Placed'),(88,28,'Google','ML Engineer',6.50,'2026-11-04','Placed'),(89,34,'Accenture','Data Analyst',6.50,'2026-11-27','Placed'),(90,32,'Accenture','ML Engineer',5.00,'2026-02-06','Placed'),(91,14,'Amazon','ML Engineer',12.00,'2026-05-11','Placed'),(92,3,'Microsoft','Data Analyst',6.50,'2026-08-20','Placed'),(93,2,'Accenture','Developer',6.50,'2026-11-15','Placed'),(94,10,'Accenture','ML Engineer',4.00,'2026-12-20','Placed'),(95,12,'TCS','Developer',4.00,'2026-08-23','Placed'),(96,15,'Google','Data Analyst',12.00,'2026-08-18','Placed'),(97,1,'Microsoft','Developer',6.50,'2026-02-20','Placed'),(98,13,'Amazon','ML Engineer',5.00,'2026-09-04','Placed'),(99,5,'Microsoft','Data Analyst',6.50,'2026-09-17','Placed'),(100,8,'Google','Software Engineer',12.00,'2026-11-05','Placed'),(101,11,'Infosys','Software Engineer',8.00,'2026-10-01','Placed'),(102,18,'Amazon','ML Engineer',12.00,'2026-10-17','Placed'),(103,17,'Microsoft','ML Engineer',6.50,'2026-08-30','Placed'),(104,20,'TCS','Developer',6.50,'2026-10-05','Placed'),(105,9,'Microsoft','ML Engineer',5.00,'2026-02-16','Placed'),(106,16,'Infosys','Software Engineer',6.50,'2026-11-28','Placed'),(107,78,'Google','Data Analyst',8.00,'2026-01-22','Placed'),(108,75,'Amazon','Software Engineer',6.50,'2026-02-15','Placed'),(109,61,'Google','ML Engineer',5.00,'2026-03-02','Placed'),(110,66,'Microsoft','Data Analyst',5.00,'2026-01-24','Placed'),(111,79,'Infosys','Software Engineer',6.50,'2026-05-20','Placed'),(112,68,'Microsoft','Data Analyst',8.00,'2026-08-10','Placed'),(113,67,'Accenture','ML Engineer',6.50,'2026-11-09','Placed'),(114,63,'Infosys','Data Analyst',5.00,'2026-02-28','Placed'),(115,72,'Accenture','Data Analyst',12.00,'2026-02-13','Placed'),(116,73,'Google','Software Engineer',5.00,'2026-06-01','Placed'),(117,89,'Accenture','ML Engineer',6.50,'2026-07-13','Placed'),(118,87,'Google','Developer',8.00,'2026-03-09','Placed'),(119,94,'TCS','Data Analyst',8.00,'2026-08-02','Placed'),(120,99,'Infosys','Software Engineer',5.00,'2026-12-06','Placed'),(121,92,'TCS','ML Engineer',5.00,'2026-09-16','Placed'),(122,88,'Amazon','Data Analyst',12.00,'2026-08-04','Placed'),(123,95,'Microsoft','Developer',5.00,'2026-10-14','Placed'),(124,93,'Google','Data Analyst',4.00,'2026-05-21','Placed');
/*!40000 ALTER TABLE `placements` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `skills`
--

DROP TABLE IF EXISTS `skills`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `skills` (
  `skill_id` int NOT NULL AUTO_INCREMENT,
  `skill_name` varchar(50) NOT NULL,
  PRIMARY KEY (`skill_id`),
  UNIQUE KEY `skill_name` (`skill_name`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `skills`
--

LOCK TABLES `skills` WRITE;
/*!40000 ALTER TABLE `skills` DISABLE KEYS */;
INSERT INTO `skills` VALUES (3,'C'),(4,'C++'),(7,'CSS'),(11,'Data Structures and Algorithms'),(10,'Deep Learning'),(14,'Git and GitHub'),(6,'HTML'),(1,'Java'),(8,'JavaScript'),(9,'Machine Learning'),(5,'MySQL'),(13,'NumPy'),(12,'Pandas'),(2,'Python');
/*!40000 ALTER TABLE `skills` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `student_skills`
--

DROP TABLE IF EXISTS `student_skills`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `student_skills` (
  `student_id` int NOT NULL,
  `skill_id` int NOT NULL,
  PRIMARY KEY (`student_id`,`skill_id`),
  KEY `skill_id` (`skill_id`),
  CONSTRAINT `student_skills_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `students` (`student_id`),
  CONSTRAINT `student_skills_ibfk_2` FOREIGN KEY (`skill_id`) REFERENCES `skills` (`skill_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `student_skills`
--

LOCK TABLES `student_skills` WRITE;
/*!40000 ALTER TABLE `student_skills` DISABLE KEYS */;
INSERT INTO `student_skills` VALUES (1,1),(2,1),(3,1),(4,1),(5,1),(6,1),(7,1),(8,1),(9,1),(10,1),(11,1),(12,1),(13,1),(14,1),(15,1),(16,1),(17,1),(18,1),(19,1),(20,1),(21,1),(22,1),(23,1),(24,1),(25,1),(26,1),(27,1),(28,1),(29,1),(30,1),(31,1),(32,1),(33,1),(34,1),(35,1),(36,1),(37,1),(38,1),(39,1),(40,1),(61,1),(62,1),(63,1),(64,1),(65,1),(66,1),(67,1),(68,1),(69,1),(70,1),(71,1),(72,1),(73,1),(74,1),(75,1),(76,1),(77,1),(78,1),(79,1),(80,1),(81,1),(82,1),(83,1),(84,1),(85,1),(86,1),(87,1),(88,1),(89,1),(90,1),(91,1),(92,1),(93,1),(94,1),(95,1),(96,1),(97,1),(98,1),(99,1),(100,1),(1,2),(2,2),(3,2),(4,2),(5,2),(6,2),(7,2),(8,2),(9,2),(10,2),(11,2),(12,2),(13,2),(14,2),(15,2),(16,2),(17,2),(18,2),(19,2),(20,2),(21,2),(22,2),(23,2),(24,2),(25,2),(26,2),(27,2),(28,2),(29,2),(30,2),(31,2),(32,2),(33,2),(34,2),(35,2),(36,2),(37,2),(38,2),(39,2),(40,2),(41,2),(42,2),(43,2),(44,2),(45,2),(46,2),(47,2),(48,2),(49,2),(50,2),(51,2),(52,2),(53,2),(54,2),(55,2),(56,2),(57,2),(58,2),(59,2),(60,2),(61,2),(62,2),(63,2),(64,2),(65,2),(66,2),(67,2),(68,2),(69,2),(70,2),(71,2),(72,2),(73,2),(74,2),(75,2),(76,2),(77,2),(78,2),(79,2),(80,2),(81,2),(82,2),(83,2),(84,2),(85,2),(86,2),(87,2),(88,2),(89,2),(90,2),(91,2),(92,2),(93,2),(94,2),(95,2),(96,2),(97,2),(98,2),(99,2),(100,2),(1,3),(2,3),(3,3),(4,3),(5,3),(6,3),(7,3),(8,3),(9,3),(10,3),(11,3),(12,3),(13,3),(14,3),(15,3),(16,3),(17,3),(18,3),(19,3),(20,3),(61,3),(62,3),(63,3),(64,3),(65,3),(66,3),(67,3),(68,3),(69,3),(70,3),(71,3),(72,3),(73,3),(74,3),(75,3),(76,3),(77,3),(78,3),(79,3),(80,3),(1,4),(2,4),(3,4),(4,4),(5,4),(6,4),(7,4),(8,4),(9,4),(10,4),(11,4),(12,4),(13,4),(14,4),(15,4),(16,4),(17,4),(18,4),(19,4),(20,4),(61,4),(62,4),(63,4),(64,4),(65,4),(66,4),(67,4),(68,4),(69,4),(70,4),(71,4),(72,4),(73,4),(74,4),(75,4),(76,4),(77,4),(78,4),(79,4),(80,4),(1,5),(2,5),(3,5),(4,5),(5,5),(6,5),(7,5),(8,5),(9,5),(10,5),(11,5),(12,5),(13,5),(14,5),(15,5),(16,5),(17,5),(18,5),(19,5),(20,5),(41,5),(42,5),(43,5),(44,5),(45,5),(46,5),(47,5),(48,5),(49,5),(50,5),(51,5),(52,5),(53,5),(54,5),(55,5),(56,5),(57,5),(58,5),(59,5),(60,5),(61,5),(62,5),(63,5),(64,5),(65,5),(66,5),(67,5),(68,5),(69,5),(70,5),(71,5),(72,5),(73,5),(74,5),(75,5),(76,5),(77,5),(78,5),(79,5),(80,5),(81,5),(82,5),(83,5),(84,5),(85,5),(86,5),(87,5),(88,5),(89,5),(90,5),(91,5),(92,5),(93,5),(94,5),(95,5),(96,5),(97,5),(98,5),(99,5),(100,5),(1,6),(2,6),(3,6),(4,6),(5,6),(6,6),(7,6),(8,6),(9,6),(10,6),(11,6),(12,6),(13,6),(14,6),(15,6),(16,6),(17,6),(18,6),(19,6),(20,6),(61,6),(62,6),(63,6),(64,6),(65,6),(66,6),(67,6),(68,6),(69,6),(70,6),(71,6),(72,6),(73,6),(74,6),(75,6),(76,6),(77,6),(78,6),(79,6),(80,6),(81,6),(82,6),(83,6),(84,6),(85,6),(86,6),(87,6),(88,6),(89,6),(90,6),(91,6),(92,6),(93,6),(94,6),(95,6),(96,6),(97,6),(98,6),(99,6),(100,6),(1,7),(2,7),(3,7),(4,7),(5,7),(6,7),(7,7),(8,7),(9,7),(10,7),(11,7),(12,7),(13,7),(14,7),(15,7),(16,7),(17,7),(18,7),(19,7),(20,7),(61,7),(62,7),(63,7),(64,7),(65,7),(66,7),(67,7),(68,7),(69,7),(70,7),(71,7),(72,7),(73,7),(74,7),(75,7),(76,7),(77,7),(78,7),(79,7),(80,7),(81,7),(82,7),(83,7),(84,7),(85,7),(86,7),(87,7),(88,7),(89,7),(90,7),(91,7),(92,7),(93,7),(94,7),(95,7),(96,7),(97,7),(98,7),(99,7),(100,7),(1,8),(2,8),(3,8),(4,8),(5,8),(6,8),(7,8),(8,8),(9,8),(10,8),(11,8),(12,8),(13,8),(14,8),(15,8),(16,8),(17,8),(18,8),(19,8),(20,8),(81,8),(82,8),(83,8),(84,8),(85,8),(86,8),(87,8),(88,8),(89,8),(90,8),(91,8),(92,8),(93,8),(94,8),(95,8),(96,8),(97,8),(98,8),(99,8),(100,8),(21,9),(22,9),(23,9),(24,9),(25,9),(26,9),(27,9),(28,9),(29,9),(30,9),(31,9),(32,9),(33,9),(34,9),(35,9),(36,9),(37,9),(38,9),(39,9),(40,9),(41,9),(42,9),(43,9),(44,9),(45,9),(46,9),(47,9),(48,9),(49,9),(50,9),(51,9),(52,9),(53,9),(54,9),(55,9),(56,9),(57,9),(58,9),(59,9),(60,9),(21,10),(22,10),(23,10),(24,10),(25,10),(26,10),(27,10),(28,10),(29,10),(30,10),(31,10),(32,10),(33,10),(34,10),(35,10),(36,10),(37,10),(38,10),(39,10),(40,10),(41,10),(42,10),(43,10),(44,10),(45,10),(46,10),(47,10),(48,10),(49,10),(50,10),(51,10),(52,10),(53,10),(54,10),(55,10),(56,10),(57,10),(58,10),(59,10),(60,10),(1,11),(2,11),(3,11),(4,11),(5,11),(6,11),(7,11),(8,11),(9,11),(10,11),(11,11),(12,11),(13,11),(14,11),(15,11),(16,11),(17,11),(18,11),(19,11),(20,11),(21,11),(22,11),(23,11),(24,11),(25,11),(26,11),(27,11),(28,11),(29,11),(30,11),(31,11),(32,11),(33,11),(34,11),(35,11),(36,11),(37,11),(38,11),(39,11),(40,11),(41,11),(42,11),(43,11),(44,11),(45,11),(46,11),(47,11),(48,11),(49,11),(50,11),(51,11),(52,11),(53,11),(54,11),(55,11),(56,11),(57,11),(58,11),(59,11),(60,11),(61,11),(62,11),(63,11),(64,11),(65,11),(66,11),(67,11),(68,11),(69,11),(70,11),(71,11),(72,11),(73,11),(74,11),(75,11),(76,11),(77,11),(78,11),(79,11),(80,11),(81,11),(82,11),(83,11),(84,11),(85,11),(86,11),(87,11),(88,11),(89,11),(90,11),(91,11),(92,11),(93,11),(94,11),(95,11),(96,11),(97,11),(98,11),(99,11),(100,11),(21,12),(22,12),(23,12),(24,12),(25,12),(26,12),(27,12),(28,12),(29,12),(30,12),(31,12),(32,12),(33,12),(34,12),(35,12),(36,12),(37,12),(38,12),(39,12),(40,12),(41,12),(42,12),(43,12),(44,12),(45,12),(46,12),(47,12),(48,12),(49,12),(50,12),(51,12),(52,12),(53,12),(54,12),(55,12),(56,12),(57,12),(58,12),(59,12),(60,12),(81,12),(82,12),(83,12),(84,12),(85,12),(86,12),(87,12),(88,12),(89,12),(90,12),(91,12),(92,12),(93,12),(94,12),(95,12),(96,12),(97,12),(98,12),(99,12),(100,12),(21,13),(22,13),(23,13),(24,13),(25,13),(26,13),(27,13),(28,13),(29,13),(30,13),(31,13),(32,13),(33,13),(34,13),(35,13),(36,13),(37,13),(38,13),(39,13),(40,13),(41,13),(42,13),(43,13),(44,13),(45,13),(46,13),(47,13),(48,13),(49,13),(50,13),(51,13),(52,13),(53,13),(54,13),(55,13),(56,13),(57,13),(58,13),(59,13),(60,13),(81,13),(82,13),(83,13),(84,13),(85,13),(86,13),(87,13),(88,13),(89,13),(90,13),(91,13),(92,13),(93,13),(94,13),(95,13),(96,13),(97,13),(98,13),(99,13),(100,13),(1,14),(2,14),(3,14),(4,14),(5,14),(6,14),(7,14),(8,14),(9,14),(10,14),(11,14),(12,14),(13,14),(14,14),(15,14),(16,14),(17,14),(18,14),(19,14),(20,14),(21,14),(22,14),(23,14),(24,14),(25,14),(26,14),(27,14),(28,14),(29,14),(30,14),(31,14),(32,14),(33,14),(34,14),(35,14),(36,14),(37,14),(38,14),(39,14),(40,14),(41,14),(42,14),(43,14),(44,14),(45,14),(46,14),(47,14),(48,14),(49,14),(50,14),(51,14),(52,14),(53,14),(54,14),(55,14),(56,14),(57,14),(58,14),(59,14),(60,14),(81,14),(82,14),(83,14),(84,14),(85,14),(86,14),(87,14),(88,14),(89,14),(90,14),(91,14),(92,14),(93,14),(94,14),(95,14),(96,14),(97,14),(98,14),(99,14),(100,14);
/*!40000 ALTER TABLE `student_skills` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `students`
--

DROP TABLE IF EXISTS `students`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `students` (
  `student_id` int NOT NULL AUTO_INCREMENT,
  `roll_no` varchar(20) NOT NULL,
  `department` varchar(50) NOT NULL,
  `graduation_year` int NOT NULL,
  PRIMARY KEY (`student_id`),
  UNIQUE KEY `roll_no` (`roll_no`)
) ENGINE=InnoDB AUTO_INCREMENT=128 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `students`
--

LOCK TABLES `students` WRITE;
/*!40000 ALTER TABLE `students` DISABLE KEYS */;
INSERT INTO `students` VALUES (1,'CSE001','CSE',2029),(2,'CSE002','CSE',2029),(3,'CSE003','CSE',2029),(4,'CSE004','CSE',2029),(5,'CSE005','CSE',2029),(6,'CSE006','CSE',2029),(7,'CSE007','CSE',2029),(8,'CSE008','CSE',2029),(9,'CSE009','CSE',2029),(10,'CSE010','CSE',2029),(11,'CSE011','CSE',2029),(12,'CSE012','CSE',2029),(13,'CSE013','CSE',2029),(14,'CSE014','CSE',2029),(15,'CSE015','CSE',2029),(16,'CSE016','CSE',2029),(17,'CSE017','CSE',2029),(18,'CSE018','CSE',2029),(19,'CSE019','CSE',2029),(20,'CSE020','CSE',2029),(21,'AIML001','AIML',2029),(22,'AIML002','AIML',2029),(23,'AIML003','AIML',2029),(24,'AIML004','AIML',2029),(25,'AIML005','AIML',2029),(26,'AIML006','AIML',2029),(27,'AIML007','AIML',2029),(28,'AIML008','AIML',2029),(29,'AIML009','AIML',2029),(30,'AIML010','AIML',2029),(31,'AIML011','AIML',2029),(32,'AIML012','AIML',2029),(33,'AIML013','AIML',2029),(34,'AIML014','AIML',2029),(35,'AIML015','AIML',2029),(36,'AIML016','AIML',2029),(37,'AIML017','AIML',2029),(38,'AIML018','AIML',2029),(39,'AIML019','AIML',2029),(40,'AIML020','AIML',2029),(41,'AIDS001','AIDS',2029),(42,'AIDS002','AIDS',2029),(43,'AIDS003','AIDS',2029),(44,'AIDS004','AIDS',2029),(45,'AIDS005','AIDS',2029),(46,'AIDS006','AIDS',2029),(47,'AIDS007','AIDS',2029),(48,'AIDS008','AIDS',2029),(49,'AIDS009','AIDS',2029),(50,'AIDS010','AIDS',2029),(51,'AIDS011','AIDS',2029),(52,'AIDS012','AIDS',2029),(53,'AIDS013','AIDS',2029),(54,'AIDS014','AIDS',2029),(55,'AIDS015','AIDS',2029),(56,'AIDS016','AIDS',2029),(57,'AIDS017','AIDS',2029),(58,'AIDS018','AIDS',2029),(59,'AIDS019','AIDS',2029),(60,'AIDS020','AIDS',2029),(61,'ECE001','ECE',2029),(62,'ECE002','ECE',2029),(63,'ECE003','ECE',2029),(64,'ECE004','ECE',2029),(65,'ECE005','ECE',2029),(66,'ECE006','ECE',2029),(67,'ECE007','ECE',2029),(68,'ECE008','ECE',2029),(69,'ECE009','ECE',2029),(70,'ECE010','ECE',2029),(71,'ECE011','ECE',2029),(72,'ECE012','ECE',2029),(73,'ECE013','ECE',2029),(74,'ECE014','ECE',2029),(75,'ECE015','ECE',2029),(76,'ECE016','ECE',2029),(77,'ECE017','ECE',2029),(78,'ECE018','ECE',2029),(79,'ECE019','ECE',2029),(80,'ECE020','ECE',2029),(81,'IT001','IT',2029),(82,'IT002','IT',2029),(83,'IT003','IT',2029),(84,'IT004','IT',2029),(85,'IT005','IT',2029),(86,'IT006','IT',2029),(87,'IT007','IT',2029),(88,'IT008','IT',2029),(89,'IT009','IT',2029),(90,'IT010','IT',2029),(91,'IT011','IT',2029),(92,'IT012','IT',2029),(93,'IT013','IT',2029),(94,'IT014','IT',2029),(95,'IT015','IT',2029),(96,'IT016','IT',2029),(97,'IT017','IT',2029),(98,'IT018','IT',2029),(99,'IT019','IT',2029),(100,'IT020','IT',2029);
/*!40000 ALTER TABLE `students` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-10-21  9:34:30
