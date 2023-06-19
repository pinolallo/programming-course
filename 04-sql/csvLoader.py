import csv
import sys
sys.path.append('../00-commons')
import common
import re
import constants
import json
import  mysql.connector

'''
this is the core of the sql importer schema:
any field from the main dataset will be evaluated with a pseudo function related
those are
     null don't consider value
     fill (will put the main dataset field into the sql field passed as argument )
     putDB (will enter a new record into (first element tableName) unsing the list of from_fieldName : to_fieldName list of fields)

'''
conversionDictionary={
               'index':'null',
               'budget':'fill(movie_budget)',
               'genres':'fill(movie_genres)',
               'homepage':'fill(movie_HomePage)',
               'id':'fill(movie_id)',
               'keywords':'fill(movie_keywords)',
               'original_language':'fill(movie_original_lang)',
               'original_title':'fill(movie_original_title)',
               'overview':'fill(movie_overview)',
               'popularity':'fill(movie_popularity)',
               'production_companies':'putDb(productions,name:prod_name,id:prod_id)',
               'production_countries':'putDb(countries,iso_3166_1:country_id,name:country_name)',
               'release_date':'fill(movie_relase)',
               'revenue':'fill(movie_revenue)',
               'runtime':'fill(movie_runtime)',
               'spoken_languages':'putDb(languages,iso_639_1:lang_id)',
               'status':'null',
               'tagline':'fill(movie_tagline)',
               'title':'fill(movie_title)',
               'vote_average':'fill(movie_vote_average)',
               'vote_count':'fill(movie_vote_num)',
               'cast':'fill(movie_cast)',
               'crew':'putDb(credits,job:job_name,department:job_department,name:people_name,id:credit_id)',
               'director':'null'
          }

def getDataset():
     #simple csv loader
     #will return the list of field name (header)
     #the list of single comma separated records
     # and the conversion dictionary
     with open('datasets/movie_dataset.csv') as movie_csv:
          csv_movie_reader= csv.reader(movie_csv,delimiter=',')
          i=0
          rawDb=[]
          result={}
          for row in csv_movie_reader:
               # first line is the header of the csv
               if i==0:
                    header=row
               else:
                    rawDb.append(row)
               i += 1
          result['header']=header 
          result['db']=rawDb
          #transport also the conversion Dictionary
          result['conversionDictionary']=conversionDictionary     
          return result
     

def importSqlGeneator(header,row,mainRecordId,sqlelements):
     #create sqlElement structure
     sqlelements={}
     sqlelements['queryElement']={}
     sqlelements['queryElement']['fields']=[]
     sqlelements['queryElement']['values']=[]
     sqlelements['sqlQueries']=[]
     i=0
     #iterate for each single record in row
     for fieldValue in row:
          #create sql elements (and sqlQueris for related fields)
          sqlelements=fieldValuate(header[i],fieldValue,mainRecordId,sqlelements)
          #get MAIN_DB_TABLE record sql elements and create a comma separated list    
          sqlFields=",".join(sqlelements['queryElement']['fields'])
          sqlValues=",".join(sqlelements['queryElement']['values'])
          i=i+1
     #create sql query line for the main MAIN_DB_TABLE
     recordSql=f'insert IGNORE into {constants.MAIN_DB_TABLE} ({sqlFields}) values ({sqlValues});'
     #merge the sql line with the internal (conversionDictionary) generated query
     sqlelements['sqlQueries'].append(recordSql)
     return   sqlelements['sqlQueries']

    


def fieldValuate(fieldName, fieldValue,mainRecordId,result):
     splittedArgs=[]
     command=conversionDictionary[fieldName]
     if  command == 'null':
          #do not consider field
          return result
     #we need to divide using a regular expression the function and argument related to the field to be evaluated
     match=re.search("(.*?)\((.*?)\)",command)
     functionName=match.group(1)
     functionArgument=match.group(2)
     if functionName=='fill':
          #since we do create a sql string and not sendig a sql command we nee to delete internal quoting 
          fieldValue=fieldValue.replace("'",' ')
          fieldValue=fieldValue.replace("\"",' ')
          #is a number or a string?
          if not re.match("^[0-9.]+$",fieldValue):
               #is not a number need to be quoted
               db_value=(f'"{fieldValue}"')
          result['queryElement']['values'].append(f'"{fieldValue}"')
          result['queryElement']['fields'].append(functionArgument)
         
          return result
     #here there are the related table to be created from the field that contain json structure
     elif functionName=='putDb':
          #the data structure loaded need quote replacemente to be stransformed into a json
          jsonField=fieldValue.replace("\'", "\"")
          try:
               #this a fix for some record that give error on json transforming (see pythonTestLog and the loadJsonFix function )
               fieldValue=loadJsonFix(jsonField,fieldName,mainRecordId)
          except Exception as theError:
               #this in case of an unrecoverable error
               common.emit('bad json Field {fieldName} on record{mainRecordId}',constants.LOG_TO_SYSLOG,constants.PRINT_MESSAGE)
               return result
          #get a list of arguments (there is a comma separated list)
          splittedArgs=functionArgument.split(",")
          #popping out the first argument (that is the destination table name)
          #pop will remove the first argument of the list
          fillingTable=splittedArgs.pop(0)
          #preparing the insert element list struct
          fieldsFiller={}
          for recordLine in fieldValue:
               mfields=[]
               mvalues=[]
               #adding relation id to the element list before read the recipe
               fieldsFiller[constants.MAIN_DB_RECORD_FIELD]=mainRecordId
               #fill all field name value using the arguments list
               for fieldArg in splittedArgs:
                    #field has colon as separator, we need the json key associated to 
                    tmp=fieldArg.split(":")
                    if len(tmp):
                         fieldsFiller[tmp[1]]=recordLine[tmp[0]]
                    else:
                         continue
               sqlValues=''
               sqlFields=''
               try:
                    for db_field,db_value in fieldsFiller.items():
                         #to evalutate a number with regular expression we need always a string
                         db_value=str(db_value)
                         #the number check regular expression
                         if not re.match("^[0-9.]+$",db_value):
                              #we have an alphanumeric value, we need to remove quotation marks
                              db_value=db_value.replace("\'",' ')
                              db_value=db_value.replace("\"",' ')
                              #and save the value quoted
                              db_value=f"'{db_value}'"
                         #we fill a list with values and fields
                         mvalues.append(db_value)
                         mfields.append(db_field)
               except Exception as err:
                    common.emit(f'error on parsing ({db_field})({db_value})  db_value {err}')
               #create a comma separated list of fields and value
               sqlFields=",".join(mfields)
               sqlValues=",".join(mvalues)
               #create the sql query using the above comma separated strings and append that to resulting list of query              
               result['sqlQueries'].append(f'insert IGNORE into {fillingTable} ({sqlFields}) values ({sqlValues});')
     return result



def loadJsonFix(s,field=None,record_id=None):
     ''' 
       fix from https://stackoverflow.com/a/18515887
     '''
     t=0
     result={}
     while  t < 2 :
        try:
            result = json.loads(s)   # try to parse...
            break                    # parsing worked -> exit loop
        except Exception as e:
            t=t+1
            common.emit(f"json parse error fix {e} on field {field} of {record_id}",constants.LOG_TO_SYSLOG)
            # "Expecting , delimiter: line 34 column 54 (char 1158)"
            # position of unexpected character after '"'
            unexp = int(re.findall(r'\(char (\d+)\)', str(e))[0])
            # position of unescaped '"' before that
            unesc = s.rfind(r'"', 0, unexp)
            s = s[:unesc] + r'\"' + s[unesc+1:]
            # position of correspondig closing '"' (+2 for inserted '\')
            closg = s.find(r'"', unesc + 2)
            s = s[:closg] + r'\"' + s[closg+1:]
     return result
