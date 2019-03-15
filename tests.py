# -*- coding: utf-8 -*-
from wikipedia2 import (tokenize_words, remove_stop_words, lemmatize_words,
                        cal_word_frequency, get_text_from_html,
                        remove_unicode_chars, split_hyphenated_words,
                        lowercase_words, get_direct_descendant_text,
                        get_screen_text, get_all_tag_names,
                        get_text_from_tag_expanded, get_selected_tags)
import pytest
from bs4 import BeautifulSoup
# from bs4.element import Comment
import urllib
import re

class TestWordCount(object):

    def test_split_hyphenated_words(self):
        hyphenated_str = "[Python-Dev] Python's python.org"
        print(split_hyphenated_words(hyphenated_str)) 
        assert 0
    
    def test_str1(self):
        str1 = 'Taft, Darryl K. (5 March 2007). "Python Slithers into Systems". eWeek.com. Ziff Davis Holdings. ' \
         + 'Retrieved 24 September 2011. Norwitz, Neal (8 April 2002). "[Python-Dev] Release Schedules (was Stability & change)". Retrieved 27 June 2009. ' \
         + "Why Python's Integer Division Floors" \
         + '. Retrieved 25 August 2010.' \
         + ' "Highlights: Python 2.5". Python.org.'

        dehyphenated_text = split_hyphenated_words(str1)
        print("======== dehyphenated text =======")
        print(dehyphenated_text)
        tokenized_clean = tokenize_words(dehyphenated_text)
        print("======== tokenized cleaned =======")
        print(tokenized_clean)
        words_col = remove_stop_words(tokenized_clean)
        print("======== words collection ========")
        print(words_col)
        lemmatized = lemmatize_words(words_col)
        print("======== lemmatized ========")
        print(lemmatized)
        word, count = cal_word_frequency(lemmatized)
        print("word = {}".format(word))
        print("count = {}".format(count))
        assert word == "python"
        assert count == 5
        # assert 0

        # are Python-Dev and python.org considered as individual word?
    @pytest.mark.parametrize("url", [
    'https://en.wikipedia.org/wiki/Python_(programming_language)',
    # 'https://google.com'
    ])
    def test_wiki(self, url):
        text = get_text_from_html(url)
        ascii_text = remove_unicode_chars(text)
        dehyphenated_text = split_hyphenated_words(ascii_text)
        print("======== dehyphenated text =======")
        # print(dehyphenated_text)
        tokenized_clean = tokenize_words(dehyphenated_text)
        # tokenized_clean = tokenize_words(ascii_text)
        print("======== tokenized cleaned =======")
        # print(tokenized_clean)
        words_col = remove_stop_words(tokenized_clean)
        print("======== words collection ========")
        # print(words_col)
        lowercased = lowercase_words(words_col)
        # lemmatized = lemmatize_words(words_col)
        # print("======== lemmatized ========")
        # print(lemmatized)
        word, count = cal_word_frequency(lowercased)
        print("word = {}".format(word))
        print("count = {}".format(count))
        assert word == "python"
        assert count == 421
        assert 0


    def test_count_from_file(self):
        content = ""
        with open("google.txt") as f:   # wikipedia_python.txt
            content = f.readlines()
        words_str = " ".join(content)
        dehyphenated_text = split_hyphenated_words(words_str)
        print("======== dehyphenated text =======")
        # print(dehyphenated_text)
        tokenized_clean = tokenize_words(dehyphenated_text)
        # tokenized_clean = tokenize_words(ascii_text)
        print("======== tokenized cleaned =======")
        # print(tokenized_clean)
        words_col = remove_stop_words(tokenized_clean)
        print("======== words collection ========")
        # print(words_col)
        lowercased = lowercase_words(words_col)
        # lemmatized = lemmatize_words(words_col)
        # print("======== lemmatized ========")
        # print(lemmatized)
        word, count = cal_word_frequency(lowercased)
        print("word = {}".format(word))
        print("count = {}".format(count))
        assert word == "python"
        assert count == 421
        assert 0 

    def get_screen_text(self, soup):
        new_texts = []
        tags = {
            "a": "title",
            "code": None,
            "h2": None, 
            "h3": None, 
            "h1": None, 
            "table": None,
            "label": None, 
            "body": None, 
            "img": None, 
            "span": None, 
            "tr": None,
            "tbody": None, 
            "li": None, 
            "th": None, 
            "sup": None, 
            "input": None, 
            "td": None, 
            "cite": None, 
            "form": None, 
            "ol": None, 
            "link": None, 
            "abbr": None,
            "br": None, 
            "caption": None, 
            "a": None, 
            "b": None, 
            "wbr": None, 
            "i": None, 
            "title": None, 
            "q": None, 
            "p": None, 
            "div": None, 
            "ul": None
        }

        print("+++++++++++++++++++++++++++++++++++")
        for tag, attribute in tags.items():
            text_group = []
            all_tags = soup.findAll(tag, recursive=True)

            print(" ")
            print("--------- implementation ----------")
            for item in all_tags:
                tmp = item.find(text=True, recursive=True)
                if tmp != None and "implementation" in tmp:
                    # print("language tag: ")
                    print(item)
                    print(tmp)
                    print(' ')
            print("-------------------")
            print(" ")

            if attribute == None:
                for aTag in all_tags:
                    hold_text = aTag.find(text=True, recursive=False)  # , recursive=False
                    if hold_text != None:
                        text_group.append(hold_text)
                print("{} text segments have been extracted from tag {}".format(len(text_group), tag))
                # print(all_tags)
            else: 
                print("{} tags have been extracted from tag {}".format(len(all_tags), tag))
                for aTag in all_tags:
                    # print("aTag = {}".format(aTag))
                    hold_text = aTag.find(text=True, recursive=False)
                    if aTag.has_attr(attribute) and hold_text != None:
                        # print("aTag.string = {}".format(aTag.string.encode('utf-8')))
                        text_group.append(hold_text)
                print("{} text segments have been extracted from tag {}".format(len(text_group), tag))
            print(text_group[0:10])
            print("+++++++++++++++++++++++++++++++++++")
            new_texts = new_texts + text_group
        
        print(len(new_texts))
        texts =  u" ".join(t for t in new_texts if t != None)

        # print(" ")
        # print("-----------------")
        # for elt in new_texts:
        #     if "language" in elt:
        #         print(elt)
        # print("-----------------")
        # print(" ")
        return texts


    @pytest.mark.parametrize("url", [
        'https://en.wikipedia.org/wiki/Python_(programming_language)',
        # 'https://google.com'
        ])
    def test_wiki_get_tags(self, url):
        html = urllib.urlopen(url).read()
        soup = BeautifulSoup(html, 'html5lib')
        # texts = soup.findAll(text=True)

        texts = get_screen_text(soup)

        print(len(texts))

        print("#################################")
        for elt in texts:
            if ("software" in elt) | ("Software" in elt):
                print(elt)
                print(" ")
            # match = re.search(r"(\w*)software(\w*)", elt)
            # if match:
            #     print match.group(1)
        print("#################################")

        text_str = u" ".join(t for t in texts if t != None)

        ascii_text = remove_unicode_chars(text_str)
        dehyphenated_text = split_hyphenated_words(ascii_text)
        print("======== dehyphenated text =======")
        # print(dehyphenated_text)
        tokenized_clean = tokenize_words(dehyphenated_text)
        # tokenized_clean = tokenize_words(ascii_text)
        print("======== tokenized cleaned =======")
        # print(tokenized_clean)
        words_col = remove_stop_words(tokenized_clean)
        print("======== words collection ========")
        # print(words_col)
        lowercased = lowercase_words(words_col)
        # lemmatized = lemmatize_words(words_col)
        # print("======== lemmatized ========")
        # print(lemmatized)
        word, count = cal_word_frequency(lowercased)
        print("word = {}".format(word))
        print("count = {}".format(count))
        assert word == "python"
        assert count == 421
        assert 0

    # def get_text_from_single_tag(self, soup, tag):
    # #    content = soup.tag.contents
    # #    for elt in content:
    #    content = soup.find(tag)
    #    return [el for el in content.children if isinstance(el, NavigableString)]

    def test_get_text_from_one_tag(self):
        _str = '<p>Python interpreters are available for many<a href="/wiki/Operating_system" title="Operating system">operating systems</a>.<a href="/wiki/CPython" title="CPython">CPython</a>, the<a href="/wiki/Reference_implementation" title="Reference implementation">reference implementation</a>of Python, is<a href="/wiki/Open-source_software" title="Open-source software">open source</a>software<sup class="reference" id="cite_ref-30"><a href="#cite_note-30">[30]</a></sup>and has a community-based development model, as do nearly all of Python\'s other implementations. Python and CPython are managed by the non-profit<a href="/wiki/Python_Software_Foundation" title="Python Software Foundation">Python Software Foundation</a>.</p>'
        soup = BeautifulSoup(_str, 'html5lib')
        actual_list_of_text = get_direct_descendant_text(soup, "p")
        expected_list_of_text = [u'Python interpreters are available for many', 
                                 u'.', 
                                 u', the', 
                                 u'of Python, is', 
                                 u'software', 
                                 u"and has a community-based development model, as do nearly all of Python's other implementations. Python and CPython are managed by the non-profit", 
                                 u'.']
        assert actual_list_of_text == expected_list_of_text

# print(soup.p.contents)  # find().get_text(strip=True))

    def test_get_text_from_multiple_tags(self):
        _str = '<p>Python interpreters are available for many<a href="/wiki/Operating_system" title="Operating system">operating systems</a>.<a href="/wiki/CPython" title="CPython">CPython</a>, the<a href="/wiki/Reference_implementation" title="Reference implementation">reference implementation</a>of Python, is<a href="/wiki/Open-source_software" title="Open-source software">open source</a>software<sup class="reference" id="cite_ref-30"><a href="#cite_note-30">[30]</a></sup>and has a community-based development model, as do nearly all of Python\'s other implementations. Python and CPython are managed by the non-profit<a href="/wiki/Python_Software_Foundation" title="Python Software Foundation">Python Software Foundation</a>.</p><p>Python was conceived in the late 1980s<sup class="reference" id="cite_ref-venners-interview-pt-1_31-0"><a href="#cite_note-venners-interview-pt-1-31">[31]</a></sup>by<a href="/wiki/Guido_van_Rossum" title="Guido van Rossum">Guido van Rossum</a>at<a href="/wiki/Centrum_Wiskunde_%26_Informatica" title="Centrum Wiskunde &amp; Informatica">Centrum Wiskunde &amp; Informatica</a>(CWI) in the<a href="/wiki/Netherlands" title="Netherlands">Netherlands</a>as a successor to the<a href="/wiki/ABC_(programming_language)" title="ABC (programming language)">ABC language</a>(itself inspired by<a href="/wiki/SETL" title="SETL">SETL</a>)<sup class="reference" id="cite_ref-AutoNT-12_32-0"><a href="#cite_note-AutoNT-12-32">[32]</a></sup>, capable of<a href="/wiki/Exception_handling" title="Exception handling">exception handling</a>and interfacing with the<a href="/wiki/Amoeba_(operating_system)" title="Amoeba (operating system)">Amoeba</a>operating system.<sup class="reference" id="cite_ref-faq-created_7-1"><a href="#cite_note-faq-created-7">[7]</a></sup>Its implementation began in December 1989.<sup class="reference" id="cite_ref-timeline-of-python_33-0"><a href="#cite_note-timeline-of-python-33">[33]</a></sup>Van Rossum\'s long influence on Python is reflected in the title given to him by the Python community:<i><a class="mw-redirect" href="/wiki/Benevolent_Dictator_For_Life" title="Benevolent Dictator For Life">Benevolent Dictator For Life</a></i>(BDFL) –  a post from which he gave himself permanent vacation on July 12, 2018.<sup class="reference" id="cite_ref-lj-bdfl-resignation_34-0"><a href="#cite_note-lj-bdfl-resignation-34">[34]</a></sup></p>'
        soup = BeautifulSoup(_str, 'html5lib')
        actual_list_of_text = get_direct_descendant_text(soup, "p")
        print(actual_list_of_text)
        expected_list_of_text = [u'Python interpreters are available for many', 
                                 u'.', 
                                 u', the', 
                                 u'of Python, is', 
                                 u'software', 
                                 u"and has a community-based development model, as do nearly all of Python's other implementations. Python and CPython are managed by the non-profit", 
                                 u'.', 
                                 u'Python was conceived in the late 1980s', 
                                 u'by', 
                                 u'at', 
                                 u'(CWI) in the', 
                                 u'as a successor to the', 
                                 u'(itself inspired by', 
                                 u')', 
                                 u', capable of', 
                                 u'and interfacing with the', 
                                 u'operating system.', 
                                 u'Its implementation began in December 1989.', 
                                 u"Van Rossum's long influence on Python is reflected in the title given to him by the Python community:", 
                                 u'(BDFL) \xe2\u20ac\u201c  a post from which he gave himself permanent vacation on July 12, 2018.'] 
        assert actual_list_of_text == expected_list_of_text

    def test_get_tag_names(self):
        url = 'https://en.wikipedia.org/wiki/Python_(programming_language)'
        html = urllib.urlopen(url).read()
        soup = BeautifulSoup(html, 'html5lib')
        actual_tags = get_all_tag_names(soup)
        expected_tags = set([u'code', u'h2', u'h3', u'h1', u'meta', u'table', u'label', u'noscript', u'style', u'span', u'img', u'script', u'tr', u'tbody', u'li', u'html', u'th', u'sup', u'input', u'td', u'cite', u'body', u'head', u'form', u'ol', u'link', u'abbr', u'br', u'caption', u'a', u'b', u'wbr', u'i', u'title', u'q', u'p', u'div', u'ul'])
        assert actual_tags == expected_tags

    def test_ignore_autocollapsed_tags(self):
        _str = '<div aria-labelledby="Python" class="navbox" role="navigation" style="padding:3px"><table class="nowraplinks collapsible autocollapse navbox-inner" style="border-spacing:0;background:transparent;color:inherit"><tbody><tr><th class="navbox-title" colspan="3" scope="col"><div class="plainlinks hlist navbar mini"><ul><li class="nv-view"><a href="/wiki/Template:Python_(programming_language)" title="Template:Python (programming language)"><abbr style=";;background:none transparent;border:none;-moz-box-shadow:none;-webkit-box-shadow:none;box-shadow:none; padding:0;" title="View this template">v</abbr></a></li><li class="nv-talk"><a href="/wiki/Template_talk:Python_(programming_language)" title="Template talk:Python (programming language)"><abbr style=";;background:none transparent;border:none;-moz-box-shadow:none;-webkit-box-shadow:none;box-shadow:none; padding:0;" title="Discuss this template">t</abbr></a></li><li class="nv-edit"><a class="external text" href="//en.wikipedia.org/w/index.php?title=Template:Python_(programming_language)&amp;action=edit"><abbr style=";;background:none transparent;border:none;-moz-box-shadow:none;-webkit-box-shadow:none;box-shadow:none; padding:0;" title="Edit this template">e</abbr></a></li></ul></div><div id="Python" style="font-size:114%;margin:0 4em"><a class="mw-selflink selflink">Python</a></div></th></tr><tr><th class="navbox-group" scope="row" style="width:1%"><a href="/wiki/Programming_language_implementation" title="Programming language implementation">Implementations</a></th><td class="navbox-list navbox-odd hlist" style="text-align:left;border-left-width:2px;border-left-style:solid;width:100%;padding:0px"><div style="padding:0em 0.25em"><ul><li><a href="/wiki/CircuitPython" title="CircuitPython">CircuitPython</a></li><li><a href="/wiki/CLPython" title="CLPython">CLPython</a></li><li><a href="/wiki/CPython" title="CPython">CPython</a></li><li><a href="/wiki/Cython" title="Cython">Cython</a></li><li><a href="/wiki/MicroPython" title="MicroPython">MicroPython</a></li><li><a href="/wiki/Numba" title="Numba">Numba</a></li><li><a href="/wiki/IronPython" title="IronPython">IronPython</a></li><li><a href="/wiki/Jython" title="Jython">Jython</a></li><li><a href="/wiki/Psyco" title="Psyco">Psyco</a></li><li><a href="/wiki/PyPy" title="PyPy">PyPy</a></li><li><a href="/wiki/Python_for_S60" title="Python for S60">Python for S60</a></li><li><a href="/wiki/Shed_Skin" title="Shed Skin">Shed Skin</a></li><li><a href="/wiki/Stackless_Python" title="Stackless Python">Stackless Python</a></li><li><a class="mw-redirect" href="/wiki/Unladen_Swallow" title="Unladen Swallow">Unladen Swallow</a></li><li><i><a href="/wiki/List_of_Python_software#Python_implementations" title="List of Python software">more</a>...</i></li></ul></div></td><td class="navbox-image" rowspan="3" style="width:1px;padding:0px 0px 0px 2px"><div><a class="image" href="/wiki/File:Python-logo-notext.svg"><img alt="Python-logo-notext.svg" data-file-height="110" data-file-width="110" decoding="async" height="55" src="//upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/55px-Python-logo-notext.svg.png" srcset="//upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/83px-Python-logo-notext.svg.png 1.5x, //upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/110px-Python-logo-notext.svg.png 2x" width="55"/></a></div></td></tr><tr><th class="navbox-group" scope="row" style="width:1%"><a href="/wiki/Integrated_development_environment" title="Integrated development environment">IDE</a></th><td class="navbox-list navbox-even hlist" style="text-align:left;border-left-width:2px;border-left-style:solid;width:100%;padding:0px"><div style="padding:0em 0.25em"><ul><li><a href="/wiki/Comparison_of_integrated_development_environments#Python" title="Comparison of integrated development environments">Boa</a></li><li><a class="mw-redirect" href="/wiki/Eric_Python_IDE" title="Eric Python IDE">Eric Python IDE</a></li><li><a class="mw-redirect" href="/wiki/IDLE_(Python)" title="IDLE (Python)">IDLE</a></li><li><a href="/wiki/PyCharm" title="PyCharm">PyCharm</a></li><li><a href="/wiki/PyDev" title="PyDev">PyDev</a></li><li><a href="/wiki/Stani%27s_Python_Editor" title="Stani\'s Python Editor">SPE</a></li><li><a href="/wiki/Ninja-IDE" title="Ninja-IDE">Ninja-IDE</a></li><li><i><a class="mw-redirect" href="/wiki/List_of_integrated_development_environments_for_Python#Python" title="List of integrated development environments for Python">more</a>...</i></li></ul></div></td></tr><tr><th class="navbox-group" scope="row" style="width:1%">Topics</th><td class="navbox-list navbox-odd hlist" style="text-align:left;border-left-width:2px;border-left-style:solid;width:100%;padding:0px"><div style="padding:0em 0.25em"><ul><li><a href="/wiki/Web_Server_Gateway_Interface" title="Web Server Gateway Interface">WSGI</a></li></ul></div></td></tr><tr><td class="navbox-abovebelow hlist" colspan="3"><div><ul><li><a href="/wiki/List_of_Python_software" title="List of Python software">software (list)</a></li><li><a href="/wiki/Python_Software_Foundation" title="Python Software Foundation">Python Software Foundation</a></li><li><a href="/wiki/Python_Conference" title="Python Conference">PyCon</a></li></ul></div></td></tr></tbody></table></div>'
        soup = BeautifulSoup(_str, 'html5lib')
        for child in soup.div.children:
            if (child.name == "table") and child.has_attr("class") and ("autocollapse" in child['class']):
                print(child["class"])
                tr_to_keep = child.tbody.find("tr")
                actual_list_of_text = get_screen_text(tr_to_keep)
        # print(actual_list_of_text)
        expected_list_of_text = [u'Python', u'v', u't', u'e']
        assert actual_list_of_text == expected_list_of_text
        # assert 0

    def test_get_all_text(self):
        _str = '<p>Python interpreters are available for many<a href="/wiki/Operating_system" title="Operating system">operating systems</a>.<a href="/wiki/CPython" title="CPython">CPython</a>, the<a href="/wiki/Reference_implementation" title="Reference implementation">reference implementation</a>of Python, is<a href="/wiki/Open-source_software" title="Open-source software">open source</a>software<sup class="reference" id="cite_ref-30"><a href="#cite_note-30">[30]</a></sup>and has a community-based development model, as do nearly all of Python\'s other implementations. Python and CPython are managed by the non-profit<a href="/wiki/Python_Software_Foundation" title="Python Software Foundation">Python Software Foundation</a>.</p><p>Python was conceived in the late 1980s<sup class="reference" id="cite_ref-venners-interview-pt-1_31-0"><a href="#cite_note-venners-interview-pt-1-31">[31]</a></sup>by<a href="/wiki/Guido_van_Rossum" title="Guido van Rossum">Guido van Rossum</a>at<a href="/wiki/Centrum_Wiskunde_%26_Informatica" title="Centrum Wiskunde &amp; Informatica">Centrum Wiskunde &amp; Informatica</a>(CWI) in the<a href="/wiki/Netherlands" title="Netherlands">Netherlands</a>as a successor to the<a href="/wiki/ABC_(programming_language)" title="ABC (programming language)">ABC language</a>(itself inspired by<a href="/wiki/SETL" title="SETL">SETL</a>)<sup class="reference" id="cite_ref-AutoNT-12_32-0"><a href="#cite_note-AutoNT-12-32">[32]</a></sup>, capable of<a href="/wiki/Exception_handling" title="Exception handling">exception handling</a>and interfacing with the<a href="/wiki/Amoeba_(operating_system)" title="Amoeba (operating system)">Amoeba</a>operating system.<sup class="reference" id="cite_ref-faq-created_7-1"><a href="#cite_note-faq-created-7">[7]</a></sup>Its implementation began in December 1989.<sup class="reference" id="cite_ref-timeline-of-python_33-0"><a href="#cite_note-timeline-of-python-33">[33]</a></sup>Van Rossum\'s long influence on Python is reflected in the title given to him by the Python community:<i><a class="mw-redirect" href="/wiki/Benevolent_Dictator_For_Life" title="Benevolent Dictator For Life">Benevolent Dictator For Life</a></i>(BDFL) –  a post from which he gave himself permanent vacation on July 12, 2018.<sup class="reference" id="cite_ref-lj-bdfl-resignation_34-0"><a href="#cite_note-lj-bdfl-resignation-34">[34]</a></sup></p>'
        soup = BeautifulSoup(_str, 'html5lib')
        texts = []
        selected_tags = get_selected_tags(soup)
        get_text_from_tag_expanded(soup.html, texts, selected_tags)
        expected_list_of_text = [u'Python interpreters are available for many', 
                                 u'operating systems', u'.', u'CPython', u', the', 
                                 u'reference implementation', u'of Python, is', 
                                 u'open source', u'software', u'[30]', 
                                 u"and has a community-based development model, as do nearly all of Python's other implementations. Python and CPython are managed by the non-profit", u'Python Software Foundation', 
                                 u'.', u'Python was conceived in the late 1980s', 
                                 u'[31]', u'by', u'Guido van Rossum', u'at', 
                                 u'Centrum Wiskunde & Informatica', 
                                 u'(CWI) in the', u'Netherlands', 
                                 u'as a successor to the', u'ABC language', 
                                 u'(itself inspired by', u'SETL', u')', u'[32]', 
                                 u', capable of', u'exception handling', 
                                 u'and interfacing with the', u'Amoeba', 
                                 u'operating system.', u'[7]', 
                                 u'Its implementation began in December 1989.', 
                                 u'[33]', u"Van Rossum's long influence on Python is reflected in the title given to him by the Python community:", 
                                 u'Benevolent Dictator For Life', 
                                 u'(BDFL) \xe2\u20ac\u201c  a post from which he gave himself permanent vacation on July 12, 2018.', 
                                 u'[34]']
        assert texts == expected_list_of_text

    def test_get_text_with_autocollapse(self):
        _str = '<div aria-labelledby="Python" class="navbox" role="navigation" style="padding:3px"><table class="nowraplinks collapsible autocollapse navbox-inner" style="border-spacing:0;background:transparent;color:inherit"><tbody><tr><th class="navbox-title" colspan="3" scope="col"><div class="plainlinks hlist navbar mini"><ul><li class="nv-view"><a href="/wiki/Template:Python_(programming_language)" title="Template:Python (programming language)"><abbr style=";;background:none transparent;border:none;-moz-box-shadow:none;-webkit-box-shadow:none;box-shadow:none; padding:0;" title="View this template">v</abbr></a></li><li class="nv-talk"><a href="/wiki/Template_talk:Python_(programming_language)" title="Template talk:Python (programming language)"><abbr style=";;background:none transparent;border:none;-moz-box-shadow:none;-webkit-box-shadow:none;box-shadow:none; padding:0;" title="Discuss this template">t</abbr></a></li><li class="nv-edit"><a class="external text" href="//en.wikipedia.org/w/index.php?title=Template:Python_(programming_language)&amp;action=edit"><abbr style=";;background:none transparent;border:none;-moz-box-shadow:none;-webkit-box-shadow:none;box-shadow:none; padding:0;" title="Edit this template">e</abbr></a></li></ul></div><div id="Python" style="font-size:114%;margin:0 4em"><a class="mw-selflink selflink">Python</a></div></th></tr><tr><th class="navbox-group" scope="row" style="width:1%"><a href="/wiki/Programming_language_implementation" title="Programming language implementation">Implementations</a></th><td class="navbox-list navbox-odd hlist" style="text-align:left;border-left-width:2px;border-left-style:solid;width:100%;padding:0px"><div style="padding:0em 0.25em"><ul><li><a href="/wiki/CircuitPython" title="CircuitPython">CircuitPython</a></li><li><a href="/wiki/CLPython" title="CLPython">CLPython</a></li><li><a href="/wiki/CPython" title="CPython">CPython</a></li><li><a href="/wiki/Cython" title="Cython">Cython</a></li><li><a href="/wiki/MicroPython" title="MicroPython">MicroPython</a></li><li><a href="/wiki/Numba" title="Numba">Numba</a></li><li><a href="/wiki/IronPython" title="IronPython">IronPython</a></li><li><a href="/wiki/Jython" title="Jython">Jython</a></li><li><a href="/wiki/Psyco" title="Psyco">Psyco</a></li><li><a href="/wiki/PyPy" title="PyPy">PyPy</a></li><li><a href="/wiki/Python_for_S60" title="Python for S60">Python for S60</a></li><li><a href="/wiki/Shed_Skin" title="Shed Skin">Shed Skin</a></li><li><a href="/wiki/Stackless_Python" title="Stackless Python">Stackless Python</a></li><li><a class="mw-redirect" href="/wiki/Unladen_Swallow" title="Unladen Swallow">Unladen Swallow</a></li><li><i><a href="/wiki/List_of_Python_software#Python_implementations" title="List of Python software">more</a>...</i></li></ul></div></td><td class="navbox-image" rowspan="3" style="width:1px;padding:0px 0px 0px 2px"><div><a class="image" href="/wiki/File:Python-logo-notext.svg"><img alt="Python-logo-notext.svg" data-file-height="110" data-file-width="110" decoding="async" height="55" src="//upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/55px-Python-logo-notext.svg.png" srcset="//upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/83px-Python-logo-notext.svg.png 1.5x, //upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/110px-Python-logo-notext.svg.png 2x" width="55"/></a></div></td></tr><tr><th class="navbox-group" scope="row" style="width:1%"><a href="/wiki/Integrated_development_environment" title="Integrated development environment">IDE</a></th><td class="navbox-list navbox-even hlist" style="text-align:left;border-left-width:2px;border-left-style:solid;width:100%;padding:0px"><div style="padding:0em 0.25em"><ul><li><a href="/wiki/Comparison_of_integrated_development_environments#Python" title="Comparison of integrated development environments">Boa</a></li><li><a class="mw-redirect" href="/wiki/Eric_Python_IDE" title="Eric Python IDE">Eric Python IDE</a></li><li><a class="mw-redirect" href="/wiki/IDLE_(Python)" title="IDLE (Python)">IDLE</a></li><li><a href="/wiki/PyCharm" title="PyCharm">PyCharm</a></li><li><a href="/wiki/PyDev" title="PyDev">PyDev</a></li><li><a href="/wiki/Stani%27s_Python_Editor" title="Stani\'s Python Editor">SPE</a></li><li><a href="/wiki/Ninja-IDE" title="Ninja-IDE">Ninja-IDE</a></li><li><i><a class="mw-redirect" href="/wiki/List_of_integrated_development_environments_for_Python#Python" title="List of integrated development environments for Python">more</a>...</i></li></ul></div></td></tr><tr><th class="navbox-group" scope="row" style="width:1%">Topics</th><td class="navbox-list navbox-odd hlist" style="text-align:left;border-left-width:2px;border-left-style:solid;width:100%;padding:0px"><div style="padding:0em 0.25em"><ul><li><a href="/wiki/Web_Server_Gateway_Interface" title="Web Server Gateway Interface">WSGI</a></li></ul></div></td></tr><tr><td class="navbox-abovebelow hlist" colspan="3"><div><ul><li><a href="/wiki/List_of_Python_software" title="List of Python software">software (list)</a></li><li><a href="/wiki/Python_Software_Foundation" title="Python Software Foundation">Python Software Foundation</a></li><li><a href="/wiki/Python_Conference" title="Python Conference">PyCon</a></li></ul></div></td></tr></tbody></table></div>'
        soup = BeautifulSoup(_str, 'html5lib')
        texts = []
        selected_tags = get_selected_tags(soup)
        get_text_from_tag_expanded(soup.html, texts, selected_tags)
        print("======== inside test function =========")
        print(texts)
        expected_list_of_text = [u'Python', u'v', u't', u'e'] 
        assert texts == expected_list_of_text
        assert 0

    def test_get_text_from_wiki_page(self):
        url = 'https://en.wikipedia.org/wiki/Python_(programming_language)'
        html = urllib.urlopen(url).read()
        soup = BeautifulSoup(html, 'html5lib')
        texts = []
        selected_tags = get_selected_tags(soup)
        get_text_from_tag_expanded(soup.html, texts, selected_tags)
        print("======== inside test function =========")
        print(texts)
        # print(selected_tags)
        expected_list_of_text = [] # [u'Python', u'v', u't', u'e']
        assert texts == expected_list_of_text
        assert 0

    @pytest.mark.parametrize("url", [
        'https://en.wikipedia.org/wiki/Python_(programming_language)',
        # 'https://google.com'
        ])
    def test_wiki_get_tags_w_expanded_func(self, url):
        html = urllib.urlopen(url).read()
        soup = BeautifulSoup(html, 'html5lib')
        # texts = soup.findAll(text=True)

        # texts = get_screen_text(soup)
        texts = []
        selected_tags = get_selected_tags(soup)
        get_text_from_tag_expanded(soup.html, texts, selected_tags)
        # print(texts)
        with open("texts.txt", "w") as f:
            for text in texts:
                f.write(text.encode('utf8'))
        print(len(texts))

        # print("#################################")
        # for elt in texts:
        #     if ("software" in elt) | ("Software" in elt):
        #         print(elt)
        #         print(" ")
        #     # match = re.search(r"(\w*)software(\w*)", elt)
        #     # if match:
        #     #     print match.group(1)
        # print("#################################")

        text_str = u" ".join(t for t in texts if t != None)

        ascii_text = remove_unicode_chars(text_str)
        dehyphenated_text = split_hyphenated_words(ascii_text)
        print("======== dehyphenated text =======")
        # print(dehyphenated_text)
        tokenized_clean = tokenize_words(dehyphenated_text)
        # tokenized_clean = tokenize_words(ascii_text)
        print("======== tokenized cleaned =======")
        # print(tokenized_clean)
        words_col = remove_stop_words(tokenized_clean)
        print("======== words collection ========")
        # print(words_col)
        lowercased = lowercase_words(words_col)
        # lemmatized = lemmatize_words(words_col)
        # print("======== lemmatized ========")
        # print(lemmatized)
        word, count = cal_word_frequency(lowercased)
        print("word = {}".format(word))
        print("count = {}".format(count))
        assert word == "python"
        assert count == 421
        assert 0

    def test_ignore_invisible_tag(self):
        # _str = '<div class="shortdescription nomobile noexcerpt noprint searchaux" style="display:none">General-purpose, high-level programming language</div>'
        _str = '<p><div class="shortdescription nomobile noexcerpt noprint searchaux" style="display:none">General-purpose, high-level programming language</div></p>'
        soup = BeautifulSoup(_str, 'html5lib')
        # texts = []
        # selected_tags = get_selected_tags(soup)
        texts = get_screen_text(soup)
        print("======== inside test function =========")
        print(texts)
        expected_list_of_text = [] # [u'Python', u'v', u't', u'e'] 
        assert texts == expected_list_of_text
        # assert 0 

    def test_ignore_comments(self):
        _str = '<div>      <!-- \nNewPP limit report\nParsed by mw1263\nCached time: 20190311165754--></div>'
        soup = BeautifulSoup(_str, "html5lib")
        texts = get_screen_text(soup)
        print(texts)
        assert 0

def test_if_else(n):
    if n > 0:
        if n < 10:
            return False
        else:
            return True
    else:
        return True

print(test_if_else(13))


            
