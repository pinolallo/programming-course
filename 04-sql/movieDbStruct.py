import commons
import constants
DB_NAME = 'movieDb'
TABLES = {}
TABLES['movies'] = (
    "CREATE TABLE `movies` ("
    "  `movie_id` int(11),"
    "  `movie_name` varchar(256) NOT NULL ,"
    "  `movie_title` varchar(256) NOT NULL,"
    "  `movie_keywords` varchar(256) NOT NULL,"
    "  `movie_HomePage` varchar(128) NOT NULL,"
    "  `movie_original_lang` varchar(2) NOT NULL,"
    "  `movie_overview` text NOT NULL,"
    "  `movie_popularity` FLOAT NOT NULL,"
    "  `movie_relase` date NOT NULL,"
    "  `movie_runtime` int(11) NOT NULL,"
    "  `movie_tagline` varchar(128) NOT NULL,"
    "  `movie_cast` varchar(256) NOT NULL,"
    "  `movie_vote_num`int(11) NOT NULL,"
     " `movie_vote_average`int(11) NOT NULL,"
    "  PRIMARY KEY (`movie_id`)"
    ") ENGINE=InnoDB")
TABLES['people'] = (
    "CREATE TABLE `people` ("
    "  `people_id` int(11),"
    "  `people_name` varchar(256) NOT NULL,"
    "  `people_gender` enum('M','F') NOT NULL,"
    "  PRIMARY KEY (`people_id`)"
    ") ENGINE=InnoDB")
TABLES['jobs'] = (
    "CREATE TABLE `jobs` ("
    "  `job_id` int(11),"
    "  `job_name` varchar(128) NOT NULL,"
    "  `job_department` varchar(128) NOT NULL,"
    "   PRIMARY KEY (`job_id`)"
    ") ENGINE=InnoDB")
TABLES['movie_jobs'] = (
    "CREATE TABLE `movie_jobs` ("
    "  `job_id` int(11),"
    "  `movie_id` int(11) NOT NULL,"
    "   PRIMARY KEY (`job_id`)"
    "   KEY `movie_id` (`movie_id`),"
    ") ENGINE=InnoDB")
TABLES['productions'] = (
    "CREATE TABLE `productions` ("
    "  `prod_id` int(11),"
    "  `prod_name` varchar(128) NOT NULL,"
    "  `job_department` varchar(128) NOT NULL,"
    "  PRIMARY KEY (`prod_id`)"
    ") ENGINE=InnoDB")
TABLES['countries'] = (
    "CREATE TABLE `countries` ("
    "  `country_id` varchar(2) not null,"
    "  `country_name` varchar(256) not null,"
    "   PRIMARY KEY (`prod_id`)"
    ") ENGINE=InnoDB")
TABLES['movie_productions'] = (
    "CREATE TABLE `movie_prod` ("
    "  `prod_id` int(11),"
    "  `movie_id` int(11),"
    "   PRIMARY KEY (`prod_id`)"
    "   KEY `movie_id` (`movie_id`),"
    ") ENGINE=InnoDB")
TABLES['language'] = (
    "CREATE TABLE `lang` ("
    "  `lang_id` varchar(2) NOT NULL,"
    "  `lang_eng_name` varchar(128) NOT NULL,"
    "  `lang_name` varchar(128) NOT NULL,"
    "   PRIMARY KEY (`lang_id`)"
    ") ENGINE=InnoDB")
TABLES['movie_language'] = (
    "CREATE TABLE `lang` ("
    "  `lang_id` varchar(2) NOT NULL,"
    "  `movie_id` int(11)  NOT NULL,"
    "   PRIMARY KEY (`lang_id`)"
    "   KEY `movie_id` (`movie_id`),"
    ") ENGINE=InnoDB")

def create_database(cursor):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        commons.emit("Failed creating database: {}".format(err),constants.PRINT_MESSAGE+constants.LOG_TO_SYSLOG)
        exit(1)
