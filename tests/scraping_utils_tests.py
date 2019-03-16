# -*- coding: utf-8 -*-
import io
import urllib
from bs4 import BeautifulSoup
from scrape_and_count.scraping_utils import (remove_comments, get_selected_tags, 
                                             scrape_visible_text, get_page_content,
                                             get_all_tag_names)
import pytest

class TestScrapingUtils(object):

    def test_get_tag_names(self):
        url = 'https://en.wikipedia.org/wiki/Python_(programming_language)'
        html = urllib.urlopen(url).read()
        soup = BeautifulSoup(html, 'html5lib')
        actual_tags = get_all_tag_names(soup)
        print(actual_tags)
        expected_tags = set([u'code', u'h2', u'h3', u'h1', u'meta', u'table', u'label', u'noscript', u'style', u'span', u'img', u'script', u'tr', u'tbody', u'li', u'html', u'th', u'sup', u'input', u'td', u'cite', u'body', u'head', u'form', u'ol', u'link', u'abbr', u'br', u'caption', u'a', u'b', u'wbr', u'i', u'title', u'q', u'p', u'div', u'ul'])
        assert actual_tags == expected_tags

    def test_ignore_comments(self):
        _str = ('<div>' 
                + '<p class="mw-empty-elt">'
                + 'something'
                + '</p>'
                + '<!--'
                + 'NewPP limit report'
                + 'Parsed by mw1263'
                + 'Cached time: 20190311165754'
                + '--></div>')
        soup = BeautifulSoup(_str, "html5lib")
        soup = remove_comments(soup)
        selected_tags = get_selected_tags(soup)
        texts = []
        scrape_visible_text(soup, texts, selected_tags)
        assert texts == [u'something ']

    def test_ignore_invisible_tag(self):
        _str = '<p><div class="shortdescription nomobile noexcerpt noprint searchaux" \
                style="display:none">General-purpose, high-level programming \
                language</div></p>'
        soup = BeautifulSoup(_str, 'html5lib')
        texts = []
        selected_tags = get_selected_tags(soup)
        scrape_visible_text(soup, texts, selected_tags)
        print("======== inside test function =========")
        print(texts)
        expected_list_of_text = []
        assert texts == expected_list_of_text

    def test_get_text_with_autocollapse(self):
        with open("tests/resources/autocollapse_div.txt", "r") as f:
            content = f.readlines()
        _str = "".join(content)
        soup = BeautifulSoup(_str, 'html5lib')
        texts = []
        selected_tags = get_selected_tags(soup)
        scrape_visible_text(soup.html, texts, selected_tags)
        expected_list_of_text = [u'v ', u't ', u'e ', u'Python ']
        assert texts == expected_list_of_text

    def test_get_all_visible_text(self):
        with io.open("tests/resources/embeded_tags.txt", mode="r", encoding="utf-8") as f:
            content = f.readlines()
        _str = "".join(content)
        soup = BeautifulSoup(_str, 'html5lib')
        texts = []
        selected_tags = get_selected_tags(soup)
        scrape_visible_text(soup.html, texts, selected_tags)
        expected_list_of_text = [u'Python interpreters are available for many ', 
                                 u'operating systems ', u'. ', u'CPython ', u', the ', 
                                 u'reference implementation ', u'of Python, is ', u'open source ', 
                                 u'software ', u'[30] ', u"and has a community-based development model, as do nearly all of Python's other implementations. Python and CPython are managed by the non-profit ", 
                                 u'Python Software Foundation ', u'. ', u'Python was conceived in the late 1980s ', 
                                 u'[31] ', u'by ', u'Guido van Rossum ', u'at ', u'Centrum Wiskunde & Informatica ', 
                                 u'(CWI) in the ', u'Netherlands ', u'as a successor to the ', u'ABC language ', 
                                 u'(itself inspired by ', u'SETL ', u') ', u'[32] ', u', capable of ', 
                                 u'exception handling ', u'and interfacing with the ', u'Amoeba ', 
                                 u'operating system. ', u'[7] ', u'Its implementation began in December 1989. ', 
                                 u'[33] ', u"Van Rossum's long influence on Python is reflected in the title given to him by the Python community: ", 
                                 u'Benevolent Dictator For Life ', u'(BDFL) \u2013  a post from which he gave himself permanent vacation on July 12, 2018. ', 
                                 u'[34] ']
        print(texts)
        assert texts == expected_list_of_text

    @pytest.mark.skip(reason="this is an integration test, needs to make sure that \
                      geckodriver and selenium are installed, need internet access")
    @pytest.mark.integration()
    @pytest.mark.parametrize("url, key_word", [
        ('https://en.wikipedia.org/wiki/Python_(programming_language)', u"Afrikaans"),
        ])
    def test_fully_loaded_dynamic_content(self, url, key_word):
        html = get_page_content(url, dynamic=True)
        soup = BeautifulSoup(html, 'html5lib')
        soup = remove_comments(soup)
        texts = []
        selected_tags = get_selected_tags(soup)
        scrape_visible_text(soup, texts, selected_tags)
        text_str = u" ".join(t for t in texts if t != None)
        assert key_word not in text_str 
