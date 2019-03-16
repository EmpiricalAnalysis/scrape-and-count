# -*- coding: utf-8 -*-
from scrape_and_count.nlp_utils import split_hyphenated_words

class TestNLPUtils(object):

    def test_split_hyphenated_words(self):
        hyphenated_str = "[Python-Dev] Python's python.org"
        actual_words = split_hyphenated_words(hyphenated_str)
        expected_words = " Python Dev  Python s python org"
        assert actual_words == expected_words

    