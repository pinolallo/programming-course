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

    commandsDictionary={
            "h":0,
            "help":0,
            "q":0,
            "quit":0,
            "v":0,
            "verbose":0,
            "c":0,
            "check":0,
            "load":0,
            "l":0,
            "create":constants.MAIN_COMMAND_ARGS
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
    # assert the input 
    # generate command and command arguments
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
    isVerbose=programControlMask & constants.MAIN_VERBOSE
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
        elif command == "c" or  command == "check":
            # set the MAIN_DIE bit of programControlMask
            common.emit(f"databaseDef {tableDef}", constants.PRINT_MESSAGE)
        elif command == "l" or  command == "load":
            common.emit("loading main datasetq", constants.PRINT_MESSAGE)
            mainDb=csvLoader.getDataset()
            databaseDef=mysqlDriver.loadDatabaseDef()
            sqlList=[]
            i=0
            for row in mainDb['db']:
                mainRecordId=row[constants.MAIN_DB_RECORD_ID_INDEX]
                try:
                    sqlList.append(csvLoader.importSqlGeneator(mainDb['header'],row,databaseDef,mainRecordId))
                except:
                    common.emit(f"fail getting sql command for line {i}")        
                i=i+i
          
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
"""
    common.emit(helpText, constants.PRINT_MESSAGE)
