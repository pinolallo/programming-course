import csv
import sys
sys.path.append('../00-commons')
import common
import re
import constants
import json
import  mysql.connector


def getDataset():
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
          return result
     
def importSqlGeneator(header,row,mainRecordId,sqlelements):
     i=0
     for fieldValue in row:
          try:
               sqlelements=fieldValuate(header[i],fieldValue,mainRecordId,sqlelements)
          except:
               vvival=''
          i=i+1
    
     sqlFields=",".join(sqlelements['queryElement']['fields'])
     sqlValues=",".join(sqlelements['queryElement']['values'])
     #print(sqlelements['extraQuery'])
     recordSql=f'insert IGNORE into {constants.MAIN_DB_TABLE} ({sqlFields}) values ({sqlValues})'
     sqlelements['extraQuery'].append(recordSql)
     #print(recordSql)
     return sqlelements

    


def fieldValuate(fieldName, fieldValue,mainRecordId,result):
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
               'production_companies':'putRelation(movie_id,productions,movie_productions)',
               'production_countries':'putRelation(movie_id,countries,movie_countries)',
               'release_date':'fill(movie_relase)',
               'revenue':'fill(movie_revenue)',
               'runtime':'fill(movie_runtime)',
               'spoken_languages':'putRelation(movie_id,laguages,movie_lang)',
               'status':'null',
               'tagline':'fill(movie_tagline)',
               'title':'fill(movie_title)',
               'vote_average':'fill(movie_vote_average)',
               'vote_count':'fill(movie_vote_num)',
               'cast':'fill(movie_cast)',
               'crew':'putDb(credits,job:job_name,department:job_department,name:people_name)',
               'director':'null'
          }
   
     command=conversionDictionary[fieldName]   
     if  command == 'null':
          return result
     match=re.search("(.*?)\((.*?)\)",command)
     functionName=match.group(1)
     functionArgument=match.group(2)
     if functionName=='fill':
          if not re.match("^[0-9.]+$",fieldValue):
               fieldValue=fieldValue.replace("'","\'")
               db_value=(f'"{fieldValue}"')
          result['queryElement']['values'].append(f'"{fieldValue}"')
          result['queryElement']['fields'].append(functionArgument)
          return result
     elif functionName=='putRelation':
         # result[splittedArgs[2]]={}
          #splittedArgs=functionArgument.split(",")
          common.emit(f'datasetField:{fieldName} will make a relation in table {splittedArgs[2]} using id ({splittedArgs[0]}) left joined ({splittedArgs[1]})) ')
     elif functionName=='putDb':
          fieldValue=json.loads(fieldValue.replace("'", '"'))
          splittedArgs=functionArgument.split(",")
          #popping out the first argument (the table)
          fillingTable=splittedArgs.pop(0)
          #preparing the insert element list struct
          fieldsFiller={}
          for recordLine in fieldValue:
               mfields=[]
               mvalues=[]
               #adding relation id to the element list before read the recipe
               fieldsFiller[constants.MAIN_DB_RECORD_FIELD]=mainRecordId
               #fill all field name value using the arguments
               for fieldArg in splittedArgs:
                    #field has colon as separator, we need the json key associated to 
                    tmp=fieldArg.split(":")
                    fieldsFiller[tmp[1]]=recordLine[tmp[0]]
               sqlValues=''
               sqlFields=''
               try:
                    for db_field,db_value in fieldsFiller.items():
                         if not re.match("^[0-9.]+$",db_value):
                              db_value=(f"'{db_value}'")
                         mfields.append(f"{db_field}")
                         mvalues.append(f"{db_value}")
               except:
                   #strange error on the fieldFiller
                   val=""
               sqlFields=",".join(mfields)
               sqlValues=",".join(mvalues)
               common.emit(f'insert IGNORE into {fillingTable} ({sqlFields}) values ({sqlValues});')
               result['extraQuery'].append(f'insert IGNORE into {fillingTable} ({sqlFields};) values ({sqlValues})')
     return result

