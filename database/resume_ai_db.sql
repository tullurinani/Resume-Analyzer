-- phpMyAdmin SQL Dump
-- version 4.0.4
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Jul 05, 2025 at 11:29 AM
-- Server version: 5.6.12-log
-- PHP Version: 5.4.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `resume_ai_db`
--
CREATE DATABASE IF NOT EXISTS `resume_ai_db` DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci;
USE `resume_ai_db`;

-- --------------------------------------------------------

--
-- Table structure for table `analyzerapp_candidate`
--

CREATE TABLE IF NOT EXISTS `analyzerapp_candidate` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `email` varchar(254) NOT NULL,
  `phone` varchar(15) NOT NULL,
  `address` longtext NOT NULL,
  `state` varchar(50) NOT NULL,
  `password` varchar(100) NOT NULL,
  `resume_file` varchar(100) DEFAULT NULL,
  `interview_video` varchar(100) DEFAULT NULL,
  `score` double NOT NULL,
  `status` varchar(20) NOT NULL,
  `submitted_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=5 ;

--
-- Dumping data for table `analyzerapp_candidate`
--

INSERT INTO `analyzerapp_candidate` (`id`, `name`, `email`, `phone`, `address`, `state`, `password`, `resume_file`, `interview_video`, `score`, `status`, `submitted_at`) VALUES
(1, 'manu', 'manu@gmail.com', '07896541230', 'hyd', '', '123', '', 'media/interviews/interview_1_J4Jli40.webm', 10, 'Rejected', '2025-07-05 09:44:42.268835'),
(2, 'Vali', 'vali@gmail.com', '09876543210', 'hyd', '', '123', '', 'media/interviews/interview_2.webm', 27, 'Rejected', '2025-07-05 10:02:20.938847'),
(4, 'shaik', 'shaik@gmail.com', '7896541231', 'Hyderbad', '', '123', '', 'media/interviews/interview_4.webm', 84, 'Accepted', '2025-07-05 11:20:42.291438');

-- --------------------------------------------------------

--
-- Table structure for table `analyzerapp_candidate1`
--

CREATE TABLE IF NOT EXISTS `analyzerapp_candidate1` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `email` varchar(254) NOT NULL,
  `phone` varchar(15) NOT NULL,
  `address` longtext NOT NULL,
  `state` varchar(50) NOT NULL,
  `password` varchar(100) NOT NULL,
  `status` varchar(20) NOT NULL,
  `score` double NOT NULL,
  `interview_video` varchar(100) DEFAULT NULL,
  `submitted_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `analyzerapp_interview`
--

CREATE TABLE IF NOT EXISTS `analyzerapp_interview` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `questions` longtext NOT NULL,
  `video_file` varchar(100) DEFAULT NULL,
  `communication_score` int(11) NOT NULL,
  `relevance_score` int(11) NOT NULL,
  `confidence_score` int(11) NOT NULL,
  `total_score` double NOT NULL,
  `status` varchar(20) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `analyzerapp_interview_user_id_0d11135f_fk_auth_user_id` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `analyzerapp_resume`
--

CREATE TABLE IF NOT EXISTS `analyzerapp_resume` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `resume_file` varchar(100) NOT NULL,
  `uploaded_at` datetime(6) NOT NULL,
  `candidate_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `analyzerapp_resume_candidate_id_429293cb_fk_analyzera` (`candidate_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=4 ;

--
-- Dumping data for table `analyzerapp_resume`
--

INSERT INTO `analyzerapp_resume` (`id`, `resume_file`, `uploaded_at`, `candidate_id`) VALUES
(1, 'resumes/uploaded\\python exp_IUq5WEY.pdf', '2025-07-05 09:54:45.064595', 1),
(2, 'resumes/uploaded\\Sanju Resume_TfPe15q.pdf', '2025-07-05 10:04:12.264581', 2),
(3, 'resumes/uploaded\\Vali Python Trainer.pdf', '2025-07-05 11:21:45.061000', 4);

-- --------------------------------------------------------

--
-- Table structure for table `auth_group`
--

CREATE TABLE IF NOT EXISTS `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group_permissions`
--

CREATE TABLE IF NOT EXISTS `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `auth_permission`
--

CREATE TABLE IF NOT EXISTS `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=41 ;

--
-- Dumping data for table `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can view log entry', 1, 'view_logentry'),
(5, 'Can add permission', 2, 'add_permission'),
(6, 'Can change permission', 2, 'change_permission'),
(7, 'Can delete permission', 2, 'delete_permission'),
(8, 'Can view permission', 2, 'view_permission'),
(9, 'Can add group', 3, 'add_group'),
(10, 'Can change group', 3, 'change_group'),
(11, 'Can delete group', 3, 'delete_group'),
(12, 'Can view group', 3, 'view_group'),
(13, 'Can add user', 4, 'add_user'),
(14, 'Can change user', 4, 'change_user'),
(15, 'Can delete user', 4, 'delete_user'),
(16, 'Can view user', 4, 'view_user'),
(17, 'Can add content type', 5, 'add_contenttype'),
(18, 'Can change content type', 5, 'change_contenttype'),
(19, 'Can delete content type', 5, 'delete_contenttype'),
(20, 'Can view content type', 5, 'view_contenttype'),
(21, 'Can add session', 6, 'add_session'),
(22, 'Can change session', 6, 'change_session'),
(23, 'Can delete session', 6, 'delete_session'),
(24, 'Can view session', 6, 'view_session'),
(25, 'Can add candidate', 7, 'add_candidate'),
(26, 'Can change candidate', 7, 'change_candidate'),
(27, 'Can delete candidate', 7, 'delete_candidate'),
(28, 'Can view candidate', 7, 'view_candidate'),
(29, 'Can add candidate1', 8, 'add_candidate1'),
(30, 'Can change candidate1', 8, 'change_candidate1'),
(31, 'Can delete candidate1', 8, 'delete_candidate1'),
(32, 'Can view candidate1', 8, 'view_candidate1'),
(33, 'Can add interview', 9, 'add_interview'),
(34, 'Can change interview', 9, 'change_interview'),
(35, 'Can delete interview', 9, 'delete_interview'),
(36, 'Can view interview', 9, 'view_interview'),
(37, 'Can add resume', 10, 'add_resume'),
(38, 'Can change resume', 10, 'change_resume'),
(39, 'Can delete resume', 10, 'delete_resume'),
(40, 'Can view resume', 10, 'view_resume');

-- --------------------------------------------------------

--
-- Table structure for table `auth_user`
--

CREATE TABLE IF NOT EXISTS `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `auth_user_groups`
--

CREATE TABLE IF NOT EXISTS `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `auth_user_user_permissions`
--

CREATE TABLE IF NOT EXISTS `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `django_admin_log`
--

CREATE TABLE IF NOT EXISTS `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `django_content_type`
--

CREATE TABLE IF NOT EXISTS `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=11 ;

--
-- Dumping data for table `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(7, 'analyzerapp', 'candidate'),
(8, 'analyzerapp', 'candidate1'),
(9, 'analyzerapp', 'interview'),
(10, 'analyzerapp', 'resume'),
(3, 'auth', 'group'),
(2, 'auth', 'permission'),
(4, 'auth', 'user'),
(5, 'contenttypes', 'contenttype'),
(6, 'sessions', 'session');

-- --------------------------------------------------------

--
-- Table structure for table `django_migrations`
--

CREATE TABLE IF NOT EXISTS `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=20 ;

--
-- Dumping data for table `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2025-07-05 09:41:17.159270'),
(2, 'auth', '0001_initial', '2025-07-05 09:41:18.157218'),
(3, 'admin', '0001_initial', '2025-07-05 09:41:18.399585'),
(4, 'admin', '0002_logentry_remove_auto_add', '2025-07-05 09:41:18.411474'),
(5, 'admin', '0003_logentry_add_action_flag_choices', '2025-07-05 09:41:18.428282'),
(6, 'analyzerapp', '0001_initial', '2025-07-05 09:41:19.011788'),
(7, 'contenttypes', '0002_remove_content_type_name', '2025-07-05 09:41:19.164979'),
(8, 'auth', '0002_alter_permission_name_max_length', '2025-07-05 09:41:19.251726'),
(9, 'auth', '0003_alter_user_email_max_length', '2025-07-05 09:41:19.331666'),
(10, 'auth', '0004_alter_user_username_opts', '2025-07-05 09:41:19.349531'),
(11, 'auth', '0005_alter_user_last_login_null', '2025-07-05 09:41:19.424466'),
(12, 'auth', '0006_require_contenttypes_0002', '2025-07-05 09:41:19.438791'),
(13, 'auth', '0007_alter_validators_add_error_messages', '2025-07-05 09:41:19.470449'),
(14, 'auth', '0008_alter_user_username_max_length', '2025-07-05 09:41:19.550289'),
(15, 'auth', '0009_alter_user_last_name_max_length', '2025-07-05 09:41:19.636143'),
(16, 'auth', '0010_alter_group_name_max_length', '2025-07-05 09:41:19.726553'),
(17, 'auth', '0011_update_proxy_permissions', '2025-07-05 09:41:19.756426'),
(18, 'auth', '0012_auto_20250629_0614', '2025-07-05 09:41:19.839095'),
(19, 'sessions', '0001_initial', '2025-07-05 09:41:19.931489');

-- --------------------------------------------------------

--
-- Table structure for table `django_session`
--

CREATE TABLE IF NOT EXISTS `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `analyzerapp_interview`
--
ALTER TABLE `analyzerapp_interview`
  ADD CONSTRAINT `analyzerapp_interview_user_id_0d11135f_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `analyzerapp_resume`
--
ALTER TABLE `analyzerapp_resume`
  ADD CONSTRAINT `analyzerapp_resume_candidate_id_429293cb_fk_analyzera` FOREIGN KEY (`candidate_id`) REFERENCES `analyzerapp_candidate` (`id`);

--
-- Constraints for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Constraints for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Constraints for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
