"""
********************************************************
*    __            __ ______     __   __               *
*   / /  ___ ____ / //_  __/__ _/ /  / /__ ___         *
*  / _ \/ _ `(_-</ _ \/ / / _ `/ _ \/ / -_|_-<         *
* /_//_/\_,_/___/_//_/_/  \_,_/_.__/_/\__/___/         *
* v 1.1 written by Silvestro "pino" Di Pietro 2023     *
* a python simple explanation for hashTabling.         *
* written by Silvestro 'pino' Di Pietro                *
********************************************************
"""
import sys
sys.path.append('../00-commons')
import common
import constants
import sys
import json
from hashClass import HashTable


def main():
    global programControlMask, theTable, commandsDictionary
    # initialization
    # the first run can be detected by checking if programControlMask exists
    try:
        programControlMask
    except:
        # this except will contain the inititalization of the program
        programControlMask = 0
        try:
            # verify if can write into logFile
            common.emit("hashTable program Started", constants.LOG_TO_SYSLOG)
        except Exception as Error:
            common.emit(Error, constants.LOG_TO_SDIO)
            # set the MAIN_DIE bit of programControlMask
            sys.exit()
        # start program
        common.emit("welcome to hashTable, type h for help",constants.PRINT_MESSAGE)
        '''
            MAIN_COMMAND_DATA=1
            MAIN_COMMAND_ARGS=2
        '''
        commandsDictionary={
            "h":0,
            "help":0,
            "q":0,
            "quit":0,
            "v":0,
            "verbose":0,
            "pr":constants. MAIN_COMMAND_DATA,
            "print":constants. MAIN_COMMAND_DATA,
            "pd":constants. MAIN_COMMAND_DATA,
            "pd":constants. MAIN_COMMAND_DATA,
            "printdictionary":constants. MAIN_COMMAND_DATA,
            "c":constants.MAIN_COMMAND_ARGS,
            "create":constants.MAIN_COMMAND_ARGS,
            "l":0,
            "load":0,
            "s":constants. MAIN_COMMAND_DATA,
            "save":constants. MAIN_COMMAND_DATA+constants.MAIN_COMMAND_ARGS,
            "p":constants. MAIN_COMMAND_DATA+constants.MAIN_COMMAND_ARGS,
            "put":constants. MAIN_COMMAND_DATA+constants.MAIN_COMMAND_ARGS,
            "g":constants. MAIN_COMMAND_DATA+constants.MAIN_COMMAND_ARGS,
            "get": constants. MAIN_COMMAND_DATA+constants.MAIN_COMMAND_ARGS,
            "d":constants. MAIN_COMMAND_DATA+constants.MAIN_COMMAND_ARGS,
            "del": constants. MAIN_COMMAND_DATA+constants.MAIN_COMMAND_ARGS,
            'gh': constants. MAIN_COMMAND_DATA+constants.MAIN_COMMAND_ARGS,

        }

    # get the input    
    dataInput = input("hash> ")

    # assert the input 
    # generate command and command arguments
    theInput=dataInput.split(" ")
    inputWordsNumber=len(theInput)
    argumentslist=[]
    i=0
    for entry in theInput:
        if i == 0:
            command=entry.lower()
        else:
            argumentslist.append(entry)
        i+=1
    argument=" ".join(argumentslist)
    

    # assert tableStatus and exec
    # can execute flag set
    hasTable=True
    canExec=True
    verbose=programControlMask & constants.MAIN_VERBOSE
    #check if there is a table (see global)
    try:
        theTable
    except:
        hasTable=False
    else:
        tableSize=len(theTable.table)

    #check if is a valid command 
    try:
        commandsDictionary[command]
    except:
        common.emit(f"command ({command}) not recognized",constants.LOG_TO_SYSLOG+constants.PRINT_MESSAGE)
        canExec=False

    #check if command can be run
    else:
        if commandsDictionary[command] & constants. MAIN_COMMAND_DATA:
            if not hasTable:
                common.emit("the hash table is not initialized, please create table with size",constants.LOG_TO_SYSLOG+constants.PRINT_MESSAGE)
                canExec=False
        if  commandsDictionary[command] & constants.MAIN_COMMAND_ARGS:
            if inputWordsNumber == 1:
                common.emit(f"command ({command}) need arguments")
                canExec=False

    #run the command
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

        #load table from file
        elif command == 'l' or command == "load":
            if not hasTable:
                theTable=HashTable()
            if inputWordsNumber==1:
                fileName=constants.SAVED_DATA_FILENAME
                common.emit(f"loading default {constants.SAVED_DATA_FILENAME}",constants.LOG_TO_SYSLOG+constants.PRINT_MESSAGE)
            else:
                fileName=argument
            try:
                loadedTable=loadTable(fileName)
            except Exception as theError:
                common.emit(f" failed to load data ({fileName}) {theError}",constants.LOG_TO_SYSLOG+constants.PRINT_MESSAGE)
            else:
                theTable.table=loadedTable
                common.emit(f" table data ({fileName}) loaded",constants.LOG_TO_SYSLOG+constants.PRINT_MESSAGE)

        #print the hashtable
        elif  command == "pr" or  command == "print":
            i=0
            printMe=[]
            for tableEntry in theTable.table:
                if tableEntry:
                    printElement=[]
                    #table entry is a list so we need to render it as string
                    for idx, element in enumerate(tableEntry):
                        printElement.append(f"k({idx}):"+element[0]+" v:"+element[1])
                        tableEntry=" | ".join(printElement)
                    printMe.append({'index':i,'value':tableEntry})
                else:
                    printMe.append({'index':i,'value':''})
                i +=1
            try:
                common.emit(common.makeAsciiTable(printMe))
            except Exception as theError:
                common.emit(f" {theError} ",constants.LOG_TO_SYSLOG+constants.PRINT_MESSAGE)

        #print the resulting dictionary
        elif command == "pd" or  command == "printdictionary":
            printDictionary(theTable.table);
        
        #put/update an entry into the hashtable
        elif command == "p" or  command == "put":
            #put need (command key value) syntax so we explode argument
            # taking first as key and the rest ast put value
            puts=argument.split(" ")
            # add entry to the hashTable
            tableEntryKey=puts[0]
            tableEntryValue=[]
            for valueWord in puts[1:]:
                tableEntryValue.append(valueWord)
            if verbose:
                common.emit(explainHash(tableEntryKey,tableSize),constants.PRINT_MESSAGE)
            # theTable is an object create using hashTable object that has __setitem__  
            # we just use the usual dictionary notation to set a value to a dictionary  (dictionary[key]=value) 
            theTable[tableEntryKey]=" ".join(tableEntryValue)

        #get value from hashtable
        elif command == 'g' or command == "get":
            if not theTable[argument]:
                common.emit(f" not value found for ({argument})")
            else:
                # theTable is an object create using hashTable object that has __getitem__  
                # we just use the usual dictionary notation to get a value (dictionary[key])
                common.emit(f" value key ({argument}) is ({theTable[argument]})")
            if verbose:
                common.emit(explainHash(argument,tableSize),constants.PRINT_MESSAGE)

        #delete value from hashtable
        elif command == 'd' or command == "del":
            print(theTable[argument])
            if not theTable[argument]:
                common.emit(f" not value to delete found for ({argument})")
            else:
                common.emit(f" deleted key ({argument}) with value({theTable[argument]})")
                if verbose:
                    common.emit(explainHash(argument,tableSize),constants.PRINT_MESSAGE)  
                    # theTable is an object create using hashTable object that has __delitem__  
                    # we just use the usuald dictionary notation to delete a value  (del dictionary[key])
                del theTable[argument]

        #save the hashtable
        elif command == 's' or command == "save":
            if inputWordsNumber==1:
                fileName=constants.SAVED_TABLE_FILENAME
                common.emit(f"saving on default {constants.SAVED_TABLE_FILENAME}",constants.LOG_TO_SYSLOG+constants.PRINT_MESSAGE)
            else:
                fileName=argument
            try:
                saveTable(theTable.table,fileName)
            except Exception as theError:
                common.emit(f" failed to save data ({fileName} {theError})",constants.LOG_TO_SYSLOG+constants.PRINT_MESSAGE)
            else:
                common.emit(f" table data saved in ({fileName})",constants.LOG_TO_SYSLOG+constants.PRINT_MESSAGE)

        #create hashtable 
        elif command == "c" or  command == "create":
            if hasTable:
                common.emit(f"table is already created with lengh {len(theTable.table)} ",constants.LOG_TO_SYSLOG+constants.PRINT_MESSAGE)
            else:
                if not argument:
                    argument=10
                try:
                    theTableSize=int(str(argument))
                except:
                    common.emit(f"invalid table size ({argument})")
                else:
                    if theTableSize < constants.MIN_TABLE_SIZE or theTableSize > constants.MAX_TABLE_SIZE:
                        common.emit("the size of the hashtable you will create is invalid (<10 or >100)",constants.LOG_TO_SYSLOG+constants.PRINT_MESSAGE)
                    else:
                        theTable=HashTable(theTableSize)
                        common.emit(f"created hashtable with size {theTableSize}",constants.LOG_TO_SYSLOG+constants.PRINT_MESSAGE)
        elif command == "v" or  command == "verbose":
            ## is already verbose shut down
            if  programControlMask & constants.MAIN_VERBOSE:
                programControlMask -=constants.MAIN_VERBOSE
                common.emit(f"verbose mode turned off")
            else:
                programControlMask +=constants.MAIN_VERBOSE
                common.emit(f"verbose mode turned on")
        elif  command == "gh":
            tableIndexFound=theTable.get_hash(argument)
            '''getValue= theTable.getItem(key)'''
            common.emit(f"i got ({tableIndexFound}) from ({argument})")
        # here if there are no recognized Commands ()
        else:
            common.emit(f"command ({command}) not recognized",constants.LOG_TO_SYSLOG+constants.PRINT_MESSAGE)
            
    #infinite loop
    main()

def printHelp():
    helpText = """
   __            __ ______     __   __
  / /  ___ ____ / //_  __/__ _/ /  / /__ ___
 / _ \/ _ `(_-</ _ \/ / / _ `/ _ \/ / -_|_-<
/_//_/\_,_/___/_//_/_/  \_,_/_.__/_/\__/ __/
v 1.1 written by Silvestro "pino" Di Pietro 2023     
a python simple explanation for hashTabling.        
written by Silvestro 'pino' Di Pietro                
in this lesson:
    * learn the basic of hashtable
    * managing hash conflicts with separate chaining method
    * usage of __getitem__ __setitem__ __delitem__ in classes

commands:
   h help               print this help
   c create N           create a N entries hashtable
   pr print             will print the table contents
   pd printDictionary   will print the created dictionary
   p put Key Value      will add/update Key entry with value
   g get Key            will return the value for Key
   d del Key            will delete the key entry
   s save NAME          will save current table with NAME
   l load NAME          will load a NAME table
   v verbose            will set the verbosity
   q quit               will end the program
"""
    common.emit(helpText, constants.PRINT_MESSAGE)


if __name__ == '__main__':
    main()

def explainHash(key,tableSize):
        '''
        this is the same hash function that is in hashClass.py
        but will return an explained explosion of the hash process
        '''
        hash = 0
        charKey=[]
        explainData=''
        keySize=len(str(key))
        charKey = [None for i in range(4)]
        #we will take 4 bytes to setup the hash
        # the first 2 bytes and the last 2 bytes (getting the ascii value with ord)
        #if the keySize is 3 the middle value will be the same in charkey[1] and  charkey[2]
        if keySize < 3:
            key=key.ljust(3,"0")
            keySize=len(str(key))
        charKey[0]=key[0]
        charKey[1]=key[1]
        charKey[2]=key[keySize-2]
        charKey[3]=key[keySize-1]
        for char in charKey:
            hash += ord(char)
        index=hash % tableSize
        explainData = f"key: {key} chars to hash: {charKey} ascii value sum: {hash} mod {tableSize} return the {index} entry in list"
        return  explainData

def printDictionary(hashedTable):
    '''  will recreate a structure key -> val from the ascii table
    '''
    resultTable=[]
    indexSize= len(hashedTable)
    i=1
    for indexedEntry in hashedTable:
        for idx,element in enumerate(indexedEntry):
            resultTable.append({'entry':i,'key':element[0],'value':element[1]})
            i +=1
    common.emit(common.makeAsciiTable(resultTable))

def saveTable(hashedTable,fileName=None):
    if not fileName:
        fileName=constants.SAVED_TABLE_FILENAME
    outFile=open(fileName,'w')
    json.dump(hashedTable,outFile,indent = 6)

def loadTable(fileName=None):
    if not fileName:
        fileName=constants.SAVED_TABLE_FILENAME
    infile=open(fileName,'r')    
    return json.load(infile)
