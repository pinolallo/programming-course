import csv
import sys
sys.path.append('../00-commons')
import common

conversionDictionary={
    
}

with open('datasets/movie_dataset.csv') as movie_csv:
     csv_movie_reader= csv.reader(movie_csv,delimiter=',')
     i=0
     header=[]
     for row in csv_movie_reader:
        # first line is the header of the csv
        if i==0:
             header.append(row)
             i +=1
        else:
            #print(f'\t{row[0]} works in the {row[1]} department, and was born in {row[2]}.')
            i += 1
common.emit(header)
