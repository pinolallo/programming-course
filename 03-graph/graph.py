"""
********************************************************
*   _____              __     ___  ________            *
*  / ___/______ ____  / /    / _ )/ __/ __/            *
* / (_ / __/ _ `/ _ \/ _ \  / _  / _/_\ \              *
* \___/_/  \_,_/ .__/_//_/ /____/_/ /___/              *
*             /_/                                      *
* v 1.1 written by Silvestro "pino" Di Pietro 2023     *
* a python simple explanation for breadth-first-search *
* written by Silvestro 'pino' Di Pietro                *
********************************************************
"""
import sys
sys.path.append('../00-commons')
import common
import constants
import sys
import json

visited = [] # List for visited nodes.
queue = []     #Initialize a queue  
resultSequence=""
def main():
    global programControlMask, theGraph, commandsDictionary,resultSequence
     # initialization
    # the first run can be detected by checking if programControlMask exists
    try:
        programControlMask
    except:
        # this except will contain the inititalization of the program
        programControlMask = 0
        try:
            # verify if can write into logFile
            common.emit("Graph program Started", constants.LOG_TO_SYSLOG)
        except Exception as Error:
            common.emit(Error, constants.LOG_TO_SDIO)
            # set the MAIN_DIE bit of programControlMask
            sys.exit()
        # start program
        common.emit("welcome to Graph, type h for help",constants.PRINT_MESSAGE)
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
            "l":0,
            "load":0,
            "s":constants. MAIN_COMMAND_DATA,
            "solve":constants. MAIN_COMMAND_DATA,
        }
    # get the input    
    dataInput = input("graph> ")

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
    canExec=True
    hasGraph=True
    #check if there is a table (see global)
    try:
        theGraph
    except:
        hasGraph=False
        
    else:
        dataize=len(theGraph)

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
        if  commandsDictionary[command] & constants.MAIN_COMMAND_DATA:
            if  hasGraph==False:
                common.emit("cannot solve: no graph loaded", constants.PRINT_MESSAGE)
                canExec=False

#run the commandx
    if canExec:
        fileName=constants.SAVED_DATA_FILENAME
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
            if inputWordsNumber > 1:
                fileName=argumentslist
            try:
                loadedTable=loadData(fileName)
            except Exception as theError:
                common.emit(f" failed to load data ({fileName}) {theError}",constants.LOG_TO_SYSLOG+constants.PRINT_MESSAGE)
            else:
                theGraph=loadedTable
                common.emit(f" table data ({fileName}) loaded",constants.LOG_TO_SYSLOG+constants.PRINT_MESSAGE)
        elif command == 's' or command == "solve":
            puts=argument.split(" ")
            if puts[0] == "bsf":
                common.emit(f" traversing graph ({fileName}) with BFS",constants.LOG_TO_SYSLOG+constants.PRINT_MESSAGE)
                resultSequence=""
                visited = [] # List for visited nodes.
                result=bfs(theGraph, '1') 
                common.emit(f"bfs {result}")
            else:
                common.emit(f" traversing graph ({fileName}) with DSF",constants.LOG_TO_SYSLOG+constants.PRINT_MESSAGE)
                resultSequence=""
                visited=set()
                result=dfs(visited,theGraph, '1') 
                common.emit(f"dsf {result}")
    main()

if __name__ == '__main__':
    main()





def printHelp():
    helpText = """
  _____              __     ______
 / ___/______ ____  / /    /_  __/______ __  _____ _______ ___
/ (_ / __/ _ `/ _ \/ _ \    / / / __/ _ `/ |/ / -_) __(_-</ -_)
\___/_/  \_,_/ .__/_//_/   /_/ /_/  \_,_/|___/\__/_/ /___/\__/
 v 1.1 written by Silvestro "pino" Di Pietro 2023     
a python simple explanation for graph traverse.        
written by Silvestro 'pino' Di Pietro                
in this lesson:
    * learn the basic of breadth first search
    * iterative functions
    * recursive funtions (dynamic programming)

commands:
   h help               print this help
   l load tree          load the graph
   v verbose            be verobose
   s solve  type        clearsolve Tree
   q quit               will end the program
"""
    common.emit(helpText, constants.PRINT_MESSAGE)

def dfs(visited,theGraph, node):  #function for dfs 
    global resultSequence
    if str(node) not in visited:
        resultSequence += f" {str(node)}"
        visited.add(str(node))
        for neighbour in theGraph[str(node)]:
            #recursive function call
            dfs(visited, theGraph, neighbour)
    return resultSequence

def bfs(theGraph, node): #function for BFS
    global resultSequence
    visited=[]
    queue=[]
    #visited.append(str(node))
    queue.append(str(node))
    while queue:          # Creating loop to visit each node
        m = str(queue.pop(0)) 
        resultSequence = resultSequence+f" {m}"
        for neighbour in theGraph[str(m)]:
            if neighbour not in visited:
                visited.append(neighbour)
                queue.append(neighbour)
    return resultSequence

def loadData(fileName=None):
    if not fileName:
        fileName=constants.SAVED_DATA_FILENAME
    infile=open(fileName,'r')    
    return json.load(infile)
