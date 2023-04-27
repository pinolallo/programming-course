"""
********************************************************
*  __          __                                      *
* / /____ ___ / /_  ___  _______  ___ ________ ___ _   *
*/ __/ -_|_-</ __/ / _ \/ __/ _ \/ _ `/ __/ _ `/  ' \  *
*\__/\__/___/\__/ / .__/_/  \___/\_, /_/  \_,_/_/_/_/  *
*                /_/            /___/                  *
* v 1.1 written by Silvestro "pino" Di Pietro 2023     *
* as example of structured python coding.              *
* written by Silvestro 'pino' Di Pietro                *
********************************************************
"""
import sys
import common
import constants
import data

def main():
    # this is a global that will permanent store among main a value
    # main is recursively called not using a infinite loop (while True)
    # to demostrate thipwds capability
    global programControlMask

    # initialization
    # the first run can be detected by checking if programControlMask exists
    try:
        programControlMask
    except:
        # this except will contain the inititalization of the program
        programControlMask = 0
        try:
            # verify if can write into logFile
            common.emit("testProgram Started", constants.LOG_TO_SYSLOG)
        except Exception as Error:
            common.emit(Error, constants.LOG_TO_SDIO)
            # set the MAIN_DIE bit of programControlMask
            sys.exit()
        # start program
        common.emit("welcome to testProgram, type h for help",
                constants.PRINT_MESSAGE)

    # the bitmask program control
    # the program will check bits of programControlMask
    if programControlMask & constants.MAIN_DIE:
        # quit program
        common.emit("end Task", 1)
        sys.exit()
    if programControlMask & constants.MAIN_CHECK:
        # reset the MAIN_CHECK bit of programControlMask
        programControlMask -= constants.MAIN_CHECK
        common.emit("test is still running fine")

    # program input commands
    dataInput = input("test> ")
    if dataInput.lower() == 'ck':
        # set MAIN_CHECK bit of programControlMask
        programControlMask += constants.MAIN_CHECK
    elif dataInput.lower() == "h":
        # run help
        printHelp()
    elif dataInput.lower() == "q":
        # set the MAIN_DIE bit of programControlMask
        programControlMask += constants.MAIN_DIE
    elif dataInput.lower() == "cr":
        # force an internal error to check the function response
        # sending a char (a) againts a bitwise integer
        try:
            common.emit("error check", "a")
        except Exception as Error:
            # manage teh excon return message
            common.emit(Error, constants.LOG_TO_SDIO+constants.LOG_TO_SYSLOG)
            # set the MAIN_DIE bit of programControlMask
            programControlMask += constants.MAIN_DIE
    elif dataInput.lower() == "tv":
        try:
            printable = common.makeAsciiTable(data.tvShow)
        except Exception as Error:
            common.emit(Error, constants.LOG_TO_SDIO+constants.LOG_TO_SYSLOG)
        else:
            common.emit(printable, constants.PRINT_MESSAGE)
    elif dataInput.lower() == "t":
        try:
            printable = common.makeAsciiTable(data.itNames)
        except Exception as Error:
            common.emit(Error, constants.LOG_TO_SDIO+constants.LOG_TO_SYSLOG)
        else:
            common.emit(printable, constants.PRINT_MESSAGE)
    elif dataInput.lower() == "re":
        try:
            printable = common.makeAsciiTable(data.Reddit)
        except Exception as Error:
            common.emit(Error, constants.LOG_TO_SDIO+constants.LOG_TO_SYSLOG)
        else:
            common.emit(printable, constants.PRINT_MESSAGE)
    elif dataInput.lower() == "lc":
        # hardcoded examples (bad habits) but is an example for the
        # common.emit capabilities
        myList = ['cippa', 'lippa', 'pippo', 'qui']
        myDict = {'pino': 'software architet', 'salvatore': 'senior sofware engineer',
                  'cosimo': 'junior software engineer'}
        mySet = {'pino software architet', 'salvatore senior sofware engineer',
                 'cosimo junior software engineer'}

        try:
            common.emit(myList, 3)
            common.emit(mySet, 3)
            common.emit(myDict, 3)
        except Exception as Error:
            common.emit(Error, constants.LOG_TO_SDIO+constants.LOG_TO_SYSLOG)
    else:
        common.emit(f"({dataInput}) is unrecognized command: type h for help")
    # run recursively
    main()

quit
def printHelp():
    helpText = """
  __          __
 / /____ ___ / /_  ___  _______  ___ ________ ___ _
/ __/ -_|_-</ __/ / _ \/ __/ _ \/ _ `/ __/ _ `/  ' \ 
\__/\__/___/\__/ / .__/_/  \___/\_, /_/  \_,_/_/_/_/
                /_/            /___/ 
v 1.1 written by Silvestro "pino" Di Pietro 2023
as example of structured python coding.
in this lesson:
    a) structured program (infinite loop) bitwise control
    b) usage of bitwise and constant
    c) use of  try except
    d) tracing log files
    e) input managment
    f) usage of global vars
    e) usage of Docstring (PEP 257) to document functions
    d) usage and description of function makeAsciiTable

commands:
    h   print this help
    ck  will check program running
    q   quit test program
    cr  try except test errors
    t   print a formatted ascii table with IT names
    tv  print a formatted ascii table tv program data
    re  print a formatted ascii table with reddit info
    lc  will send a list, a sets and a dictionary to
        sdio
        log 
"""
    common.emit(helpText, constants.PRINT_MESSAGE)


if __name__ == '__main__':
    main()
