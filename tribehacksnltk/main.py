
import nltk
from nltk.stem import WordNetLemmatizer
import nltk.data
import nltk.grammar
import fileProcess
from nltk.corpus import wordnet as wn

wordnet_lemmatizer = WordNetLemmatizer()

def isverb(word):
    tmp = ""
    for i in range(len(wn.synsets(word))):
        if wn.synsets(word)[i].pos() == "v":
            tmp = wn.synsets(word)[i].pos()
            break
        else:
            tmp = wn.synsets(word)[0].pos()
    # print (word, ":", tmp)
    if (tmp == "v"):
        return True
    else:
        return False


def removeAdSuf(word):
    adjsuf = ["al", "ary", 'ful', 'ic', 'ical', 'ish', 'less', 'like', 'ly', 'ous', 'y', 'able', 'ible', 'ant',
              'ent', 'ive', 'ing', 'ed', 'en']
    mystr = ""

    for suf in adjsuf:
        if suf in word[len(word)-len(suf):]:
            li = word.rsplit(suf, 1)
            mystr = "".join(li)
            break
    return (mystr)

def multi_verb(tokens,pos_tag_tokens):
    for i in range(len(tokens)):
        if (tokens[i] == ',') and (tokens[i+1] == 'and') and ("V" in pos_tag_tokens[i+2][1]):
            return True
        elif (tokens[i] == 'and') and ("V" in pos_tag_tokens[i+1][1]):
            return True
    return False

def multi_clause(tokens,pos_tag_tokens):
    for i in range(len(tokens)):
        if (tokens[i-2] == ',') and (tokens[i] in ['and','but','or','yet','for','nor','so'])\
                and ("N" in pos_tag_tokens[i + 1][1]):
            return i
        elif (tokens[i] == ';'):
            return i
    return 0

def read_file(filename):
    result = []
    file = open(filename,"r")
    for line in file:
        linevalues = line.split(',')
        result.append(linevalues)
    file.close()
    return result

def word_tagger(parnum,sennum,tokens):
    result = [str(parnum),str(sennum), [], [], [], []]
    verb_flag = False
    firstverbindex = 0
    pos_tag_tokens = nltk.pos_tag(tokens)
    actverbindex = []
    multiclause = multi_clause(tokens,pos_tag_tokens)

    if multiclause != 0:
        sec_clause = word_tagger(parnum, sennum, tokens[multiclause + 1:])
        tokens = tokens[0:multiclause]

    for i in range(len(tokens)):
        word = tokens[i]

        base_form = wordnet_lemmatizer.lemmatize(word, "v")
        base_formremov =removeAdSuf(base_form)
        base_form2 = wordnet_lemmatizer.lemmatize(removeAdSuf(base_form), 'v')
        if word.title() == word and verb_flag == False and word[0].lower() in "qwertyuiopasdfghjklzxcvbnm":
            result[2].append(word)
        elif isverb(base_form):
            result[3].append(base_form)
            if verb_flag == False:
                firstverbindex = tokens.index(word)
            verb_flag = True
        elif ("MD" in nltk.pos_tag(nltk.word_tokenize(word))[0][1] or
            "RB" in nltk.pos_tag(nltk.word_tokenize(word))[0][1]) and (verb_flag == False):
            firstverbindex = tokens.index(word)
            verb_flag = True
            continue
        elif isverb(base_formremov):
            result[3].append(base_formremov)
            if not verb_flag:
                firstverbindex = tokens.index(word)
            verb_flag = True
        elif isverb(base_formremov + 'e'):
            result[3].append(base_formremov + 'e')
            if not verb_flag:
                firstverbindex = tokens.index(word)
            verb_flag = True
        elif isverb(base_form2):
            result[3].append(base_form2)
            if not verb_flag:
                firstverbindex = tokens.index(word)
            verb_flag = True

        else:
            if not verb_flag:
                result[2].append(word)

    pos_tag_tokens = nltk.pos_tag(tokens)

    multiverb = multi_verb(tokens,pos_tag_tokens)

    verb_flag = False

    if multiverb:
        for i in range(len(tokens)):
            base_form = wordnet_lemmatizer.lemmatize(tokens[i], 'v')

            if base_form in ["have", "be"]:
                if "V" not in pos_tag_tokens[i + 1][1]:
                    result[4].append(base_form)
                    actverbindex.append(i)
                    # tokens.remove(tokens[i])
                else:
                    result[4].append(wordnet_lemmatizer.lemmatize(tokens[i+1],'v'))
                    actverbindex.append(i+1)

            elif tokens[i-1] == ',' and ("V" in pos_tag_tokens[i][1]):
                result[4].append(base_form)
                actverbindex.append(i)

            elif tokens[i-2] == ',' and (tokens[i-1] == "and") and ("V" in pos_tag_tokens[i][1]):
                result[4].append(base_form)
                actverbindex.append(i)
                break
            elif tokens[i-1] == 'and' and ("V" in pos_tag_tokens[i][1]):
                result[4].append(base_form)
                actverbindex.append(i)

    else:
        for i in range(len(tokens)):
            base_form = wordnet_lemmatizer.lemmatize(tokens[i],'v')
            if "V" in pos_tag_tokens[i][1]:
                if base_form in ["have","be"]:
                    if "V" not in pos_tag_tokens[i+1][1]:
                        result[4].append(base_form)
                        actverbindex.append(i)
                        break
                    else:
                        continue
                elif pos_tag_tokens[i][1] in ["VBD","VBG","VBN"] and \
                    (wordnet_lemmatizer.lemmatize(tokens[i-1],'v') not in ["have","be"]):
                    continue
                elif not result[2] == [] and i >= 1:
                    result[4].append(base_form)
                    actverbindex.append(i)
                    break
            elif "V" in nltk.pos_tag([base_form])[0][1] and i >= 1:
                result[4].append(base_form)
                actverbindex.append(i)
                break


    actverbindex.sort(reverse=True)
    for index in actverbindex:
        tokens.pop(index)

    for i in range(firstverbindex):
        tokens.pop(0)

    remainder = " ".join(tokens)
    result[5].append(remainder)
    if multiclause != 0:
        for i in range(4):
            for word in sec_clause[i+2]:
                result[i+2].append(word)
    print (pos_tag_tokens)
    return result


def docanalyze(inputfile,outputfile,table):
    outputfile.write("Para. #, Sent. #, Subject, Verbs, Actual Verbs, Remaining, "
                     "Ctg.#1, Ctg.#2, Ctg.#3, Ctg.#4, Ctg.#5, Ctg.#6, Ctg.#7\n")
    for i in range(len(inputfile)):
        verblist = []
        for j in range(len(inputfile[i])):
            actverb_tableindexs = []
            tagged_output = word_tagger(i+1,j+1,inputfile[i][j])

            for actverb in tagged_output[4]:
                for l in range(len(table)):
                    if actverb.title() == table[l][0].replace(' ',''):
                        if actverb not in verblist:
                            actverb_tableindexs.append(l)
                            verblist.append(actverb)

            for m in range(7):
                tagged_output.append(0)
                for index in actverb_tableindexs:
                    tagged_output[-1] += int(table[index][m+1].replace("\n",'',1))

                tagged_output[-1] = str(tagged_output[-1])

            print(tagged_output)

            tagged_output_str = ""

            for o in range(2,7):
                tagged_output[o] = " ".join(tagged_output[o])
                tagged_output[o] = tagged_output[o].replace(", ","")
            for thing in tagged_output:
                tagged_output_str += ', ' + str(thing)
            tagged_output_str = tagged_output_str.replace(", ","",1)
            outputfile.write(tagged_output_str + "\n")

    outputfile.close()

if __name__ == "__main__":
    inputfile = fileProcess.refineFile("input.txt")
    outputfile = open("output.csv","w")
    table = read_file("table1.csv")

    docanalyze(inputfile,outputfile,table)
