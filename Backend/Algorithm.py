import nltk
import math
from string import punctuation
from collections import Counter
from nltk.corpus import stopwords
from bs4 import BeautifulSoup

text1 = "<p>Die Change Tracker Tabelle in der Datenbank hat im Auslieferungszustand keine Indizes. Sobald die Tabelle w&auml;chst, "
text2 = "The Georgetown experiment in 1954 involved fully automatic translation of more than sixty Russian sentences into English. The authors claimed that within three or five years, machine translation would be a solved problem.[2] However, real progress was much slower, and after the ALPAC report in 1966, which found that ten-year-long research had failed to fulfill the expectations, funding for machine translation was dramatically reduced. Little further research in machine translation was conducted until the late 1980s, when the first statistical machine translation systems were developed."
text3 = "During the 1970s, many SAP SAP SAP SAP SAPprogrammers began to write conceptual ontologies, which structured real-world information into computer-understandable data. Examples are MARGIE (Schank, 1975), SAM (Cullingford, 1978), PAM (Wilensky, 1978), TaleSpin (Meehan, 1976), QUALM (Lehnert, 1977), Politics (Carbonell, 1979), and Plot Units (Lehnert 1981). During this time, many chatterbots were written including PARRY, Racter, and Jabberwacky。"


def get_tokens(text):
    tokens = nltk.word_tokenize(text)
    return tokens


def stem_tokens(tokens, stemmer):
    stemmed = []
    for item in tokens:
        stemmed.append(stemmer.stem(item))

    return stemmed


def tf(word, count):
    return count[word] / sum(count.values())


def n_containing(word, count_list):
    return sum(1 for count in count_list if word in count)


def idf(word, count_list):
    print(len(count_list))
    return math.log(1+ len(count_list)) / (1 + n_containing(word, count_list))


def tfidf(word, count, count_list):
    return tf(word, count) * idf(word, count_list)


def filter(text):
    soup = BeautifulSoup(text, 'html.parser')
    #print(soup)
    soup = soup.get_text()
    #print(soup)
    soup = ' '.join(word.strip(punctuation) for word in soup.split()
             if word.strip(punctuation))
    print(soup)
    tokens = get_tokens(soup)
    words = [w.lower() for w in tokens]
    filtered = [w for w in words if not w in stopwords.words('english')]
    count = Counter(filtered)
    return count


def generateTags(title, body):
    title1 = 'SAP SAP SAP SAP-Lumira, ,BI. wwww.ibSolution.de write do swim learn read why not is it ok to check on noun filtering'
    demo1 = 'SAP BI-Knowhow Links Links Links ' + title1

    text = title + ' ' + body
    countlist = []
    countlist.append(filter(text))#includes html parsing
    #print(countlist)
    stringTags = ''
    for i, count in enumerate(countlist):
        print("Top words in document {}".format(i + 1))
        scores = {word: tfidf(word, count, countlist) for word in count}
        #print(scores)
        sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        #print(sorted_words)
        tags = []
        if len(sorted_words) >= 5:
            for word, score in sorted_words[:5]:
                tags.append(word)
                stringTags = ', '.join(tags)
                print("\tWord: {}, TF-IDF: {}".format(word, score))
            print(tags)

        elif len(sorted_words) >= 3:
            for word, score in sorted_words[:2]:
                tags.append(word)
                stringTags = ', '.join(tags)
                print("\tWord: {}, TF-IDF: {}".format(word, score))

        elif len(sorted_words) >= 1:
            for word, score in sorted_words[:1]:
                tags.append(word)
                stringTags = ', '.join(tags)
                print("\tWord: {}, TF-IDF: {}".format(word, score))
        return stringTags

print(generateTags('', ''))