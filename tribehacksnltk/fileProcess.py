import nltk
from nltk.corpus import wordnet as wn

def isverb(word):
    tmp = ""
    for i in range(len(wn.synsets(word))):
        if wn.synsets(word)[i].pos() == "v":
            tmp = wn.synsets(word)[i].pos()
            break
        else:
            tmp = wn.synsets(word)[0].pos()
    if tmp == "v" :
        return True
    else :
        return False



def refineFile(filename):
    f = open(filename,"r",encoding= "utf-8")
    
    checkVerb = 0
    sentenceList = []
    sentence = ''
    refinedOutput = []
    paragraph = []
    taggedSentence = []


    for line in f:
        
        if line == '\n' or line.isupper():
            sentence = ''
 
            if paragraph != []:
                refinedOutput.append(paragraph)
                paragraph = []
                
        else:
                
            tokens = nltk.word_tokenize(line)
    
            for word in tokens:
        
                sentence = str(sentence) + ' ' + word
        
                if word == '.':
                    
                    sentenceTokens = nltk.word_tokenize(sentence)
                    for wordCheck in sentenceTokens:
                       
                        if isverb(wordCheck):
                            checkVerb += 1
                            break

                    sentence = ''
                    
                    if checkVerb >=1 and len(sentenceTokens) > 2:
                        paragraph.append(sentenceTokens)
                    
                    checkVerb = 0
                    sentenceTokens = []

    refinedOutput.append(paragraph)
    
    f.close()
    return refinedOutput
  