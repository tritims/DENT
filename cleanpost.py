import re
from bs4 import BeautifulSoup as bs

def removeTag(soup, tagname):
    for tag in soup.findAll(tagname):
        contents = tag.contents
        parent = tag.parent
        tag.extract()


def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

def removecode(raw_html):
    cleanr = re.compile('<code>(.|\n)*?<\/code>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext

def removeurls(raw_html):
    cleanr = re.compile('</?a.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext

def remove_escape(text):
    # print(text)
    esc = text.replace('\r', ' ').replace('\n', ' ').replace('\t', ' ').replace("\'", ' ')
    # print(text.replace("\n", " "))
    return re.sub('\s+', ' ', esc)

def clean_body(data):
    s = bs(data, "html.parser")
    removeTag(s, 'a')
    removeTag(s, 'code')
    body =  eval(s.get_text())
    return remove_escape(cleanhtml(removecode(removeurls(body)))).strip()