from bs4 import BeautifulSoup
from bs4.element import Comment
from bs4 import NavigableString
import urllib 
import requests
import re
from nltk import word_tokenize
import string
from unidecode import unidecode


def get_all_tag_names(soup):
    names = set() 
    for tag in soup.find_all(True):
        names.add(tag.name)
    return names

def get_selected_tags(soup):
    tags = get_all_tag_names(soup) #[u'code', u'h2', u'h3', u'h1', u'meta', u'table', u'label', u'noscript', u'style', u'span', u'img', u'script', u'tr', u'tbody', u'li', u'html', u'th', u'sup', u'input', u'td', u'cite', u'body', u'head', u'form', u'ol', u'link', u'abbr', u'br', u'caption', u'a', u'b', u'wbr', u'i', u'title', u'q', u'p', u'div', u'ul']
    ignore_tags = ['style', 'script', 'head', 'meta', 'noscript'] 
    for tag in ignore_tags:
        if tag in tags:
            tags.remove(tag)
    return tags

def get_screen_text(soup):
    all_visible_text = []
    tags = get_selected_tags(soup) 
    # tags = get_tag_names(soup) #[u'code', u'h2', u'h3', u'h1', u'meta', u'table', u'label', u'noscript', u'style', u'span', u'img', u'script', u'tr', u'tbody', u'li', u'html', u'th', u'sup', u'input', u'td', u'cite', u'body', u'head', u'form', u'ol', u'link', u'abbr', u'br', u'caption', u'a', u'b', u'wbr', u'i', u'title', u'q', u'p', u'div', u'ul']
    # ignore_tags = ['style', 'script', 'head', 'meta'] 
    # for tag in ignore_tags:
    #     if tag in tags:
    #         tags.remove(tag)
    for tag in tags:
        all_visible_text = all_visible_text + get_direct_descendant_text(soup, tag)
    return all_visible_text

def get_direct_descendant_text(soup, tag):
    immediate_descendant_text = []
    contents = soup.findAll(tag)
    for content in contents:
        immediate_descendant_text = immediate_descendant_text + [el for el in content.children if isinstance(el, NavigableString)]
    return immediate_descendant_text

def get_text_from_tag_expanded(tag, texts, selected_tags):
    # print(tag)
    # print(selected_tags)
    if tag.name in selected_tags:
        # print("HERE!")
        if isinstance(tag, type(None)): 
            # return (None, texts)
            pass
        elif isinstance(tag, NavigableString):
            texts.append(tag.string)
            # return (None, texts)
        else:
            for child in tag.children:
                # print("examinging child {}".format(child.name))
                if isinstance(child, NavigableString):
                    # print(u"{} is a NavigableString\n".format(child))
                    texts.append(child.string)
                elif (child.name == "table") and child.has_attr("class") and ("autocollapse" in child['class']):
                    # print("{} is a autocollapsed table\n".format(child.name))
                    tr_to_keep = child.tbody.find("tr")

                    # print("--------- tr_to_keep --------")
                    # print(tr_to_keep)
                    actual_list_of_text = get_screen_text(tr_to_keep)
                    # print("=========== text from table ===========")
                    # print(actual_list_of_text)
                    # print("=========== texts before ===========")
                    for elt in actual_list_of_text:
                        texts.append(elt)
                    # texts = texts + actual_list_of_text 
                    # print("=========== texts after ===========")
                    # print(texts)
                # elif child.name == "a" and not child.has_attr("title"):
                #     print("{} is an a tag without a title attribute\n".format(child.name)) 
                #     continue
                else:
                    # print("{} is a normal tag\n".format(child.name))
                    if child.contents != None:
                        get_text_from_tag_expanded(child, texts, selected_tags)
                        # print("new_tag is {}".format(new_tag))
            # return (None, texts)
    # else:
        # return (None, texts)




def tag_visible(element):
    # print(element)
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    # if element.a['class'] in ["mw-jump-link"]:
    #     return False
    # else:
    #     print(element.a["class"])
    if isinstance(element, Comment):
        return False
    return True

# def not_a_jump_link(css_class):
#     print(css_class)
#     if css_class != "mw-jump-link":
#         return True
#     else:
#         return False

def text_from_html(body):
    soup = BeautifulSoup(body, 'html5lib')
    texts = soup.findAll(text=True)
    # filtered_class = []
    # for p in texts:
    #     print(p)
    #     if p.find({"class": "mw-jump-link"}):
    #         continue
    #     else:
    #         filtered_class.append(p)
    # print(texts)
    visible_texts = filter(tag_visible, texts)
    # return re.sub(r'^a-zA-Z]', ' ', u"".join(t.strip() for t in visible_texts))
    return u" ".join(t.strip() for t in visible_texts)
    # cleaned_texts = [x for x in visible_texts]
    # return visible_texts

def text_from_html2(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)

    # visible_texts = filter(tag_visible, texts)
    # return re.sub(r'^a-zA-Z]', ' ', u"".join(t.strip() for t in visible_texts))
    return u" ".join(t.strip() for t in texts)
    # cleaned_texts = [x for x in visible_texts]
    # return visible_texts

def remove_non_ascii(text):
    # return unidecode(unicode(text, encoding = "utf-8"))
    pass

def get_text_from_html(url='https://en.wikipedia.org/wiki/Python_(programming_language'):
    print("=========== get text from HTML =============")
    html = urllib.urlopen(url).read()
    text = text_from_html(html)
    print(type(text))
    print(len(text))
    # print(text[0:6000])
    return text


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
    print(tokenyzed[0:5])
    print(len(tokenyzed))
    # print(tokenyzed_cleaned)
    print(type(tokenyzed_cleaned))
    print(len(tokenyzed_cleaned))
    # ascii2 = remove_non_ascii(text)
    return tokenyzed_cleaned


def remove_stop_words(tokenyzed_cleaned):
    # ------------------------- remove stop words ----------------------------
    print("=========== remove stop words =============")
    from nltk.corpus import stopwords

    exclude = set(string.punctuation)
    stop = set(stopwords.words('english'))
    # print("stop words are:")
    # print(stop)
    # print("excluding:")
    # print(exclude)
    exclude.update(["``", "''"])
    # print("excluding:")
    # print(exclude)
    stop_free = [word for word in tokenyzed_cleaned if word not in stop]
    punc_free = [word for word in stop_free if word not in exclude]

    # print(punc_free)
    print(len(punc_free))
    print(punc_free[0:10])
    print(type(punc_free))

    ascii_ls =  punc_free # [x.encode('ascii','ignore').lower() for x in punc_free]
    print(type(ascii_ls))
    print(type(ascii_ls[0]))
    print(len(ascii_ls))
    print(ascii_ls[0:10])
    print("-----------------------------")
    return ascii_ls

def lowercase_words(all_cases):
    lowercased = [word.lower() for word in all_cases]
    return lowercased

def lemmatize_words(ascii_ls):
    # ------------------ lemmatize words ----------------------
    print("=========== lemmatize words ===========")
    from nltk.stem.wordnet import WordNetLemmatizer
    lemma = WordNetLemmatizer()
    normalized = [lemma.lemmatize(word) for word in ascii_ls]

    from nltk.stem.porter import PorterStemmer
    porter = PorterStemmer()
    stemmed_text = [porter.stem(token) for token in normalized]
    stemmed_ascii = [x.encode('ascii','ignore').lower() for x in stemmed_text]
    return stemmed_ascii


def cal_word_frequency(stemmed_ascii):
    # -------------------- word frequency ----------------------
    from collections import Counter
    import numpy as np
    # import matplotlib.pyplot as plt

    counts = Counter(stemmed_ascii)

    labels, values = zip(*counts.items())

    # sort your values in descending order
    indSort = np.argsort(values)[::-1]

    # rearrange your data
    labels = np.array(labels)[indSort]
    values = np.array(values)[indSort]

    # print(ascii_ls)
    # print(labels[0:10])
    # print(values[0:10])
    count = 0
    for word, value in zip(labels, values):
        print("{}: {}".format(word, value))
        if count < 10:
            count+=1
        else:
            break
    return ((labels[0], values[0]))


# text = get_text_from_html()
# ascii_text = remove_unicode_chars(text)
# tokenized_clean = tokenize_words(ascii_text)
# words_col = remove_stop_words(tokenized_clean)
# lemmatized = lemmatize_words(words_col)
# cal_word_frequency(lemmatized)

def get_html_body(base_url):
    r = requests.get(base_url)
    soup = BeautifulSoup(r.text, 'html.parser')
    print(soup.prettify())
    with open("prettified_wiki_python.txt", "w") as textfile:
        textfile.write(soup.prettify().encode('utf8'))

base_url = "https://en.wikipedia.org/wiki/Python_(programming_language)"
# get_html_body(base_url)

def get_tags(base_url):
    r = requests.get(base_url)
    soup = BeautifulSoup(r.text, 'html.parser')
    tags = set()
    for tag in soup.find_all(True):
        tags.add(tag.name)
    return tags

# print(get_tags(base_url))

def get_text(base_url):
    r = requests.get(base_url)
    soup = BeautifulSoup(r.text, 'html.parser')
    with open("get_text.txt", "w") as textfile:
        textfile.write(soup.get_text("|", strip=True).encode('utf8'))
    # return soup.get_text("|", strip=True)
    # content = [text for text in soup.stripped_strings]
    # return content

# print(get_text(base_url))