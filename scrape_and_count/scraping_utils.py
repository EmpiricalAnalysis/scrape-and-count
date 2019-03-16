import urllib
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import NavigableString, Comment


def get_page_content(url, dynamic=False):
    if dynamic:
        driver = webdriver.Firefox()
        driver.get(url)
        try:
            xpathstring = "//*[@class='interlanguage-link interwiki-af'][contains(@style, 'display: none')]"
            WebDriverWait(driver,1000).until(EC.presence_of_element_located((By.XPATH,xpathstring)))
            html = driver.page_source
        finally:
            driver.quit()
    else:
        html = urllib.urlopen(url).read()
    return html

def get_all_tag_names(soup):
    names = set() 
    for tag in soup.find_all(True):
        names.add(tag.name)
    return names

def get_selected_tags(soup):
    tags = get_all_tag_names(soup)
    if "[document]" not in tags:
        tags.add("[document]")
    ignore_tags = ['style', 'script', 'head', 'meta', 'noscript'] 
    for tag in ignore_tags:
        if tag in tags:
            tags.remove(tag)
    return tags

def remove_comments(soup):
    comments = soup.findAll(text=lambda text:isinstance(text, Comment))
    [comment.extract() for comment in comments]
    return soup

def parse_k_v_string(str_, split_by):
    k, v = str_.split(split_by)
    return k.strip(), v.strip()

def content_is_visible(content):
    visible = True
    if content.has_attr("style"):
        styles = content.attrs["style"]
        if ";" in styles:
            styles = content.attrs["style"].split(";")
            for style in styles:
                if ":" in style:
                    k, v = parse_k_v_string(style, ":")
                    if k == "display" and v == "none":
                        visible = False
        else:
            if ":" in styles:
                    k, v = parse_k_v_string(styles, ":")
                    if k == "display" and v == "none":
                        visible = False
    return visible

def scrape_visible_text(tag, texts, selected_tags):
    if tag.name in selected_tags:
        if isinstance(tag, type(None)):
            pass
        elif isinstance(tag, NavigableString):
            texts.append(tag + u' ')
        else:
            for child in tag.children:
                if isinstance(child, NavigableString):
                    texts.append(child + u' ')
                else:
                    if content_is_visible(child):
                        if (child.name == "table") and child.has_attr("class") and ("autocollapse" in child['class']):
                            tr_to_keep = child.tbody.find("tr")
                            scrape_visible_text(tr_to_keep, texts, selected_tags)
                        else:
                            if child.contents != None:
                                scrape_visible_text(child, texts, selected_tags)

