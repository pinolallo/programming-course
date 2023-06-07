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
                    #common.emit(f'\t{row[0]} works in the {row[1]} department, and was born in {row[2]}.')
                    rawDb.append(row)
               i += 1
          result['header']=header 
          result['db']=rawDb     
          return result
     
def importSqlGeneator(header,row,databaseDef):
     sqlelements=[];
     i=0
     for field in row:
          #common.emit(f"field {field}")
          sqlelement={}
          sqlelement[header[i]]=fieldValuate(header[i],field,databaseDef)
          '''try:
               sqlelement[header[i]]=fieldValuate(header[i],field,databaseDef)
          except:
               common.emit(f"fail generating insert sql line for field ({header[i]})",constants.PRINT_MESSAGE+constants.LOG_TO_SYSLOG)'''
          sqlelements.append(sqlelement)
          i=i+1

def fieldValuate(field, value, databaseDef):
     hasQuote=True
     conversionDictionary={
          'index':{'action':'null'},
          'budget':{'action':',fill(movie_budget)'},
          'genres':{'action':',fill(movie_genres)'},
          'homepage':{'action':',fill(movie_HomePage)'},
          'id':{'action':',fill(movie_id)'},
          'keywords':{'action':',fill(movie_keywords)'},
          'original_language':{'action':',getId(languages,movie_original_lang)'},
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
          'crew':{'action':',putDb(jobs,job:job_name,department:job_department),putDb(people,name:people_name,gender:people_gender),putRelation(people_id,job_id,people_jobs),putRelation(movie_id,job_id,movie_jobs)'},
          'director':{'action':'null'}
     }
     command=conversionDictionary[field]
     if  command['action'] == 'null':
          common.emit(f'field {field} has a null action')
          return
     else:
          fieldAction=command['action']
          '''fieldType=databaseDef[constants.MAIN_DB_TABLE][field]
          if fieldType=='int' or fieldType=='float':
               hasQuote=False'''
          parsedFunctions=re.findall(",(.*?)\((.*?)\)",fieldAction)
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
               elif functionName=='getId':
                    splittedArgs=functionArgument.split(",")
                    common.emit(f'datasetField:{field} wil gedId from table {splittedArgs[0]} and fill dbfield({splittedArgs[1]}) ')
               elif functionName=='putRelation':
                    splittedArgs=functionArgument.split(",")
                    common.emit(f'datasetField:{field} will make a relation in table {splittedArgs[2]} using id ({splittedArgs[0]}) left joined ({splittedArgs[1]})) ')
               elif functionName=='putDb':
                    splittedArgs=functionArgument.split(",")
                    #popping out the first argument (the table)
                    fillingTable=splittedArgs.pop(0)
                    inputFields=[]
                    outputFields=[]
                    #we can have an undetermined list of fields from json to db
                    for fieldArg in splittedArgs:
                         #field has colon as sepator
                         tmp=fieldArg.split(":")
                         inputFields.append(tmp[0])
                         outputFields.append(tmp[1])
                         common.emit(f'datasetField:{field} will put into db {fillingTable} fieldJason ({tmp[0]}) int dbField ({tmp[1]})) ')
          return ['cose']   
