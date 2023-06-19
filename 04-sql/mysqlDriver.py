import sys
sys.path.append('../00-commons')
import common
import constants
import sys
import  mysql.connector
import re

def initDb():
    try:
        connector  = mysql.connector.connect(**constants.mysqlConfig)
    except mysql.connector as errMsg:
        common.emit(errMsg,constants.LOG_TO_SYSLOG+constants.PRINT_MESSAGE)
    return connector.cursor()



def loadDatabaseDef():
    '''Will read the datasets/tableCreation.sql 
        and using the connection defined id ../commons/constants.py
        will load the tables definition created
    '''
    try:
        connector  = mysql.connector.connect(**constants.mysqlConfig)
    except mysql.connector as errMsg:
        common.emit(errMsg,constants.LOG_TO_SYSLOG+constants.PRINT_MESSAGE)
    else:
        cursor = connector.cursor()
    # check database table definitions
    with open('datasets/tableCreation.sql','r') as tableDef:
        tableDefToParse=tableDef.read()
    #use regular expression to get the table name
    parsed=re.findall('CREATE TABLE `(.*?)`',tableDefToParse)
    #create list from results
    tables = [line.rstrip('\n') for line in parsed]
    
    TableDef={}
    for table in tables:
        sql="desc "+table
        cursor.execute(sql)
        result = cursor.fetchall()
        #TableDef[table]={}
        TableDef[table]={}
        #TableDef[table].append({})
        for fields in result:
            TableDef[table][fields[0]]={}
            TableDef[table][fields[0]]['fieldName']=fields[0]
            cippa=re.findall("(.*?)\(",fields[1].decode())
            if cippa:
                TableDef[table][fields[0]]['fieldType']=cippa[0]
            else:
                TableDef[table][fields[0]]['fieldType']=fields[1].decode()
            TableDef[table][fields[0]]['fieldKey']=fields[3]
            #TableDef[table].append({})
                                           
    return TableDef