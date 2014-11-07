########################################################################
# Miguel Melchor
# search.py
# Main file for asking user for query and searching
########################################################################

import sys
from clean import*
from invertedFiles import*
from phraseSearch import*


if __name__ == '__main__':

    os.chdir("/home/Miguel/Linguistics/FinalProject/Information Retrieval/books")
    save_path = "/home/Miguel/Linguistics/FinalProject/Information Retrieval/filtered"

    keywordsTable = createHashTable()
    biPhraseTable = createHashTable()

    changes = False
    
    #cleans all files
    done = os.listdir(save_path)
    for file in os.listdir(os.getcwd()):
        if file.endswith(".txt"):
            name = file[:-4]+"_clean.txt"
            if name not in done:
                print file + " added"
                completeName = os.path.join(save_path,name)
                filterFile(file,completeName)

              
    #creates keywords for inverted algorithm and for bigrams
    os.chdir("/home/Miguel/Linguistics/FinalProject/filtered")
    for file in os.listdir(os.getcwd()):
        createKeywords(file,keywordsTable)
        createBigrams(file,biPhraseTable)

    #takes queries and returns results until user is #DONE
    query = raw_input("MMS: ")
    while query != "//":
        if query[:5].lower() == 'title':
            name = query[6:].lower()
            for file in os.listdir(os.getcwd()):
                temp = file.lower()
                if name in temp:
                    print " " + file.split("_")[0]
        elif len(query.split()) == 1:
            searchInvertedFiles(query,keywordsTable)
            
        elif len(query.split()) == 2:
            phraseSearch(query,biPhraseTable,keywordsTable)
            
        elif len(query.split()) > 2 or len(query.split()) == 0:
            print "Error: Max of 2 keywords at least 1"  
        query = raw_input("MMS: ")
