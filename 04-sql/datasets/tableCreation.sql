/*
********************************************************
                  _     ___  __             __
  __ _  ___ _  __(_)__ / _ \/ /    ___ ___ / /___ _____
 /  ' \/ _ \ |/ / / -_) // / _ \  (_-</ -_) __/ // / _ \
/_/_/_/\___/___/_/\__/____/_.__/ /___/\__/\__/\_,_/ .__/
                                                 /_/
* written by Silvestro 'pino' Di Pietro
  sql relational structure to be filled with the parsed
  movie_dataset.csv
********************************************************
*/
drop database movieDb;
create database movieDb  DEFAULT CHARACTER SET 'utf8';
CREATE USER IF NOT EXISTS 'dbUser'@'%' IDENTIFIED  BY 'cippalippa';
GRANT ALL ON movieDb.* to 'dbUser'@'%';
use movieDb;
     CREATE TABLE `movies` ( 
       `movie_id` int(11), 
       `movie_name` varchar(256) NOT NULL , 
       `movie_title` varchar(256) NOT NULL, 
       `movie_original_title` varchar(256) NOT NULL, 
       `movie_genres` varchar(256) NOT NULL, 
       `movie_HomePage` varchar(128) NOT NULL, 
       `movie_keywords` varchar(256) NOT NULL, 
       `movie_budget` int(11) NOT NULL, 
       `movie_original_lang` varchar(2) NOT NULL, 
       `movie_overview` text NOT NULL, 
       `movie_popularity` FLOAT NOT NULL, 
       `movie_relase` date NOT NULL, 
       `movie_revenue`int(11) NOT NULL, 
       `movie_runtime` int(11) NOT NULL, 
       `movie_tagline` varchar(128) NOT NULL, 
       `movie_cast` varchar(256) NOT NULL, 
       `movie_vote_num`int(11) NOT NULL, 
       `movie_vote_average`int(11) NOT NULL, 
       PRIMARY KEY (`movie_id`) 
     ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='movie_dataset';
     
    CREATE TABLE `credits` ( 
      `credit_id` int(11),
      `people_name` varchar(256) NOT NULL, 
      `people_gender` enum('M','F') NOT NULL, 
      `job_name` varchar(128) NOT NULL, 
      `job_department` varchar(128) NOT NULL, 
      `movie_id` int(11),
      PRIMARY KEY (`credit_id`),
      KEY `movie_id` (`movie_id`) 
     ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='jobs of movie_dataset';
       
      CREATE TABLE `productions` (
       `id` int(11) NOT NULL auto_increment,
       `prod_id` int(11),
       `prod_name`  varchar(128) not null,
       `movie_id` int(11),
        PRIMARY KEY (`id`), 
        KEY (`prod_id`),
        KEY (`prod_name`),
        KEY (`movie_id`) 
     ) ENGINE=InnoDB COMMENT='movie productions';

      CREATE TABLE `countries` ( 
       `id` int(11) NOT NULL auto_increment,
       `country_name`  varchar(128) not null,
       `movie_id` int(11),
       `country_id` varchar(2) not null,
        PRIMARY KEY (`id`), 
        KEY (`movie_id`),
        KEY (`country_id`) 
     ) ENGINE=InnoDB COMMENT='movie languages relation table';

    CREATE TABLE `languages` (
       `id` int(11) NOT NULL auto_increment, 
       `movie_id` int(11),
       `lang_id` varchar(2) not null, 
        PRIMARY KEY (`id`),
        KEY (`movie_id`),
        KEY (`lang_id`) 
     ) ENGINE=InnoDB COMMENT='movie languages relation table';
