import nltk
import math
from string import punctuation
from collections import Counter
from nltk.corpus import stopwords
from bs4 import BeautifulSoup
nltk.download('punkt')
nltk.download('stopwords')


#Tokenizer for text.
def get_tokens(text):
    tokens = nltk.word_tokenize(text)
    return tokens

#Stemmer for tokenized text.
def stem_tokens(tokens, stemmer):
    stemmed = []
    for item in tokens:
        stemmed.append(stemmer.stem(item))

    return stemmed

#Term frequencey of a word in a single text
def tf(word, count):
    return count[word] / sum(count.values())

#Adds 1 if a word appears in a text, e.g. a word appears in 2 documents -> sum = 2
def n_containing(word, count_list):
    return sum(1 for count in count_list if word in count)

#Inverse document frequency to weigh down frequent words like verbs etc.
def idf(word, count_list):
    return math.log(1+ len(count_list)) / (1 + n_containing(word, count_list))

#TF-IDF algorithm to evaluate the importance of a word inside documents.
def tfidf(word, count, count_list):
    return tf(word, count) * idf(word, count_list)

#Preprocessing of documents, e.g. parses HTML text to normal text,
#filters punctuation, filters German and English stopwords.
def filter(text):
    soup = BeautifulSoup(text, 'html.parser')
    soup = soup.get_text()
    soup = ' '.join(word.strip(punctuation) for word in soup.split()
             if word.strip(punctuation))
    tokens = get_tokens(soup)
    words = [w.lower() for w in tokens]
    filtered = [w for w in words if not w in stopwords.words('english')]
    filtered = [w for w in filtered if not w in stopwords.words('german')]
    count = Counter(filtered)
    return count

#Tag generation using TF-IDF based on the document title and content.
def generateTags(title, body):
    text = title + ' ' + body
    countlist = []
    countlist.append(filter(text))#preprocessing, includes html parsing
    stringTags = ''
    #Iterates through the combined text
    for i, count in enumerate(countlist):
        print("Top words in document:")
        #Calculate the TF-IDF
        scores = {word: tfidf(word, count, countlist) for word in count}
        sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        tags = []
        #Decide how long the list for possible tag-words are and return only the top tags
        if len(sorted_words) >= 5:
            for word, score in sorted_words[:5]:
                if len(word) > 1:
                    tags.append(word)
                    stringTags = ', '.join(tags)
                    print("\tWord: {}, TF-IDF: {}".format(word, score))
        #Special case, e.g. if document has no content, only short title
        elif len(sorted_words) >= 3:
            for word, score in sorted_words[:2]:
                if len(word) > 1:
                    tags.append(word)
                    stringTags = ', '.join(tags)
                    print("\tWord: {}, TF-IDF: {}".format(word, score))
        #Special case, e.g. if document has no content, only 1 word title
        elif len(sorted_words) >= 1:
            for word, score in sorted_words[:1]:
                if len(word) > 1:
                    tags.append(word)
                    stringTags = ', '.join(tags)
                    print("\tWord: {}, TF-IDF: {}".format(word, score))
        return stringTags