import re


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
    esc = text.replace('\r', ' ').replace('\n', ' ').replace('\t', ' ').replace("\'", ' ')
    return re.sub('\s+', ' ', esc)

def apply_cleaning(s):
    return remove_escape(cleanhtml(removecode(removeurls(s))))