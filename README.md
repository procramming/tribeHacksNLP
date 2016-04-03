# tribeHacksNLP
Natural Language Processing

##Inspiration
This project was inspired by the concept of implementing Natural Language Processing (NLP) and string searching algorithms. It mainly aimed towards to solve Logapps LLC's challenge to extract Key Words from the given input .txt file. In this process, The Natural Language Toolkit (NLTK) allows symbolic and statistical NLP for the Python programming. NLP has a huge potential in a direct real-world application in many different fields, including linguistics, cognitive science, artificial intelligence, and machine learning.

##What it does
Our program takes a .txt file as an input and extracts sentence structures,including subject, verbs, actual verbs, and objects (remaining), from each sentence. Here, actual verbs mean verbs that actually carry meanings in a sentence. For example, in a sentence "she is loved," subject is "she," verb is"be," and actual verb is "love." Furthermore, using the given table of Key Word scores, the program also presents the sum of Key Word score of each sentence. Finally, the program arranges collected data in .csv file output.

##How we built it
After reading and decomposing the paragraphs and sentences, it detects words from a sentence and convert each of them to its base form. Then each word is passed into appropriate functions ,verb passed into _ isVerb_ , to determine the correct form. In this process, it is important to distinguish noun-adjectives(ex. skillful) and verb-adjectives(ex. agreeable) from regular noun, verb, and adjective. To solve this problem, the program checks if the adjective suffix is in the word.

#Simplified algorithm flowcharts are also attached above.

##Challenges we ran into
Enabling computers to derive meanings of human language was the biggest challenge. English sentences are not always as clear as "subject-verb-objective," and enabling program to handle exceptions and extracting the word was complicated. In addition, imperfection of NLP library, such as detecting the word "seamless" as a verb instead of an adjective made it hard to correctly categorize the words.

##Accomplishments that we're proud of
The program demonstrates exceptionally high accuracy in extracting verbs and distinguishing actual verbs from regular verbs by handling various special cases thoroughly. For example, when a sentence contains several verbs linked by commas, it successfully detects all of the actual verbs. It also effectively extracts base nouns and verbs from adjective combinations without break the verb form, which is important as stemming function often modify the verb. Careful handlings on special cases improved the accruracy.

##What we learned
This project was challenging as none of the team members had prior knowledge in NLP. However, it only gave us more chance to learn about NLP and python programming. It was pretty impressive to see how difficult it is to solve the interaction between computers and natural human language.

##What's next for NLP (Natural Language Processing)
NLP program can be extended to many different directions. One of the key development points is to enhance the accuracy and be able to handle different exceptions in English sentence structure. The program can also be developed to handle sentence structures in different languages.

#Built With
python

natural-language-processing

nltk
