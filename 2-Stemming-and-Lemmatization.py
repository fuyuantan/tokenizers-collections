# 1.regular expression

import re

text = "Hello, world! This is a test."
tokens = re.findall(r'\w+|[^\w\s]', text)
print(f"Tokens: {tokens}")


# convert to lowercase:

import re

text = "Hello, world! This is a test."
tokens = re.findall(r'\w+|[^\w\s]', text.lower())
print(f"Tokens: {tokens}")


# 2.stemming algorithm

import nltk
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

nltk.download('punkt_tab')  # download the necessary resources if haven't done so

text = "These models may become unstable quickly if not initialized."
stemmer = PorterStemmer()
words = word_tokenize(text)
stemmed_words = [stemmer.stem(word) for word in words]
print("stemming algorithm output:", stemmed_words)


# 3.Lemmatization
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

# download the necessary resources if haven't done so
nltk.download('wordnet')

text = "These models may become unstable quickly if not initialized."
lemmatizer = WordNetLemmatizer()
words = word_tokenize(text)
lemmatized_words = [lemmatizer.lemmatize(word) for word in words]
print("Lemmatization output:", lemmatized_words)