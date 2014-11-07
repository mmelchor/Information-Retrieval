#####################################################
# Miguel Melchor (03/30/2014) 
# clean.py
# Clean the text of each book
####################################################

import sys
import re
import os
import os.path
import string
from nltk.stem import SnowballStemmer
from unidecode import unidecode


def filterFile(filein,fileout):
    #Turn to lowercase, remove Spaces, replace Or Remove Special Symbols 
    #and stem words

    fin = open(filein,"r")
    fout = open(fileout,"w")

    snowball = SnowballStemmer('english')
    end = "End of the Project Gutenberg"

    #remove the header
    lines = fin.readline()
    while re.match(r'^Title',lines)==None:
        lines = fin.readline()
        
    lines = re.sub(r'[:,]+',"",lines)
    words = lines.split()
    for word in words: 
        fout.write(snowball.stem(word.lower())+" ")

    #Filter and stem
    for line in fin:
        if end in line:
            break
        elif re.search('\S',line):
            line = line.lower()
            line = re.sub(r'\s+'," ",line)
            line = re.sub(r'&',"and",line)
            line = re.sub(r'[\[\]\'\"()@#$%^&*?\|!.,:;]+|(--)+','',line)
            line = re.sub(r'[_-]+'," ",line)
            words = line.split()
            for word in words: 
                try:
                    fout.write(snowball.stem(word)+" ")
                except ValueError:
                    #REMOVES ALL ACCENTS
                    word = unicode(word,"utf-8")
                    word = unidecode(word)
                    fout.write(snowball.stem(word)+" ")
        
    fin.close()
    fout.close()


    


