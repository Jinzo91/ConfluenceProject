import nltk
import math
import string
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from collections import Counter
from nltk.stem.porter import*
#nltk.download()
# nltk.download('punkt')
# nltk.download('stopwords')
from textblob import TextBlob

text1 = "<p>Die Change Tracker Tabelle in der Datenbank hat im Auslieferungszustand keine Indizes. Sobald die Tabelle w&auml;chst, "

text2 = TextBlob("The Georgetown experiment in 1954 involved fully automatic translation of more than sixty Russian sentences into English. The authors claimed that within three or five years, machine translation would be a solved problem.[2] However, real progress was much slower, and after the ALPAC report in 1966, which found that ten-year-long research had failed to fulfill the expectations, funding for machine translation was dramatically reduced. Little further research in machine translation was conducted until the late 1980s, when the first statistical machine translation systems were developed.")
text3 = "During the 1970s, many SAP SAP SAP SAP SAPprogrammers began to write conceptual ontologies, which structured real-world information into computer-understandable data. Examples are MARGIE (Schank, 1975), SAM (Cullingford, 1978), PAM (Wilensky, 1978), TaleSpin (Meehan, 1976), QUALM (Lehnert, 1977), Politics (Carbonell, 1979), and Plot Units (Lehnert 1981). During this time, many chatterbots were written including PARRY, Racter, and Jabberwacky。"

stopwords = set(stopwords.words("english"))
words = word_tokenize()

def get_tokens(text):
   lower = text.lower()
   remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)
   no_punctuation = lower.translate(remove_punctuation_map)
   tokens = nltk.word_tokenize(no_punctuation)

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
   return math.log(len(count_list)) / (1 + n_containing(word, count_list))


def tfidf(word, count, count_list):
   return tf(word, count) * idf(word, count_list)


def count_term(text):
   tokens = get_tokens(text)
   filtered = [w for w in tokens if not w in stopwords.words('english')]
   stemmer = PorterStemmer()
   stemmed = stem_tokens(filtered, stemmer)
   count = Counter(stemmed)
   return count

def main():
   texts = [text1, text2, text3]
   countlist = []
   for text in texts:
      countlist.append(count_term(text))
   for i, count in enumerate(countlist):
      print("Top words in document {}".format(i + 1))
      scores = {word: tfidf(word, count, countlist) for word in count}
      sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
      for word, score in sorted_words[:5]:
         print("\tWord: {}, TF-IDF: {}".format(word, round(score, 5)))

   #print(text2.tags)

if __name__ == "__main__":
   main()
