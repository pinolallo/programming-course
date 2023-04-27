"""
********************************************************
*   _____                                              *
*  / ___/__  __ _  __ _  ___  ___  ___
* / /__/ _ \/  ' \/  ' \/ _ \/ _ \(_-<
* \___/\___/_/_/_/_/_/_/\___/_//_/___/
* v 1.1 written by Silvestro "pino" Di Pietro 2023     *
* Common functions                                     *
* little example of a library file for shared          *
* function                                             *
*                                                      *
* written by Silvestro 'pino' Di Pietro                *
********************************************************
"""
import datetime
import logging
import logging.handlers
import sys
sys.path.append('../00-commons')
import constants


def emit(message, outputType=1):
    """Will output text
        arguments:
            message can be a string
                a dictionary
                a set
            outputType (int) bitmask for different outputs where
                bit 1 will output as printout on stdio (wihout timestamp)
                bit 2 will output on stdio with timestamp
                bit 4 will output on constants SYSLOG
                bit 8 will send an email (not implemented)
    """
    if not isinstance(outputType, int):
        errorMsg = f'emit: invalid outpuType, ({outputType}) must be an integer'
        emit(errorMsg, constants.LOG_TO_SYSLOG)
        raise TypeError(errorMsg)
    if outputType & constants.LOG_TO_SDIO:
        outputSdio(message)
    if outputType & constants.LOG_TO_SYSLOG:
        outputSyslog(message)
    if outputType & constants.LOG_TO_EMAIL:
        outputMail(message)
    if outputType & constants.PRINT_MESSAGE:
        outputSdio(message, False)

def createEmitOutput(message, logMode=True):
    """Will managed the format of the message:
        arguments:
            message will be splitted into lines
                if is a set or a list just lines
                if is a dictionary the line will
                be formatted with key tab value
            logMode:
                if true
                will  start with timestamp
                and end with end task
        return:
            formatted string
    """
    output = [];
    todayDate = datetime.datetime.now()
    if logMode:
        output.append(f" ---  start emit{todayDate}")
    if type(message) is list or type(message) is set:
        for messageValue in message:
            output.append(f" {messageValue}")
    elif type(message) is dict:
        for key, value in message.items():
            pkey = key.ljust(20, " ")
            output.append(f"{pkey} {value}")
    else:
        output.append(f"{message}")
        if logMode:
            output.append("--- end emit")
    return output


def outputSdio(message, logMode=True):
    """output on logfile
        arguments:
            message: a string, dict, list or set
            logMode: if true
                will  start with timestamp
                and end with end task
        return:
            void

    """
    output = createEmitOutput(message, logMode)
    for line in output:
        print(f"{line}")


def outputSyslog(message):
    """output on stdio
        arguments:
            message: a string, dict, list or set
        return:
            void
    """
    output = createEmitOutput(message)
    errorMessage = f'cannot open file {constants.SYSLOG_FILENAME} check constant.py conf SYSLOG_FILENAME'
    try:
        logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                            filename=constants.SYSLOG_FILENAME, encoding='utf-8', level=logging.DEBUG)
    except:
        raise TypeError("basicConfig openLog "+errorMessage)
    for line in output:
        try:
            logging.debug(f"{line}")
        except:
             raise TypeError("writing line  " + errorMessage)


def outputMail(message):
        """output on mail (not implemented)
        arguments:
            message: a string, dict, list or set
        return:
            void
    """
        return None


def makeAsciiTable(input):
    '''will return a formatted ascii table from a list with dictionary structure
        arguments:
            input as list [{'key':'val'},{'key':'val1'},{'key':'valN'}]
        return:
            +------+
            | key  |
            +------+
            |   val|
            |  val1|
            |  valN|
            +------+
    '''
    tablePrint = ["", "", ""]
    # need that input is a list
    if type(input) is not list:
        raise Exception(f'input is not a list but ('+type(input)+')')
    strucSize = len(input)
    if strucSize == 0:
        return
    fieldDim = {}
    i = 0
    for record in input:
        # need that record is a dictionary
        if type(record) is not dict:
            raise Exception(f'record is not a dict but ('+type(record)+')')
        # get header value and  field size
        for fieldName, fieldValue in record.items():
            if i == 0 and type(fieldValue) is not dict:
                #we can manage always strings
                fieldName = str(fieldName)
                fieldDim[fieldName]=len(fieldName)+2
            if  type(fieldValue) is  dict:
                continue
            fieldValue=str(fieldValue)
            lenSize= len(fieldValue)+2  
            if lenSize > fieldDim[fieldName]:
                fieldDim[fieldName]=lenSize
        i=i+1
    #create table header
    for fieldName,lenSize in fieldDim.items():
        if fieldName not in fieldDim:
            continue
        emptyStuff=""
        fieldName = str(fieldName)
        tablePrint[0] +=  '+' + emptyStuff.ljust(lenSize,"-")
        tablePrint[1] += "|" + fieldName.center(fieldDim[fieldName])
    tablePrint[0] += "+"
    tablePrint[1] += "|"
    tablePrint[2] =tablePrint[0]
    i=3
    #fill columns
    for record in input:
        tablePrint.append("")
        for fieldName, fieldValue in record.items():
            if type (fieldValue) is dict or type (fieldValue) is list:
                continue
            fieldValue = str(fieldValue)
            tablePrint[i] += "|" + fieldValue.rjust(fieldDim[fieldName],' ')
        tablePrint[i] += "|"
        i=i+1
    #end line
    tablePrint.append(tablePrint[0])
    #textify the created list   
    output = "\n".join(tablePrint)
    return output
