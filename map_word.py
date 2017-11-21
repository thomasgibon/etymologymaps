# -*- coding: utf-8 -*-
"""
Created on Tue Nov 05 2013 20:39:37 2013

@author: t.gibon@gmail.com
"""

import csv
import urllib
import codecs
import string
import re
from bs4 import BeautifulSoup

def unicode_csv_reader(utf8_data, dialect=csv.excel, **kwargs):
    csv_reader = csv.reader(utf8_data, dialect=dialect, **kwargs)
    for row in csv_reader:
        yield [cell.decode('utf-8') for cell in row]

def mtranslate(to_translate, wiki_lang = 'en'):
    '''
    Return the translation using wikipedia
    you must shortcut the langage you define (French = fr, English = en, Spanish = es, etc...)
    if you don't define anything it will detect it or use english by default
    '''
    
    agents = {'User-Agent':"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30)"}
    link = "http://%s.wikipedia.org/wiki/%s" % (wiki_lang, to_translate.replace(" ", "_"))
    request = urllib.request.Request(link, headers=agents)
    page = urllib.request.urlopen(request).read()
    parsed_html = BeautifulSoup(page, 'lxml')
    interwiki = parsed_html.body.findAll('li', attrs = {'class':re.compile('interwiki-')})
    pair = [each.find('a').get('title') for each in interwiki]

    code = [each.find('a').get('hreflang') for each in interwiki]

    result = list()
    result.append(tuple(code))

    pairs = [each.split(u' \u2013 ') for each in pair]

    result.append([each[0] for each in pairs])
    result.append([each[1] for each in pairs])

    filename = codecs.open('output_' + to_translate.replace(" ", "_") + '.txt','w', encoding='utf-8')
    filename.write(u'Language\t' + to_translate + u'\n')

    for i in range(len(pair)):
        each = pair[i].split(u' \u2013 ')
        filename.write(code[i] + u'\t' + each[1] + u'\t' + each[0] + u'\n')

    return result
        
def ipa(to_translate, wiki_lang = 'en'):
    
    reader  = list(csv.reader(open('wiki_lang_codes.txt','rb'), delimiter='\t'))
    lang_codes = [row[0] for row in reader]
    lang_names = [row[1] for row in reader]
    lang_names = [l.decode('utf-8') for l in lang_names]
    
    agents = {'User-Agent':"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30)"}
    link = "http://%s.wiktionary.org/wiki/%s" % (wiki_lang, string.lower(to_translate.replace(" ", "_")))
    request = urllib.request.Request(link, headers=agents)
    page = urllib.request.urlopen(request).read()
    parsed_html = BeautifulSoup(page, 'lxml')
    
    lang_name = lang_names[lang_codes.index(wiki_lang)]
    parsed_html.body.findAll('span', attrs = {'id':lang_name})
    
    try:
        result = parsed_html.body.find('span', attrs = {'class':'IPA'}).contents[0]
    except:
        result = parsed_html.body.find('span', attrs = {'class':'API'}).contents[0]
    
    return result

def map_word_old(to_translate = 'love', from_language = 'en'):

    reader  = list(csv.reader(open('Language_names.txt','rb'), delimiter='\t'))
    lang_codes = [row[0] for row in reader[1:]]
    lang_names = [row[3] for row in reader[1:]]
    lang_names = [l.decode('utf-8') for l in lang_names]

    flower = mtranslate(to_translate,from_language)
    matches = list(set(flower[2]) & set(lang_names))
    non_matches = list((set(flower[2]) ^ set(lang_names)).intersection(set(lang_names)))

    to_replace = [lang_codes[lang_names.index(m)] for m in matches]
    replace_by = [flower[1][flower[2].index(m)] for m in matches]
    
    to_replace.extend([lang_codes[lang_names.index(m)] for m in non_matches])
    replace_by.extend([u'']*len(non_matches))
    
    replace_by = [re.sub(' \(.*\)','',s) for s in replace_by]
    
    test   = codecs.open('Languages-Europe.svg','rU','utf-8').read()

    for i in range(len(to_replace)):
        test = test.replace(u'>' + to_replace[i] + u'</text>','>' + replace_by[i] + u'</text>')

    with codecs.open('Languages_Europe_' + to_translate + '.svg','wU','utf-8') as fi:
        fi.write(test)
    with codecs.open('Languages_Europe_last_output.svg','wU','utf-8') as fi2:
        fi2.write(test)
        
def map_word(to_translate = 'love', from_language = 'en'):
    '''
    This in an updated version of map_word_old, using a more legible map
    '''

    reader  = list(csv.reader(open('Language_names.txt','rt',encoding = 'utf-8'), delimiter='\t'))
    lang_codes = [row[0] for row in reader[1:]]
    lang_names = [row[1] for row in reader[1:]]

    flower = mtranslate(to_translate, from_language)
    matches = list(set(flower[2]) & set(lang_names))
    non_matches = list((set(flower[2]) ^ set(lang_names)).intersection(set(lang_names)))

    to_replace = [lang_codes[lang_names.index(m)] for m in matches]
    replace_by = [flower[1][flower[2].index(m)].lower() for m in matches]
    
    to_replace.extend([lang_codes[lang_names.index(m)] for m in non_matches])
    replace_by.extend([u'']*len(non_matches))
    
    to_replace.append(u'word')
    replace_by.append(u'\"' + to_translate + '\" in Europe')    
    
    replace_by = [re.sub(' \(.*\)','',s) for s in replace_by]
    
    test   = codecs.open('Simplified_Languages_of_Europe_map_base.svg','rU','utf-8').read()

    for i in range(len(to_replace)):
        test = test.replace(u'style="font-style:normal;-inkscape-font-specification:Arial">' + to_replace[i] + u'</tspan>',
                            u'style="font-style:normal;-inkscape-font-specification:Arial">' + replace_by[i] + u'</tspan>')
        
    with codecs.open('Simplified_Languages_of_Europe_map_' + to_translate + '.svg','w','utf-8') as fi:
        fi.write(test)
    with codecs.open('Simplified_Languages_of_Europe_map_last_output.svg','w','utf-8') as fi2:
        fi2.write(test)
        
if __name__ == '__main__':
        to_translate = 'love'
        language = 'en'
        mtranslate(to_translate, language)
