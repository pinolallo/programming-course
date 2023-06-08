import csv
import sys
sys.path.append('../00-commons')
import common
import re
import constants

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
     
def importSqlGeneator(header,row,databaseDef,mainRecordId):
     sqlelements=[];
     i=0
     #common.emit(databaseDef)
     for field in row:
          #common.emit(f"field {field}")
          sqlelement={}
          try:
               sqlelement[header[i]]=fieldValuate(header[i],field,databaseDef,mainRecordId)
          except:
               vvival=''
               #common.emit(f"fail field evalutate {header[i]} fieldvalue:{field} main recordid:{mainRecordId}")
          '''try:
               sqlelement[header[i]]=fieldValuate(header[i],field,databaseDef)
          except:
               common.emit(f"fail generating insert sql line for field ({header[i]})",constants.PRINT_MESSAGE+constants.LOG_TO_SYSLOG)'''
          sqlelements.append(sqlelement)
          i=i+1

def fieldValuate(field, value, databaseDef,mainRecordId):
     hasQuote=True
     sql=[]
     result={}
     result[constants.MAIN_DB_TABLE]={}
     result[constants.MAIN_DB_TABLE]['field']=[]
     result[constants.MAIN_DB_TABLE]['value']=[]
     conversionDictionary={
          'index':{'action':'null'},
          'budget':{'action':',fill(movie_budget)'},
          'genres':{'action':',fill(movie_genres)'},
          'homepage':{'action':',fill(movie_HomePage)'},
          'id':{'action':',fill(movie_id)'},
          'keywords':{'action':',fill(movie_keywords)'},
          'original_language':{'action':',fill(movie_original_lang)'},
          'original_title':{'action':',fill(movie_original_title)'},
          'overview':{'action':',fill(movie_overview)',},
          'popularity':{'action':',fill(movie_popularity)'},
          'production_companies':{'action':',putRelation(movie_id,productions,movie_productions)'},
          'production_countries':{'action':',putRelation(movie_id,countries,movie_countries)'},
          'release_date':{'action':',fill(movie_relase)'},
          'revenue':{'action':',fill(movie_revenue)'},
          'runtime':{'action':',fill(movie_runtime)'},
          'spoken_languages':{'action':',putRelation(movie_id,laguages,movie_lang)'},
          'status':{'action':'null'},
          'tagline':{'action':',fill(movie_tagline)'},
          'title':{'action':',fill(movie_title)'},
          'vote_average':{'action':',fill(movie_vote_average)'},
          'vote_count':{'action':',fill(movie_vote_num)'},
          'cast':{'action':',fill(movie_cast)'},
          'crew':{'action':',putDb(credits,job:job_name,department:job_department,name:people_name,gender:people_gender)'},
          'director':{'action':'null'}
     }
     command=conversionDictionary[field]
   
     if  command['action'] == 'null':
          return result
     #fieldType=databaseDef[constants.MAIN_DB_TABLE][field]['fieldType']
     '''if fieldType=='int' or fieldType=='float':
          hasQuote=0
     else:
          hasQuote=1'''
     
     common.emit(f"adadadadadad {command['fieldType']}")
     parsedFunctions=re.findall(",(.*?)\((.*?)\)",command['action'])
     
     common.emit(parsedFunctions)

     for parsedFunction in parsedFunctions:
          i=0
          for functionElement in parsedFunction:
               if i==0:
                    functionName=functionElement
               else:
                    functionArgument=functionElement
               i=i+1
          if functionName=='fill':
               common.emit(f'datasetField:{field} fill dbfield ({functionArgument})')
               result['field'].append(field)
               if hasQuote==1:
                    result[constants.MAIN_DB_TABLE]['value'].append(f"'{value}'")
               else:
                    result[constants.MAIN_DB_TABLE]['value'].append(value)
          elif functionName=='putRelation':
               result[splittedArgs[2]]={}
               splittedArgs=functionArgument.split(",")
               common.emit(f'datasetField:{field} will make a relation in table {splittedArgs[2]} using id ({splittedArgs[0]}) left joined ({splittedArgs[1]})) ')
          elif functionName=='putDb':
               common.emit('putDB')
               splittedArgs=functionArgument.split(",")
               #popping out the first argument (the table)
               fillingTable=splittedArgs.pop(0)
               queryElement={}
               queryElement['field']=[]
               queryElement['value']=[]
               #adding movie id
               queryElement['field'].append('credit_id')
               queryElement['value'].append(mainRecordId)
               for fieldArg in splittedArgs:
                    #field has colon as sepator
                    tmp=fieldArg.split(":")
                    queryElement=putDb(value,tmp[0],tmp[1],queryElement)
                    common.emit(f'datasetField:{field} will add into db {fillingTable} fieldJason ({tmp[0]}) int dbField ({tmp[1]})) ')
               for fieldInsert in queryElement:
                    fields=",".join(fieldInsert['field'])
                    values=",".join(fieldInsert['value'])
                    sql.append(f'insert IGNORE into {fillingTable} ({fields}) values ({values})') 
               common.emit(sql)
     return result


def putDb(crewSet,fieldJason,dbField,queryElement):
     queryElement={}
     queryElement['field']=[]
     queryElement['value']=[]
     for crew in crewSet:
          queryElement['field'].append(dbField)
          queryElement['value'].append(f"'{crew[fieldJason]}'")
     return queryElement
