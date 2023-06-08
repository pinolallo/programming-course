"""
********************************************************
*  __          __                                      *
* / /____ ___ / /_  ___  _______  ___ ________ ___ _   *
*/ __/ -_|_-</ __/ / _ \/ __/ _ \/ _ `/ __/ _ `/  ' \  *
*\__/\__/___/\__/ / .__/_/  \___/\_, /_/  \_,_/_/_/_/  *
*                /_/            /___/                  *
* v 1.1 written by Silvestro "pino" Di Pietro 2023     *
* the constants declarations file to be included       *
*                                                      *
* written by Silvestro 'pino' Di Pietro                *
********************************************************
"""
#main controls bits
MAIN_DIE=1
MAIN_CHECK=2
MAIN_VERBOSE=4

MAIN_COMMAND_DATA=1
MAIN_COMMAND_ARGS=2


#emit control bits declaration
PRINT_MESSAGE=1
LOG_TO_SDIO=2
LOG_TO_SYSLOG=4
LOG_TO_EMAIL=8

#configuration defines
SYSLOG_FILENAME="pythonTest.log"
SYSLOG_LEVEL="DEBUG"

#configs for hash table
MIN_TABLE_SIZE=10
MAX_TABLE_SIZE=100
SAVED_DATA_FILENAME='savedTable.json'


#mysql connection config
MAIN_DB_TABLE='movies'
MAIN_DB_RECORD_ID_INDEX=4
mysqlConfig={
    'user'  : 'pinolallo',
    'password':'cippalippa',
    'host':'localhost',
    'database':'movieDb',
    'port':3306
}

