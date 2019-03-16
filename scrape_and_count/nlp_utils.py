import re
import string
from nltk import word_tokenize
from nltk.stem.porter import PorterStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords
from collections import Counter

def remove_unicode_chars(text):
    print("============ remove unicode characters =============")
    # printable = set(string.printable)
    # unicode_removed = filter(lambda x: x in printable, text)
    unicode_removed = re.sub(r'[^\x00-\x7f]',r' ', text)
    # print(unicode_removed)
    unicode_removed = unicode_removed.encode('ascii','ignore')
    print(type(unicode_removed))
    print(len(unicode_removed))
    return unicode_removed

def split_hyphenated_words(text):
    # print(text)
    dehyphenated_text = re.sub(r"[^\w\s]", " ", text)
    # split_text = text.translate(None, string.punctuation)
    return dehyphenated_text

def tokenize_words(unicode_removed):
    print("============= tokenize words ===============")
    tokenyzed = word_tokenize(unicode_removed)
    # tokenyzed = tokenyzed.rstrip()
    tokenyzed_cleaned = [x.strip() for x in tokenyzed]
    # print(tokenyzed[0:5])
    print(len(tokenyzed))
    # print(tokenyzed_cleaned)
    print(type(tokenyzed_cleaned))
    print(len(tokenyzed_cleaned))
    # ascii2 = remove_non_ascii(text)
    return tokenyzed_cleaned

def remove_stop_words(tokenyzed_cleaned):
    # ------------------------- remove stop words ----------------------------
    print("=========== remove stop words =============")


    exclude = set(string.punctuation)
    stop = set(stopwords.words('english'))
    # print("stop words are:")
    # print(stop)
    exclude.update(["``", "''"])
    stop_free = [word for word in tokenyzed_cleaned if word not in stop]
    punc_free = [word for word in stop_free if word not in exclude]

    # print(punc_free)
    # print(len(punc_free))
    # print(punc_free[0:10])
    # print(type(punc_free))

    ascii_ls =  punc_free # [x.encode('ascii','ignore').lower() for x in punc_free]
    # print(type(ascii_ls))
    # print(type(ascii_ls[0]))
    # print(len(ascii_ls))
    # print(ascii_ls[0:10])
    # print("-----------------------------")
    return ascii_ls

# lowercase_words ==>  convert_to_lowercase
def convert_to_lowercase(all_cases):
    lowercased = [word.lower() for word in all_cases]
    return lowercased

def lemmatize_words(ascii_ls):
    # ------------------ lemmatize words ----------------------
    print("=========== lemmatize words ===========")
    
    lemma = WordNetLemmatizer()
    normalized = [lemma.lemmatize(word) for word in ascii_ls]


    porter = PorterStemmer()
    stemmed_text = [porter.stem(token) for token in normalized]
    stemmed_ascii = [x.encode('ascii','ignore').lower() for x in stemmed_text]
    return stemmed_ascii

def cal_word_frequency(stemmed_ascii, n_most_common):
    # -------------------- word frequency ----------------------
    counts = Counter(stemmed_ascii)
    return counts.most_common(n_most_common) 


