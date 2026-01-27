-- MySQL dump 10.13  Distrib 8.0.44, for Linux (x86_64)
--
-- Host: localhost    Database: medicient
-- ------------------------------------------------------
-- Server version	8.0.44-0ubuntu0.24.04.2

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `appointment`
--

DROP TABLE IF EXISTS `appointment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `appointment` (
  `appointment_id` int NOT NULL AUTO_INCREMENT,
  `doctor_id` int NOT NULL,
  `patient_id` int NOT NULL,
  `scheduled_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `symptoms` text NOT NULL,
  `medical_history_id` int DEFAULT NULL,
  `status` enum('scheduled','canceled','ongoing','ended') NOT NULL DEFAULT 'scheduled',
  PRIMARY KEY (`appointment_id`),
  KEY `doctor_id` (`doctor_id`),
  KEY `patient_id` (`patient_id`),
  CONSTRAINT `appointment_ibfk_1` FOREIGN KEY (`doctor_id`) REFERENCES `doctor` (`doctor_id`),
  CONSTRAINT `appointment_ibfk_2` FOREIGN KEY (`patient_id`) REFERENCES `patient` (`patient_id`)
) ENGINE=InnoDB AUTO_INCREMENT=10000000 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `appointment`
--

LOCK TABLES `appointment` WRITE;
/*!40000 ALTER TABLE `appointment` DISABLE KEYS */;
/*!40000 ALTER TABLE `appointment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `disease`
--

DROP TABLE IF EXISTS `disease`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `disease` (
  `disease_id` int NOT NULL AUTO_INCREMENT,
  `disease_name` varchar(50) NOT NULL,
  `symptoms` text NOT NULL,
  `disease_desc` text NOT NULL,
  `medicines_preferred` text NOT NULL,
  `precautions_needed` text NOT NULL,
  `first_case_on` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`disease_id`),
  UNIQUE KEY `disease_name` (`disease_name`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `disease`
--

LOCK TABLES `disease` WRITE;
/*!40000 ALTER TABLE `disease` DISABLE KEYS */;
INSERT INTO `disease` VALUES (1,'short term memory loss','forgetting basic things done right now ','seen in amir khan movie','no one preferred','always have some extra writting stuff avoid repetative mind load','2026-01-27 09:10:53'),(2,'diabatese','rise in bool sugar level , increase in weight ','this diesase is very common among all the indians ','no medicine yet ','avoiod sugar and high carb diet','2026-01-27 09:13:33'),(3,'indigestion','stomach ache','often occured after bad diet','digesto','avoide overeating','2026-01-27 19:33:17');
/*!40000 ALTER TABLE `disease` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `doctor`
--

DROP TABLE IF EXISTS `doctor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `doctor` (
  `doctor_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `license_number` varchar(50) NOT NULL,
  `spec_id` int NOT NULL,
  `skills` text,
  `doctor_desc` text,
  `spec_institute` varchar(50) NOT NULL,
  `work_location` text,
  PRIMARY KEY (`doctor_id`),
  UNIQUE KEY `license_number` (`license_number`),
  UNIQUE KEY `user_id` (`user_id`,`spec_id`),
  KEY `spec_id` (`spec_id`),
  CONSTRAINT `doctor_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`),
  CONSTRAINT `doctor_ibfk_2` FOREIGN KEY (`spec_id`) REFERENCES `specialization` (`spec_id`)
) ENGINE=InnoDB AUTO_INCREMENT=100001 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `doctor`
--

LOCK TABLES `doctor` WRITE;
/*!40000 ALTER TABLE `doctor` DISABLE KEYS */;
INSERT INTO `doctor` VALUES (100000,10,'DOC23333333',1,'best in vascular work,best in cardia arrest cases','a doctor','reputed institue','nowhare');
/*!40000 ALTER TABLE `doctor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `medical_history`
--

DROP TABLE IF EXISTS `medical_history`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `medical_history` (
  `record_id` int NOT NULL AUTO_INCREMENT,
  `doctor_id` int NOT NULL,
  `patient_id` int NOT NULL,
  `disease_id` int NOT NULL,
  `symptoms` text,
  `treatment` text,
  `medicines` text,
  `prevention` text,
  `diagnosed_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `status` enum('active','recovered') NOT NULL DEFAULT 'active',
  `note` text,
  PRIMARY KEY (`record_id`),
  UNIQUE KEY `record_id` (`record_id`),
  KEY `doctor_id` (`doctor_id`),
  KEY `patient_id` (`patient_id`),
  KEY `disease_id` (`disease_id`),
  CONSTRAINT `medical_history_ibfk_1` FOREIGN KEY (`doctor_id`) REFERENCES `doctor` (`doctor_id`),
  CONSTRAINT `medical_history_ibfk_2` FOREIGN KEY (`patient_id`) REFERENCES `patient` (`patient_id`),
  CONSTRAINT `medical_history_ibfk_3` FOREIGN KEY (`disease_id`) REFERENCES `disease` (`disease_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `medical_history`
--

LOCK TABLES `medical_history` WRITE;
/*!40000 ALTER TABLE `medical_history` DISABLE KEYS */;
/*!40000 ALTER TABLE `medical_history` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `patient`
--

DROP TABLE IF EXISTS `patient`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `patient` (
  `patient_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `height` int NOT NULL,
  `weight` int NOT NULL,
  `lifestyle` text NOT NULL,
  `current_location` text,
  `note` text,
  PRIMARY KEY (`patient_id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `fk_user_patient` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`),
  CONSTRAINT `patient_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `patient`
--

LOCK TABLES `patient` WRITE;
/*!40000 ALTER TABLE `patient` DISABLE KEYS */;
INSERT INTO `patient` VALUES (1,9,66,45,'very messy and dirty','Not Provided','Not Provided'),(2,12,64,45,'lazy','nowhere','Not Provided');
/*!40000 ALTER TABLE `patient` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `specialization`
--

DROP TABLE IF EXISTS `specialization`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `specialization` (
  `spec_id` int NOT NULL AUTO_INCREMENT,
  `spec_name` varchar(30) NOT NULL,
  `spec_desc` text NOT NULL,
  `treats_diseases` text NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `status` enum('verified','unverified','discontinued') NOT NULL DEFAULT 'unverified',
  PRIMARY KEY (`spec_id`),
  UNIQUE KEY `spec_name` (`spec_name`),
  UNIQUE KEY `spec_name_2` (`spec_name`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `specialization`
--

LOCK TABLES `specialization` WRITE;
/*!40000 ALTER TABLE `specialization` DISABLE KEYS */;
INSERT INTO `specialization` VALUES (1,'cardiologist','this is the doctor for heart related problems','coronary artery disease, high blood pressure (hypertension), heart failure, arrhythmias (like atrial fibrillation), and heart attacks','2026-01-27 08:32:01','verified'),(2,'nurology','docotor of brain','memory_loss,internal_dammage to brain,nerves constriction issues ','2026-01-27 09:08:36','unverified'),(3,'endocronology','handles hormonal immbalance ','diabatese','2026-01-27 09:11:51','verified'),(4,'gastrologist','deals with gastic problems','indigestion ','2026-01-27 19:31:20','unverified');
/*!40000 ALTER TABLE `specialization` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `user_name` varchar(20) NOT NULL,
  `email` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` enum('doctor','patient','admin') NOT NULL,
  `age` int NOT NULL,
  `dob` date NOT NULL,
  `current_address` varchar(50) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `status` enum('inactive','active','suspended') NOT NULL DEFAULT 'inactive',
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `email_2` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (2,'tsri','tsri@gmail.com','Hello@1201','admin',23,'2011-09-02','nyaipur config , heloganj ,printnagar,indiput','2026-01-26 09:05:26','inactive'),(3,'test','test@gmail.com','7a6c8c1834e8fc09b82ac75ed232bee701bdebfbb462a621d3440b4deddb9e29','admin',23,'2011-09-01','helonagar,pyragganj,inidana','2026-01-26 20:23:07','inactive'),(5,'doctor_1','dcotor@gmail.com','784e9f183001fad9ee0f8f56abc1493dc1f2a7994d720c96aad134777ecfc9ef','doctor',34,'2022-11-04','not available','2026-01-27 09:07:10','inactive'),(8,'hello','hello@gmail.com','784e9f183001fad9ee0f8f56abc1493dc1f2a7994d720c96aad134777ecfc9ef','admin',34,'2002-09-09','nyaiganj','2026-01-27 17:04:17','inactive'),(9,'patient_2','patient@gmail.com','784e9f183001fad9ee0f8f56abc1493dc1f2a7994d720c96aad134777ecfc9ef','patient',34,'2003-09-09','anynagar','2026-01-27 17:06:57','inactive'),(10,'doctor_2','doctor2@gmail.com','784e9f183001fad9ee0f8f56abc1493dc1f2a7994d720c96aad134777ecfc9ef','doctor',34,'2002-04-03','anywahre','2026-01-27 17:09:21','inactive'),(11,'admin3','admin3@gmail.com','784e9f183001fad9ee0f8f56abc1493dc1f2a7994d720c96aad134777ecfc9ef','admin',45,'2022-12-09','anywahre','2026-01-27 19:52:55','inactive'),(12,'patient5','patient5@gmail.com','784e9f183001fad9ee0f8f56abc1493dc1f2a7994d720c96aad134777ecfc9ef','patient',45,'2001-12-02','nowhare','2026-01-27 19:54:32','inactive');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-01-27 20:10:05
