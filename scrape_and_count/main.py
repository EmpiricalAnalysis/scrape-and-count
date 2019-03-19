# -*- coding: utf-8 -*-
import click
from bs4 import BeautifulSoup
from scraping_utils import (get_page_content, remove_comments, get_selected_tags, 
                                scrape_visible_text)
from nlp_utils import (remove_unicode_chars, split_hyphenated_words, tokenize_words, 
                        remove_stop_words, convert_to_lowercase, lemmatize_words,
                        cal_word_frequency) 

def main(url, dynamic, split_hyphenated_text=True):

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


@click.group()
def cli():
    pass

@click.option('--url',
              'url',
              required=False,
              default='https://en.wikipedia.org/wiki/Python_(programming_language)',
              help='url to scrape text')
@click.option('--dynamic',
              'dynamic',
              required=False,
              default=False,
              help='wait for a dynamic webpage to load javascript? need to have geckodriver installed')
@click.command()
def get_word_count(url, dynamic):
    """
    Scrape a webpage and count its visible words
    """
    main(url, dynamic)

cli.add_command(get_word_count)


if __name__ == "__main__":
    cli()
    """
    Example: python scrape_and_count/main.py get-word-count --dynamic True
    """
