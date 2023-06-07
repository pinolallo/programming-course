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

create database movieDb IF NOT EXISTS DEFAULT CHARACTER SET 'utf8';
use movieDb;

drop table if exists movies;
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
     
  drop table if exists people;
  CREATE TABLE `people` ( 
       `people_id` int(11), 
       `people_name` varchar(256) NOT NULL, 
       `people_gender` enum('M','F') NOT NULL, 
       PRIMARY KEY (`people_id`) 
     ) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='crew of movie_dataset';
    
    drop table if exists people_jobs;
    CREATE TABLE `people_jobs` ( 
       `people_id` int(11), 
       `job_id` int(11) NOT NULL, 
        KEY `people_id` (`people_id`),
        KEY `job_id` (`job_id`)
     ) ENGINE=InnoDB COMMENT='people jobs relation table';
     
    drop table if exists jobs;
    CREATE TABLE `jobs` ( 
       `job_id` int(11), 
       `job_name` varchar(128) NOT NULL, 
       `job_department` varchar(128) NOT NULL, 
        PRIMARY KEY (`job_id`) 
     ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='jobs of movie_dataset';
         
	 drop table if exists movie_jobs;
     CREATE TABLE `movie_jobs` ( 
       `job_id` int(11), 
       `movie_id` int(11) NOT NULL, 
        KEY `job_id` (`job_id`), 
        KEY `movie_id` (`movie_id`) 
     ) ENGINE=InnoDB COMMENT='movie jobs relation table';
    
    drop table if exists productions;
    CREATE TABLE `productions` ( 
       `prod_id` int(11), 
       `prod_name` varchar(128) NOT NULL, 
       PRIMARY KEY (`prod_id`) 
     ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='productions company';
     
     drop table if exists movie_productions;
     CREATE TABLE `movie_productions` ( 
       `prod_id` int(11), 
       `movie_id` int(11) NOT NULL, 
        KEY `prod_id` (`prod_id`),
        KEY `movie_id` (`movie_id`)
     ) ENGINE=InnoDB COMMENT='movie production relation table';
    
    drop table if exists countries;
    CREATE TABLE `countries` ( 
       `country_id` varchar(2) not null, 
       `country_name` varchar(256) not null, 
        PRIMARY KEY (`country_id`) 
     ) ENGINE=InnoDB COMMENT='iso_3166_1 countries code';
     
      drop table if exists movie_countries;
      CREATE TABLE `movie_countries` ( 
       `movie_id` varchar(2) not null, 
       `country_id` varchar(256) not null, 
        KEY (`movie_id`),
        KEY (`country_id`) 
     ) ENGINE=InnoDB COMMENT='movie languages relation table';

    drop table if exists languages;
    CREATE TABLE `languages` ( 
       `lang_id` varchar(2) not null, 
       `lang_name` varchar(256) not null, 
        PRIMARY KEY (`lang_id`)
     ) ENGINE=InnoDB COMMENT='iso_3166_1 countries code';
     
    drop table if exists movie_lang;
    CREATE TABLE `movie_lang` ( 
       `movie_id` varchar(2) not null, 
       `lang_id` varchar(256) not null, 
        KEY (`movie_id`),
        KEY (`lang_id`) 
     ) ENGINE=InnoDB COMMENT='movie languages relation table';

     CREATE USER IF NOT EXISTS 'dbUser'@'%' IDENTIFIED BY 'cippalippa';

     GRANT ALL ON movieDb.* to 'dbUser'@'%';