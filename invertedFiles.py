#####################################################
# Miguel Melchor (03/30/2014) 
# invertedFiles.py
# Implements one InvertedFiles algorithm
####################################################

from nltk.stem import SnowballStemmer

def createHashTable():
    table = {}
    alpha = "abcdefghijklmnopqrstuvwxyz0123456789"
    for letter in alpha:
        table[letter] = {}
    return table

def createKeywords(filein,table):
    #dict of dict of list ex:{'a':{'b':[(1,t),(2,t)],'c':[(1,t),(2,t)]}}
    fin = open(filein,"r")
    title = filein.split("_")[0]
    for line in fin:
        words = line.split()
        for word in words: 
            ID = word[0]
            if ID in table:
                if word not in table[ID]:
                    table[ID][word] = [[1,title]]
                elif table[ID][word][-1][1] == title:
                    table[ID][word][-1][0] += 1
                else:
                    table[ID][word].append([1,title])
    
    fin.close()

def searchInvertedFiles(query,table):
    #Gets all words starting with the first letter of the query
    #then finds the word and returns the books related
    snowball = SnowballStemmer('english')
    query = snowball.stem(query)
    idTable = table[query[0].lower()]
    if query not in idTable:
        print "No Matches Found"
    else:
        wordOccurences = idTable[query]
        #sorts by most relevant
        wordOccurences.sort(key=lambda x: x[0])
        threshold = wordOccurences[-1][0]
        for i in range(len(wordOccurences)-1,-1,-1):
            if wordOccurences[i][0] >= threshold//2:
                print " " + wordOccurences[i][1] + " ", wordOccurences[i][0]

