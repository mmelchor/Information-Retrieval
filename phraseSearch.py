######################################################
# Miguel Melchor (03/30/2014) 
# phraseSearch.py
# searches for each phrase in the document, if phrase
# not in document then searches for each word in doc
######################################################

import nltk
from nltk.stem import SnowballStemmer
from itertools import tee, izip
from invertedFiles import *


def bigrams(words):
    x, y = tee(words)
    next(y, None)
    return izip(x,y)

def createBigrams(filein,table):
    #dict of dict of list ex:{'a':{'b':[(1,t),(2,t)],'c':[(1,t),(2,t)]}}
    fin = open(filein,"r")
    title = filein.split("_")[0]
    words = fin.readlines()
    words = words[0].split()
    bi = bigrams(words)
    bi = list(bi)

    for item in bi:
        ID = item[0][0]
        if ID in table:
            if item not in table[ID]:
                table[ID][item] = [[1,title]]
            elif table[ID][item][-1][1] == title:
                table[ID][item][-1][0] += 1
            else:
                table[ID][item].append([1,title])
    
    fin.close()

def phraseSearch(query,table,singleTable):
    #searches for the phrase and each individual word in each doc
    snowball = SnowballStemmer('english')
    query = query.split()
    stemmed = []
    matches = []

    for word in query:
        stemmed.append(snowball.stem(word.lower()))

    biPhrase = (stemmed[0],stemmed[1])
    idTable = table[biPhrase[0][0]]

    if biPhrase in idTable:
        phraseOccurences = idTable[biPhrase]

        #sorts by most relevant
        phraseOccurences.sort(key=lambda x: x[0])
        print " MATCH:"
        threshold = phraseOccurences[-1][0]
        for i in range(len(phraseOccurences)-1,-1,-1):
            if phraseOccurences[i][0] >= threshold//2:
                print " " + phraseOccurences[i][1]+ " ", phraseOccurences[i][0]

       #Prints books that have both keywords in it but not together
    
    
        for i in range(len(phraseOccurences)): matches.append(phraseOccurences[i][1])
    
    else: print " MATCH: No Matches"

    searchEachWord(stemmed,singleTable,matches)

def searchEachWord(query,table,Match):
    #search for each word in each file
    ID1 = query[0][0]; ID2 = query[1][0]
    idTable1 = table[ID1]; idTable2 = table[ID2];

    if query[0] not in idTable1 and query[1] not in idTable2:
        print "No Matches"

    elif query[0] not in idTable1:
        print "No Matches for "+query[0]
        print "Matches for " + query[1]+":"
        searchInvertedFiles(query[1],table)

    elif query[1] not in idTable2:
        print "No Matches for "+query[1]
        print "Matches for " + query[0]+":"
        searchInvertedFiles(query[0],table)

    else:

        IdTable1 = table[ID1]; wordOccurences1 = IdTable1[query[0]]
        IdTable2 = table[ID2]; wordOccurences2 = IdTable2[query[1]]
    
    
        wordOccurences1.sort(key=lambda x: x[0])
        wordOccurences2.sort(key=lambda x: x[0])
    
        total = {}
    
        for item in wordOccurences1:
            if item[1] not in Match:
                total[item[1]] = [item[0],0]
        
        for item in wordOccurences2:
            if item[1] in total:
                values = total[item[1]]
                values[1] = item[0] 
                total[item[1]] = values        
            elif item[1] not in total and item[1] not in Match:
                total[item[1]] = [0,item[0]]

    
        #classify each file as relevant if both words appear in it
        relevant = []
        lessRelevant = []
        for item in total:
            if total[item][0] != 0 and total[item][1] != 0:
                relevant.append([total[item][0]+total[item][1],item])
            else:
                lessRelevant.append([total[item][0]+total[item][1],item])
            
        relevant.sort(key=lambda x: x[0])
        lessRelevant.sort(key=lambda x: x[0])
    
        print " MATCH BUT NOT TOGETHER:"
        if len(relevant) == 0:
                print " No Matches"
        else:
            for i in range(len(relevant)-1,-1,-1):
                print " " + relevant[i][1] + " ", relevant[i][0]

        print " SINGLE MATCH:"
        if len(lessRelevant) == 0:
                print " No Matches"
        else:
            for i in range(len(lessRelevant)-1,-1,-1):
                print " " + lessRelevant[i][1] + " ", lessRelevant[i][0]
                
        
            

    
    
    
                       
        
    
