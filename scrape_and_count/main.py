# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from scraping_utils import (get_page_content, remove_comments, get_selected_tags, 
                                scrape_visible_text)
from nlp_utils import (remove_unicode_chars, split_hyphenated_words, tokenize_words, 
                        remove_stop_words, convert_to_lowercase, lemmatize_words,
                        cal_word_frequency) 

def main(url, dynamic=True, split_hyphenated_text=True):

    html = get_page_content(url, dynamic)
    soup = BeautifulSoup(html, 'html5lib')
    soup = remove_comments(soup)

    texts = []
    selected_tags = get_selected_tags(soup)
    scrape_visible_text(soup, texts, selected_tags)
    text_str = u" ".join(t for t in texts if t != None)
    ascii_str = remove_unicode_chars(text_str)
    tokenized_clean = tokenize_words(ascii_str)
    words_coll = remove_stop_words(tokenized_clean)
    most_common_pairs = cal_word_frequency(words_coll, 10)
    print("The most common words are: ")
    print(most_common_pairs)

url = 'https://en.wikipedia.org/wiki/Python_(programming_language)'
if  __name__ =='__main__':main(url)