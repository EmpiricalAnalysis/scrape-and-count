# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from scrape_and_count.scraping_utils import (get_page_content, remove_comments, get_selected_tags, 
                                scrape_visible_text)
from scrape_and_count.nlp_utils import (remove_unicode_chars, split_hyphenated_words, tokenize_words, 
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
    if split_hyphenated_text:
        dehyphenated_text = split_hyphenated_words(ascii_str)
        print("======== dehyphenated text =======")
        # print(dehyphenated_text)
    else:
        dehyphenated_text = ascii_str
    tokenized_clean = tokenize_words(dehyphenated_text)
    # tokenized_clean = tokenize_words(ascii_str)
    print("======== tokenized cleaned =======")
    # print(tokenized_clean)
    words_col = remove_stop_words(tokenized_clean)
    print("======== words collection ========")
    # print(words_col)
    lowercased = convert_to_lowercase(words_col)
    # lemmatized = lemmatize_words(words_col)
    # print("======== lemmatized ========")
    # print(lemmatized)
    most_common_pairs = cal_word_frequency(lowercased, 10)

    print(most_common_pairs)

    print("word = {}".format(most_common_pairs[0][0]))
    print("count = {}".format(most_common_pairs[0][1]))


url = 'https://en.wikipedia.org/wiki/Python_(programming_language)'
if  __name__ =='__main__':main(url)