import nltk
import math
from string import punctuation
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from collections import Counter
from nltk.stem.porter import *
# nltk.download()
# nltk.download('punkt')
# nltk.download('stopwords')
from nltk.corpus import stopwords
from bs4 import BeautifulSoup
import re

text1 = "<p>Die Change Tracker Tabelle in der Datenbank hat im Auslieferungszustand keine Indizes. Sobald die Tabelle w&auml;chst, "
text2 = "The Georgetown experiment in 1954 involved fully automatic translation of more than sixty Russian sentences into English. The authors claimed that within three or five years, machine translation would be a solved problem.[2] However, real progress was much slower, and after the ALPAC report in 1966, which found that ten-year-long research had failed to fulfill the expectations, funding for machine translation was dramatically reduced. Little further research in machine translation was conducted until the late 1980s, when the first statistical machine translation systems were developed."
text3 = "During the 1970s, many SAP SAP SAP SAP SAPprogrammers began to write conceptual ontologies, which structured real-world information into computer-understandable data. Examples are MARGIE (Schank, 1975), SAM (Cullingford, 1978), PAM (Wilensky, 1978), TaleSpin (Meehan, 1976), QUALM (Lehnert, 1977), Politics (Carbonell, 1979), and Plot Units (Lehnert 1981). During this time, many chatterbots were written including PARRY, Racter, and Jabberwacky。"


def get_tokens(text):
    # lower = text.lower()
    # remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)
    # no_punctuation = lower.translate(remove_punctuation_map)
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
    print(soup)
    soup = ' '.join(word.strip(punctuation) for word in soup.split()
             if word.strip(punctuation))
    print(soup)
    #print(re.findall(r"\w+(?:[-']\w+)*|'|[-.(]+|\S\w*", soup))
    tokens = get_tokens(soup)
    words = [w.lower() for w in tokens]
    filtered = [w for w in words if not w in stopwords.words('english')]
    count = Counter(filtered)
    return count


def generateTags(title, body):
    title1 = 'SAP SAP SAP SAP-Lumira, ,BI. wwww.ibSolution.de write do swim learn read why not is it ok to check on noun filtering'
    texts1 = """<p style="text-align: center;">&nbsp;</p><p><span style="color: rgb(153,153,153);"><br /></span></p><h2><ac:image><ri:attachment ri:filename="welcome.png" /></ac:image><br />&nbsp; <span style="color: rgb(128,128,128);">With Confluence it is easy to create, edit and share content with your team. <br />&nbsp; Choose a topic below to start learning how.</span></h2><h2><span style="color: rgb(0,0,128);"><br /></span></h2><ol><li><span style="color: rgb(0,0,128);"><ac:link><ri:page ri:content-title="What is Confluence? (step 1 of 9)" /><ac:link-body>What is Confluence?<br /><br /></ac:link-body></ac:link></span></li><li><span style="color: rgb(0,0,128);"><ac:link><ri:page ri:content-title="A quick look at the editor (step 2 of 9)" /><ac:plain-text-link-body><![CDATA[A quick look at the editor]]></ac:plain-text-link-body></ac:link><br />&nbsp;</span></li><li><span style="color: rgb(0,0,128);"><ac:link><ri:page ri:content-title="Let's edit this page (step 3 of 9)" /><ac:plain-text-link-body><![CDATA[Let's edit this page]]></ac:plain-text-link-body></ac:link><br /><br /></span></li><li><span style="color: rgb(0,0,128);"><ac:link><ri:page ri:content-title="Prettify the page with an image (step 4 of 9)" /><ac:link-body>Prettify the page with an image<br /><br /></ac:link-body></ac:link></span></li><li><span style="color: rgb(0,0,128);"><ac:link><ri:page ri:content-title="Get serious with a table (step 5 of 9)" /><ac:link-body>Get serious with a table<br /></ac:link-body></ac:link></span><span style="color: rgb(0,0,128);">&nbsp;</span></li><li><span style="color: rgb(0,0,128);"><ac:link><ri:page ri:content-title="Lay out your page (step 6 of 9)" /><ac:plain-text-link-body><![CDATA[Lay out your page]]></ac:plain-text-link-body></ac:link>&nbsp;<br /><br /></span></li><li><ac:link><ri:page ri:content-title="Learn the wonders of autoconvert (step 7 of 9)" /><ac:plain-text-link-body><![CDATA[Learn the wonders of autoconvert]]></ac:plain-text-link-body></ac:link>&nbsp;<br /><br /></li><li><ac:link><ri:page ri:content-title="Tell people what you think in a comment (step 8 of 9)" /><ac:plain-text-link-body><![CDATA[Tell people what you think in a comment]]></ac:plain-text-link-body></ac:link>&nbsp;<br /><br /></li><li><ac:link><ri:page ri:content-title="Share your page with a team member (step 9 of 9)" /><ac:plain-text-link-body><![CDATA[Share your page with a team member]]></ac:plain-text-link-body></ac:link></li></ol><p><span style="color: rgb(128,128,128);"><br /></span></p><p><span style="color: rgb(128,128,128);"><br /></span></p><p><span style="color: rgb(128,128,128);"><br /></span></p><p><span style="color: rgb(128,128,128);"><br /></span></p><p><span style="color: rgb(128,128,128);"><br /></span></p><p style="text-align: right;">&nbsp; &nbsp; &nbsp;&nbsp;</p>"""
    texts2 = title1 +' '+ """<p><ac:link><ri:page ri:content-title="Change Tracker" /><ac:plain-text-link-body><![CDATA[Change Tracker]]></ac:plain-text-link-body></ac:link></p>"""
    demo1 = 'SAP BI-Knowhow Links Links Links'

    text = title + ' ' + body
    countlist = []
    countlist.append(filter(demo1))#includes html parsing
    print(countlist)

    for i, count in enumerate(countlist):
        print("Top words in document {}".format(i + 1))
        print({word: tf(word, count) for word in count})
        print({word: idf(word, countlist) for word in count})
        scores = {word: tfidf(word, count, countlist) for word in count}
        print(scores)
        sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        print(sorted_words)
        tags = []
        if len(sorted_words) >= 5:
            for word, score in sorted_words[:5]:
                tags.append(word)
                print("\tWord: {}, TF-IDF: {}".format(word, score))
        elif len(sorted_words) >= 3:
            for word, score in sorted_words[:3]:
                tags.append(word)
                print("\tWord: {}, TF-IDF: {}".format(word, score))

generateTags('', '')