import nltk
import math
from string import punctuation
from collections import Counter
from nltk.corpus import stopwords
from bs4 import BeautifulSoup
nltk.download('punkt')
nltk.download('stopwords')


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
    return math.log(1+ len(count_list)) / (1 + n_containing(word, count_list))


def tfidf(word, count, count_list):
    return tf(word, count) * idf(word, count_list)


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


def generateTags(title, body):
    text = title + ' ' + body
    countlist = []
    countlist.append(filter(text))#includes html parsing
    stringTags = ''
    for i, count in enumerate(countlist):
        print("Top words in document:")
        scores = {word: tfidf(word, count, countlist) for word in count}
        sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        tags = []
        if len(sorted_words) >= 5:
            for word, score in sorted_words[:5]:
                if len(word) > 1:
                    tags.append(word)
                    stringTags = ', '.join(tags)
                    print("\tWord: {}, TF-IDF: {}".format(word, score))

        elif len(sorted_words) >= 3:
            for word, score in sorted_words[:2]:
                if len(word) > 1:
                    tags.append(word)
                    stringTags = ', '.join(tags)
                    print("\tWord: {}, TF-IDF: {}".format(word, score))

        elif len(sorted_words) >= 1:
            for word, score in sorted_words[:1]:
                if len(word) > 1:
                    tags.append(word)
                    stringTags = ', '.join(tags)
                    print("\tWord: {}, TF-IDF: {}".format(word, score))
        return stringTags