import re
import string
from nltk import word_tokenize
from nltk.stem.porter import PorterStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords
from collections import Counter

def remove_unicode_chars(text):
    unicode_removed = re.sub(r'[^\x00-\x7f]',r' ', text)
    unicode_removed = unicode_removed.encode('ascii','ignore')
    return unicode_removed

def split_hyphenated_words(text):
    dehyphenated_text = re.sub(r"[^\w\s]", " ", text)
    return dehyphenated_text

def tokenize_words(unicode_removed):
    print("tokenizing words...")
    tokenyzed = word_tokenize(unicode_removed)
    tokenyzed_cleaned = [re.sub(r'[^a-zA-Z]', ' ', x) for x in tokenyzed]
    tokenyzed_cleaned = convert_to_lowercase(tokenyzed_cleaned)
    tokenyzed_cleaned = [x.strip() for x in tokenyzed_cleaned]
    tokenyzed_cleaned = [word for word in tokenyzed_cleaned if word != ""]
    print(cal_word_frequency(tokenyzed_cleaned, 10))
    return tokenyzed_cleaned

def remove_stop_words(tokenyzed_cleaned):
    print("removing stop words...")
    exclude = set(string.punctuation)
    stop = set(stopwords.words('english'))
    exclude.update(["``", "''"])
    stop_free = [word for word in tokenyzed_cleaned if (word not in stop) and (not word.isdigit())]
    punc_free = [word for word in stop_free if word not in exclude]
    ascii_words =  punc_free
    return ascii_words

def convert_to_lowercase(all_cases):
    lowercased = [word.lower() for word in all_cases]
    return lowercased

def lemmatize_words(ascii_ls):
    lemma = WordNetLemmatizer()
    normalized = [lemma.lemmatize(word) for word in ascii_ls]


    porter = PorterStemmer()
    stemmed_text = [porter.stem(token) for token in normalized]
    stemmed_ascii = [x.encode('ascii','ignore').lower() for x in stemmed_text]
    return stemmed_ascii

def cal_word_frequency(stemmed_ascii, n_most_common):
    counts = Counter(stemmed_ascii)
    return counts.most_common(n_most_common) 


