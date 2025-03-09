-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Mar 09, 2025 at 07:34 PM
-- Server version: 8.3.0
-- PHP Version: 8.2.18

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `cricket-league-management`
--

DELIMITER $$
--
-- Procedures
--
DROP PROCEDURE IF EXISTS `add_player_if_role_isplayer`$$
CREATE DEFINER=`root`@`localhost` PROCEDURE `add_player_if_role_isplayer` (IN `p_username` VARCHAR(50), IN `p_password` VARCHAR(255), IN `p_email` VARCHAR(100), IN `p_role` ENUM('player','user'))   BEGIN
    DECLARE user_id INT;

    -- Insert the new user into the users table
    INSERT INTO users (username, password_hash, email, role)
    VALUES (p_username, p_password, p_email, p_role);

    -- Get the last inserted user_id
    SET user_id = LAST_INSERT_ID();

    -- If the role is 'player', insert into the players table
    IF p_role = 'player' THEN
        INSERT INTO players (user_id) VALUES (user_id);
    END IF;
END$$

DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

DROP TABLE IF EXISTS `admin`;
CREATE TABLE IF NOT EXISTS `admin` (
  `admin_id` bigint UNSIGNED NOT NULL AUTO_INCREMENT,
  `admin_username` varchar(50) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  PRIMARY KEY (`admin_id`),
  UNIQUE KEY `admin_id` (`admin_id`),
  UNIQUE KEY `admin_username` (`admin_username`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`admin_id`, `admin_username`, `password_hash`) VALUES
(1, 'admin', '123');

-- --------------------------------------------------------

--
-- Table structure for table `matches`
--

DROP TABLE IF EXISTS `matches`;
CREATE TABLE IF NOT EXISTS `matches` (
  `match_id` bigint UNSIGNED NOT NULL AUTO_INCREMENT,
  `team1_id` int DEFAULT NULL,
  `team2_id` int DEFAULT NULL,
  `match_date` timestamp NOT NULL,
  `status` enum('scheduled','ongoing','completed') DEFAULT 'scheduled',
  `winner_team_id` int DEFAULT NULL,
  PRIMARY KEY (`match_id`),
  UNIQUE KEY `match_id` (`match_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `players`
--

DROP TABLE IF EXISTS `players`;
CREATE TABLE IF NOT EXISTS `players` (
  `player_id` bigint UNSIGNED NOT NULL AUTO_INCREMENT,
  `player_name` varchar(100) NOT NULL,
  `team_id` int DEFAULT NULL,
  `role` enum('batsman','bowler','all-rounder','wicket-keeper') NOT NULL,
  `matches_played` int DEFAULT '0',
  `runs` int DEFAULT '0',
  `wickets` int DEFAULT '0',
  `user_id` int DEFAULT NULL,
  PRIMARY KEY (`player_id`),
  UNIQUE KEY `player_id` (`player_id`),
  UNIQUE KEY `user_id` (`user_id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `players`
--

INSERT INTO `players` (`player_id`, `player_name`, `team_id`, `role`, `matches_played`, `runs`, `wickets`, `user_id`) VALUES
(1, '', NULL, 'batsman', 0, 0, 0, 5);

-- --------------------------------------------------------

--
-- Table structure for table `player_statistics`
--

DROP TABLE IF EXISTS `player_statistics`;
CREATE TABLE IF NOT EXISTS `player_statistics` (
  `stat_id` bigint UNSIGNED NOT NULL AUTO_INCREMENT,
  `match_id` int DEFAULT NULL,
  `player_id` int DEFAULT NULL,
  `runs_scored` int DEFAULT '0',
  `wickets_taken` int DEFAULT '0',
  `balls_faced` int DEFAULT '0',
  `overs_bowled` float DEFAULT '0',
  PRIMARY KEY (`stat_id`),
  UNIQUE KEY `stat_id` (`stat_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `standings`
--

DROP TABLE IF EXISTS `standings`;
CREATE TABLE IF NOT EXISTS `standings` (
  `team_id` int NOT NULL,
  `matches_played` int DEFAULT '0',
  `wins` int DEFAULT '0',
  `losses` int DEFAULT '0',
  `points` int DEFAULT '0',
  PRIMARY KEY (`team_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `teams`
--

DROP TABLE IF EXISTS `teams`;
CREATE TABLE IF NOT EXISTS `teams` (
  `team_id` bigint UNSIGNED NOT NULL AUTO_INCREMENT,
  `team_name` varchar(100) NOT NULL,
  `coach_name` varchar(100) DEFAULT NULL,
  `captain_id` int DEFAULT NULL,
  PRIMARY KEY (`team_id`),
  UNIQUE KEY `team_id` (`team_id`),
  UNIQUE KEY `team_name` (`team_name`),
  UNIQUE KEY `captain_id` (`captain_id`)
) ENGINE=MyISAM AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `teams`
--

INSERT INTO `teams` (`team_id`, `team_name`, `coach_name`, `captain_id`) VALUES
(1, 'Dadar Daredevils', 'Santosh Pawar', NULL),
(2, 'Andheri Avengers', 'Ramesh Patil', NULL),
(3, 'Bandra Blasters', 'Suhas Desai', NULL),
(4, 'Thane Thunderbolts', 'Ganesh Jadhav', NULL),
(5, 'Borivali Braves', 'Nitin Naik', NULL),
(6, 'Chembur Chargers', 'Vikas More', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
CREATE TABLE IF NOT EXISTS `users` (
  `user_id` bigint UNSIGNED NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `email` varchar(100) NOT NULL,
  `role` enum('player','user') NOT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `user_id` (`user_id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`)
) ENGINE=MyISAM AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`user_id`, `username`, `password_hash`, `email`, `role`) VALUES
(1, 'soham', '123', 'soham@gmail.com', 'user'),
(2, 'aa', 'aaa', 'aaa', 'player'),
(3, 'qqq', 'qqq', 'qqq', 'player'),
(4, '1111', '111', '1111', 'player'),
(5, 'soham1', '123', 'sohamlohote@gmail.com', 'player');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
