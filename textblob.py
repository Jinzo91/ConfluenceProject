# create TextBlob
import imp
from textblob import TextBlob
from textblob import Word
from textblob.wordnet import VERB


wiki = TextBlob(open(file.txt).read())
'''wiki = TextBlob(wiki)'''

# part of speech tagging
wiki.tags

# Noun Phrase extraction
wiki.noun_phrases

# Sentiment Analysis
wiki.Sentiment

# Tokenization
wiki.words
wiki.sentences

# Words Inflection and Lemmatization
wiki.words  # wordList
wiki.words[2].singularize()
wiki.words[-1].pluralize()

# lemmatize method
text1 = Word(wiki)
text1.lemmatize()
text1.lemmatize("v")    # Pass in WordNet part of speech (verb)

# definitions
text1.words[].definitions

# Spelling Correction
print(wiki.correct())

Word("type_word").spellcheck()  # spellcheck

# Word or Phrase Frequcy
wiki.word_count['type_word or Phrase']
wiki.words.count('type_word or Phrase', case_sensitive=True)     # case sensitive result

wiki.noun_phrases.count(' type_word or Phrase')

# Translation and language Detection
en_blob = TextBlob(" file.txt")
en_blob.detect_language()
en_blob.translate(from_lang=" " , to='es')

# Parsing
b = TextBlob("file.txt")
b[0:16]
b.upper()
b.find("write_text")

# n-grams
b = Textblob("file.txt")
b.ngrams(n=3)

# Loading data and creating Classifier

from textblob.classifiers import NaiveBayesClassifier
with open ('train.jason', 'r') as fp:
    cl = NaiveBayesClassifier(fp, format='jason')
