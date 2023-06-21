import sys
sys.path.append('../00-commons')
import common
import constants
import csvLoader
import mysqlDriver
import re
if __name__ == '__main__':
    main()


def main():
    global programControlMask
    global commandsDictionary
    global tableDef
    global mainDb
    global sqlResult
    commandsDictionary={
            "h":0,
            "help":0,
            "q":0,
            "quit":0,
            "v":0,
            "verbose":0,
            "p":0,
            "parse":0,
            "l":0,
            "load":0,
            "s":0,
            "save":0,
            "d":0,
            "describe":0
        }
    try:
        programControlMask
    except:
        # this except will contain the inititalization of the program
        programControlMask = 0
        try:
            # verify if can create a db connection
            common.emit("starting app ")
            tableDef=mysqlDriver.loadDatabaseDef()
      
        except Exception as Error:
            common.emit(Error, constants.LOG_TO_SDIO+constants.PRINT_MESSAGE)
            sys.exit()
        # ok
        common.emit("welcome to sqlApp, type h for help",constants.PRINT_MESSAGE)
    # get the input    
    dataInput = input("sqlApp> ")
    canExec=True
    hasTable=True
    try:
        mainDb
    except:
        hasTable=False
    # assert the input 
    # generate command and command arguments (splitting in words)
    theInput=dataInput.split(" ")
    inputWordsNumber=len(theInput)
    argumentslist=[]
    verbose=programControlMask & constants.MAIN_VERBOSE

    i=0
    for entry in theInput:
        if i == 0:
            command=entry.lower()
        else:
            argumentslist.append(entry)
        i+=1
    argument=" ".join(argumentslist)
    #check if is a valid command 
    try:
        commandsDictionary[command]
    except:
        common.emit(f"command ({command}) not recognized",constants.LOG_TO_SYSLOG+constants.PRINT_MESSAGE)
        canExec=False
    #check if command can be run
    else:
        if  commandsDictionary[command] & constants.MAIN_COMMAND_ARGS:
            if inputWordsNumber == 1:
                common.emit(f"command ({command}) need arguments")
                canExec=False
    #run the command
    verbose=programControlMask & constants.MAIN_VERBOSE
    if canExec:
        #print help
        if command == "h" or  command == "help":
            # run help
            printHelp()
            
        #exit program
        elif command == "q" or  command == "quit":
            # set the MAIN_DIE bit of programControlMask
            programControlMask += constants.MAIN_DIE
            common.emit("bye bye", constants.PRINT_MESSAGE)
            sys.exit()
        elif command == "v" or  command == "verbose":
            ## check before set
            if  programControlMask & constants.MAIN_VERBOSE:
                programControlMask -=constants.MAIN_VERBOSE
                common.emit(f"verbose mode turned off")
            else:
                programControlMask +=constants.MAIN_VERBOSE
                common.emit(f"verbose mode turned on")
        elif command == "l" or  command == "load":
            common.emit("loading main datasetq", constants.PRINT_MESSAGE)
            mainDb=csvLoader.getDataset()
            if verbose:
                display=[]
                display.append({'parsed fields':len(mainDb['header']),'tot entries':len(mainDb['db'])})
                common.emit(common.makeAsciiTable(display))
                conversionTable=makeConversionTable(mainDb['conversionDictionary'])
                common.emit(common.makeAsciiTable(conversionTable))
        #describe
        elif command == 'd' or command == "describe":
            if hasTable:
                display=[]
                display.append({'parsed fields':len(mainDb['header']),'tot entries':len(mainDb['db'])})
                common.emit(common.makeAsciiTable(display))
                display=makeConversionTable(mainDb['conversionDictionary'])
                common.emit(common.makeAsciiTable(display))
                for tableName,fieldDef in tableDef.items():
                    common.emit(f"\t{tableName}:")
                    display=[]
                    for fieldName, fieldDefinition in fieldDef.items():
                           display.append(fieldDefinition)
                    common.emit(common.makeAsciiTable(display))
            else:
                common.emit(f"Cannot describe: no loaded dataset (use l(load) to fix)")

        #save file
        elif command == 's' or command == "save":
            sqlResult=[]
            if inputWordsNumber==1:
                fileName=constants.SAVED_SQL_FILENAME
                common.emit(f"saving as default {constants.SAVED_SQL_FILENAME}",constants.LOG_TO_SYSLOG+constants.PRINT_MESSAGE)
            else:
                fileName=argument

            if not hasTable:
                common.emit(f" cannot Save ({fileName}) because no loaded data",constants.LOG_TO_SYSLOG+constants.PRINT_MESSAGE)
            else:
                i=0
                sqlelements=[]
                for row in mainDb['db']:
                    sql=[]
                    mainRecordId=row[constants.MAIN_DB_RECORD_ID_INDEX]
                    try:
                        sql=csvLoader.importSqlGeneator(mainDb['header'],row,mainRecordId,sqlelements)
                    except Exception as theError:
                        common.emit(f"fail getting sql command for line {i} because {theError}")
                    sqlResult=mergeList(sqlResult,sql)
                    i=i+1
            try:
                saveSql("\n".join(sqlResult),fileName)
            except Exception as theError:
                common.emit(f"fail saving {fileName} because {theError}")   
    main()




    

def printHelp():
    helpText = """
                  _     ___  __               __  __
  __ _  ___ _  __(_)__ / _ \/ /    ___  __ __/ /_/ /  ___  ___
 /  ' \/ _ \ |/ / / -_) // / _ \  / _ \/ // / __/ _ \/ _ \/ _ \\
/_/_/_/\___/___/_/\__/____/_.__/ / .__/\_, /\__/_//_/\___/_//_/
                                /_/   /___/
                       __  __             __
  __ _  __ _____ ___ _/ / / /__  ___ ____/ /__ ____
 /  ' \/ // (_-</ _ `/ / / / _ \/ _ `/ _  / -_) __/
/_/_/_/\_, /___/\_, /_/ /_/\___/\_,_/\_,_/\__/_/
      /___/      /_/                                 
v 1.1 written by Silvestro "pino" Di Pietro 2023     
a python simple example of database parsing/creation.        
written by Silvestro 'pino' Di Pietro                
in this lesson:
    * learn how manage the python mysql cursor
    * disassemble information root to create a relational sql database
    * manage a csv without using

commands:
   h help               print this help
   create               will init/create a new database set
   v verbose            will set the verbosity
   q quit               will end the program
   l load               will load the default dataset(movie_dataset.csv)
   s save   filename    will save the sql commands list from parsed dataset
   d describe           will output the sql table and the conversion action
"""
    common.emit(helpText, constants.PRINT_MESSAGE)


def saveSql(sql,fileName=None):
    if not fileName:
        fileName=constants.SAVED_SQL_FILENAME
    with open(fileName, 'w') as file:
        file.write(sql)


def mergeList(lst1, lst2):
    for i in lst2:
        lst1.append(i)
    return lst1

def makeConversionTable(conversionDictionary):
    display=[]
    for field, action in conversionDictionary.items():
        if action=='null':
            action='no action'
        res=re.search("(.*?)\((.*?)\)",action)
        if  res == None:
            continue
        functionName=res.group(1)
        functionArgument=res.group(2)
        display.append({'field':field,'pseudoFuntion':functionName,'argument':functionArgument})
    return display