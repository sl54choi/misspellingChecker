# -*- coding: utf-8 -*-
__author__ = 'electopx@gmail.com'

import re
import sys
import time
import pandas as pd
from enchant import DictWithPWL
from urllib.request import urlopen
from urllib.request import Request
from pandas import Series, DataFrame
#import pattern.en import singularize
from enchant.checker import SpellChecker
from urllib.error import URLError, HTTPError
from bs4 import BeautifulSoup, NavigableString

inputfile = False
inputname, outputname, logname, targeturl = '', '', '', ''

# The most common file types and file extensions
excludedfiles = '.aif.cda.mid.mp3.mpa.ogg.wav.wma.wpl.7z.arj.deb.pkg.rar.rpm.tar.z.zip.bin.dmg.iso.toa.vcd.csv.dat.db.log.mdb.sav.sql.tar.xml.apk.bat.bin.cgi.com.exe.gad.jar.py.wsf.fnt.fon.otf.ttf.ai.bmp.gif.ico.jpe.png.ps.psd.svg.tif.asp.cer.cfm.cgi.js.jsp.par.php.py.rss.key.odp.pps.ppt.ppt.c.cla.cpp.cs.h.jav.sh.swi.vb.ods.xlr.xls.xls.bak.cab.cfg.cpl.cur.dll.dmp.drv.icn.ico.ini.lnk.msi.sys.tmp.3g2.3gp.avi.flv.h26.m4v.mkv.mov.mp4.mpg.rm.swf.vob.wmv.doc.odt.pdf.rtf.tex.txt.wks.wpd'
#useragent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36"
useragent = 'user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36'

def cleanHtml(text):

    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, ' ', text)

    return cleantext

'''
def checkplural(word):
    text = singularize(word)
    return text
'''

def removeUnicode(text):

    mtext = ''
    words = text.split(' ')
    for word in words:
        #print ('before: ', word)
        if word.find('\\') < 0:
            mtext = mtext + ' ' + word
            #print ('after: ', word)

    return mtext

def removeInvalidTag(text):

    mtext = text
    mtext.replace('<b>', '').replace('</b>', '').\
    replace('<i>', '').replace('</i>', '').\
    replace('<u>', '').replace('</u>', '').\
    replace('<strong>', '').replace('</strong>', '').\
    replace('<em>', '').replace('</em>', '').\
    replace('<cite>', '').replace('</cite>', '').\
    replace('<small>', '').replace('</small>', '')

    return mtext

def unescape(text):

    text = text.replace('&amp;', '&').\
    replace('&quot;', '"').\
    replace('&apos;', "'").\
    replace('&lt;', '<').\
    replace('&gt;', '>').\
    replace('&nbsp;', ' ')

    return text

def unicode2ascii(text):

    #UTF-8 encoding table and Unicode characters : U+0000 to U02CF)
    text = text.replace('\\xe2\\x80\\x99', "'").\
    replace('\\xc2\\xa0', ' ').replace('\\xc2\\xa1', '¡').\
    replace('\\xc2\\xa2', '¢').replace('\\xc2\\xa3', '£').\
    replace('\\xc2\\xa4', '¤').replace('\\xc2\\xa5', '¥').\
    replace('\\xc2\\xa6', '¦').replace('\\xc2\\xa7', '§').\
    replace('\\xc2\\xa8', '¨').replace('\\xc2\\xa9', '©').\
    replace('\\xc2\\xaa', 'ª').replace('\\xc2\\xab', '«').\
    replace('\\xc2\\xac', '¬').replace('\\xc2\\xad', ' ').\
    replace('\\xc2\\xae', '®').replace('\\xc2\\xaf', '¯').\
    replace('\\xc2\\xb0', '°').replace('\\xc2\\xb1', '±').\
    replace('\\xc2\\xb2', '²').replace('\\xc2\\xb3', '³').\
    replace('\\xc2\\xb4', '´').replace('\\xc2\\xb5', 'µ').\
    replace('\\xc2\\xb6', '¶').replace('\\xc2\\xb7', '·').\
    replace('\\xc2\\xb8', '¸').replace('\\xc2\\xb9', '¹').\
    replace('\\xc2\\xba', 'º').replace('\\xc2\\xbb', '»').\
    replace('\\xc2\\xbc', '¼').replace('\\xc2\\xbd', '½').\
    replace('\\xc2\\xbe', '¾').replace('\\xc2\\xbf', '¿').\
    replace('\\xc3\\x80', 'À').replace('\\xc3\\x81', 'Á').\
    replace('\\xc3\\x82', 'Â').replace('\\xc3\\x83', 'Ã').\
    replace('\\xc3\\x84', 'Ä').replace('\\xc3\\x85', 'Å').\
    replace('\\xc3\\x86', 'Æ').replace('\\xc3\\x87', 'Ç').\
    replace('\\xc3\\x88', 'È').replace('\\xc3\\x89', 'É').\
    replace('\\xc3\\x8a', 'Ê').replace('\\xc3\\x8b', 'Ë').\
    replace('\\xc3\\x8c', 'Ì').replace('\\xc3\\x8d', 'Í').\
    replace('\\xc3\\x8e', 'Î').replace('\\xc3\\x8f', 'Ï').\
    replace('\\xc3\\x90', 'Ð').replace('\\xc3\\x91', 'Ñ').\
    replace('\\xc3\\x92', 'Ò').replace('\\xc3\\x93', 'Ó').\
    replace('\\xc3\\x94', 'Ô').replace('\\xc3\\x95', 'Õ').\
    replace('\\xc3\\x96', 'Ö').replace('\\xc3\\x97', '×').\
    replace('\\xc3\\x98', 'Ø').replace('\\xc3\\x99', 'Ù').\
    replace('\\xc3\\x9a', 'Ú').replace('\\xc3\\x9b', 'Û').\
    replace('\\xc3\\x9c', 'Ü').replace('\\xc3\\x9d', 'Ý').\
    replace('\\xc3\\x9e', 'Þ').replace('\\xc3\\x9f', 'ß').\
    replace('\\xc3\\xa0', 'à').replace('\\xc3\\xa1', 'á').\
    replace('\\xc3\\xa2', 'â').replace('\\xc3\\xa3', 'ã').\
    replace('\\xc3\\xa4', 'ä').replace('\\xc3\\xa5', 'å').\
    replace('\\xc3\\xa6', 'æ').replace('\\xc3\\xa7', 'ç').\
    replace('\\xc3\\xa8', 'è').replace('\\xc3\\xa9', 'é').\
    replace('\\xc3\\xaa', 'ê').replace('\\xc3\\xab', 'ë').\
    replace('\\xc3\\xac', 'ì').replace('\\xc3\\xad', 'í').\
    replace('\\xc3\\xae', 'î').replace('\\xc3\\xaf', 'ï').\
    replace('\\xc3\\xb0', 'ð').replace('\\xc3\\xb1', 'ñ').\
    replace('\\xc3\\xb2', 'ò').replace('\\xc3\\xb3', 'ó').\
    replace('\\xc3\\xb4', 'ô').replace('\\xc3\\xb5', 'õ').\
    replace('\\xc3\\xb6', 'ö').replace('\\xc3\\xb7', '÷').\
    replace('\\xc3\\xb8', 'ø').replace('\\xc3\\xb9', 'ù').\
    replace('\\xc3\\xba', 'ú').replace('\\xc3\\xbb', 'û').\
    replace('\\xc3\\xbc', 'ü').replace('\\xc3\\xbd', 'ý').\
    replace('\\xc3\\xbe', 'þ').replace('\\xc3\\xbf', 'ÿ').\
    replace('\\xc4\\x80', 'Ā').replace('\\xc4\\x81', 'ā').\
    replace('\\xc4\\x82', 'Ă').replace('\\xc4\\x83', 'ă').\
    replace('\\xc4\\x84', 'Ą').replace('\\xc4\\x85', 'ą').\
    replace('\\xc4\\x86', 'Ć').replace('\\xc4\\x87', 'ć').\
    replace('\\xc4\\x88', 'Ĉ').replace('\\xc4\\x89', 'ĉ').\
    replace('\\xc4\\x8a', 'Ċ').replace('\\xc4\\x8b', 'ċ').\
    replace('\\xc4\\x8c', 'Č').replace('\\xc4\\x8d', 'č').\
    replace('\\xc4\\x8e', 'Ď').replace('\\xc4\\x8f', 'ď').\
    replace('\\xc4\\x90', 'Đ').replace('\\xc4\\x91', 'đ').\
    replace('\\xc4\\x92', 'Ē').replace('\\xc4\\x93', 'ē').\
    replace('\\xc4\\x94', 'Ĕ').replace('\\xc4\\x95', 'ĕ').\
    replace('\\xc4\\x96', 'Ė').replace('\\xc4\\x97', 'ė').\
    replace('\\xc4\\x98', 'Ę').replace('\\xc4\\x99', 'ę').\
    replace('\\xc4\\x9a', 'Ě').replace('\\xc4\\x9b', 'ě').\
    replace('\\xc4\\x9c', 'Ĝ').replace('\\xc4\\x9d', 'ĝ').\
    replace('\\xc4\\x9e', 'Ğ').replace('\\xc4\\x9f', 'ğ').\
    replace('\\xc4\\xa0', 'Ġ').replace('\\xc4\\xa1', 'ġ').\
    replace('\\xc4\\xa2', 'Ģ').replace('\\xc4\\xa3', 'ģ').\
    replace('\\xc4\\xa4', 'Ĥ').replace('\\xc4\\xa5', 'ĥ').\
    replace('\\xc4\\xa6', 'Ħ').replace('\\xc4\\xa7', 'ħ').\
    replace('\\xc4\\xa8', 'Ĩ').replace('\\xc4\\xa9', 'ĩ').\
    replace('\\xc4\\xaa', 'Ī').replace('\\xc4\\xab', 'ī').\
    replace('\\xc4\\xac', 'Ĭ').replace('\\xc4\\xad', 'ĭ').\
    replace('\\xc4\\xae', 'Į').replace('\\xc4\\xaf', 'į').\
    replace('\\xc4\\xb0', 'İ').replace('\\xc4\\xb1', 'ı').\
    replace('\\xc4\\xb2', 'Ĳ').replace('\\xc4\\xb3', 'ĳ').\
    replace('\\xc4\\xb4', 'Ĵ').replace('\\xc4\\xb5', 'ĵ').\
    replace('\\xc4\\xb6', 'Ķ').replace('\\xc4\\xb7', 'ķ').\
    replace('\\xc4\\xb8', 'ĸ').replace('\\xc4\\xb9', 'Ĺ').\
    replace('\\xc4\\xba', 'ĺ').replace('\\xc4\\xbb', 'Ļ').\
    replace('\\xc4\\xbc', 'ļ').replace('\\xc4\\xbd', 'Ľ').\
    replace('\\xc4\\xbe', 'ľ').replace('\\xc4\\xbf', 'Ŀ').\
    replace('\\xc5\\x80', 'ŀ').replace('\\xc5\\x81', 'Ł').\
    replace('\\xc6\\x80', 'ƀ').replace('\\xc6\\x81', 'Ɓ').\
    replace('\\xc6\\x82', 'Ƃ').replace('\\xc6\\x83', 'ƃ').\
    replace('\\xc6\\x84', 'Ƅ').replace('\\xc6\\x85', 'ƅ').\
    replace('\\xc6\\x86', 'Ɔ').replace('\\xc6\\x87', 'Ƈ').\
    replace('\\xc6\\x88', 'ƈ').replace('\\xc6\\x89', 'Ɖ').\
    replace('\\xc6\\x8a', 'Ɗ').replace('\\xc6\\x8b', 'Ƌ').\
    replace('\\xc6\\x8c', 'ƌ').replace('\\xc6\\x8d', 'ƍ').\
    replace('\\xc6\\x8e', 'Ǝ').replace('\\xc6\\x8f', 'Ə').\
    replace('\\xc6\\x90', 'Ɛ').replace('\\xc6\\x91', 'Ƒ').\
    replace('\\xc6\\x92', 'ƒ').replace('\\xc6\\x93', 'Ɠ').\
    replace('\\xc6\\x94', 'Ɣ').replace('\\xc6\\x95', 'ƕ').\
    replace('\\xc6\\x96', 'Ɩ').replace('\\xc6\\x97', 'Ɨ').\
    replace('\\xc6\\x98', 'Ƙ').replace('\\xc6\\x99', 'ƙ').\
    replace('\\xc6\\x9a', 'ƚ').replace('\\xc6\\x9b', 'ƛ').\
    replace('\\xc6\\x9c', 'Ɯ').replace('\\xc6\\x9d', 'Ɲ').\
    replace('\\xc6\\x9e', 'ƞ').replace('\\xc6\\x9f', 'Ɵ').\
    replace('\\xc6\\xa0', 'Ơ').replace('\\xc6\\xa1', 'ơ').\
    replace('\\xc6\\xa2', 'Ƣ').replace('\\xc6\\xa3', 'ƣ').\
    replace('\\xc6\\xa4', 'Ƥ').replace('\\xc6\\xa5', 'ƥ').\
    replace('\\xc6\\xa6', 'Ʀ').replace('\\xc6\\xa7', 'Ƨ').\
    replace('\\xc6\\xa8', 'ƨ').replace('\\xc6\\xa9', 'Ʃ').\
    replace('\\xc6\\xaa', 'ƪ').replace('\\xc6\\xab', 'ƫ').\
    replace('\\xc6\\xac', 'Ƭ').replace('\\xc6\\xad', 'ƭ').\
    replace('\\xc6\\xae', 'Ʈ').replace('\\xc6\\xaf', 'Ư').\
    replace('\\xc6\\xb0', 'ư').replace('\\xc6\\xb1', 'Ʊ').\
    replace('\\xc6\\xb2', 'Ʋ').replace('\\xc6\\xb3', 'Ƴ').\
    replace('\\xc6\\xb4', 'ƴ').replace('\\xc6\\xb5', 'Ƶ').\
    replace('\\xc6\\xb6', 'ƶ').replace('\\xc6\\xb7', 'Ʒ').\
    replace('\\xc6\\xb8', 'Ƹ').replace('\\xc6\\xb9', 'ƹ').\
    replace('\\xc6\\xba', 'ƺ').replace('\\xc6\\xbb', 'ƻ').\
    replace('\\xc6\\xbc', 'Ƽ').replace('\\xc6\\xbd', 'ƽ').\
    replace('\\xc6\\xbe', 'ƾ').replace('\\xc6\\xbf', 'ƿ').\
    replace('\\xc7\\x80', 'ǀ').replace('\\xc7\\x81', 'ǁ').\
    replace('\\xc9\\x90', 'ɐ').replace('\\xc9\\x91', 'ɑ').\
    replace('\\xc9\\x92', 'ɒ').replace('\\xc9\\x93', 'ɓ').\
    replace('\\xc9\\x94', 'ɔ').replace('\\xc9\\x95', 'ɕ').\
    replace('\\xc9\\x96', 'ɖ').replace('\\xc9\\x97', 'ɗ').\
    replace('\\xc9\\x98', 'ɘ').replace('\\xc9\\x99', 'ə').\
    replace('\\xc9\\x9a', 'ɚ').replace('\\xc9\\x9b', 'ɛ').\
    replace('\\xc9\\x9c', 'ɜ').replace('\\xc9\\x9d', 'ɝ').\
    replace('\\xc9\\x9e', 'ɞ').replace('\\xc9\\x9f', 'ɟ').\
    replace('\\xc9\\xa0', 'ɠ').replace('\\xc9\\xa1', 'ɡ').\
    replace('\\xc9\\xa2', 'ɢ').replace('\\xc9\\xa3', 'ɣ').\
    replace('\\xc9\\xa4', 'ɤ').replace('\\xc9\\xa5', 'ɥ').\
    replace('\\xc9\\xa6', 'ɦ').replace('\\xc9\\xa7', 'ɧ').\
    replace('\\xc9\\xa8', 'ɨ').replace('\\xc9\\xa9', 'ɩ').\
    replace('\\xc9\\xaa', 'ɪ').replace('\\xc9\\xab', 'ɫ').\
    replace('\\xc9\\xac', 'ɬ').replace('\\xc9\\xad', 'ɭ').\
    replace('\\xc9\\xae', 'ɮ').replace('\\xc9\\xaf', 'ɯ').\
    replace('\\xc9\\xb0', 'ɰ').replace('\\xc9\\xb1', 'ɱ').\
    replace('\\xc9\\xb2', 'ɲ').replace('\\xc9\\xb3', 'ɳ').\
    replace('\\xc9\\xb4', 'ɴ').replace('\\xc9\\xb5', 'ɵ').\
    replace('\\xc9\\xb6', 'ɶ').replace('\\xc9\\xb7', 'ɷ').\
    replace('\\xc9\\xb8', 'ɸ').replace('\\xc9\\xb9', 'ɹ').\
    replace('\\xc9\\xba', 'ɺ').replace('\\xc9\\xbb', 'ɻ').\
    replace('\\xc9\\xbc', 'ɼ').replace('\\xc9\\xbd', 'ɽ').\
    replace('\\xc9\\xbe', 'ɾ').replace('\\xc9\\xbf', 'ɿ').\
    replace('\\xca\\x80', 'ʀ').replace('\\xca\\x81', 'ʁ').\
    replace('\\xca\\x82', 'ʂ').replace('\\xca\\x83', 'ʃ').\
    replace('\\xca\\x84', 'ʄ').replace('\\xca\\x85', 'ʅ').\
    replace('\\xca\\x86', 'ʆ').replace('\\xca\\x87', 'ʇ').\
    replace('\\xca\\x88', 'ʈ').replace('\\xca\\x89', 'ʉ').\
    replace('\\xca\\x8a', 'ʊ').replace('\\xca\\x8b', 'ʋ').\
    replace('\\xca\\x8c', 'ʌ').replace('\\xca\\x8d', 'ʍ').\
    replace('\\xca\\x8e', 'ʎ').replace('\\xca\\x8f', 'ʏ').\
    replace('\\xca\\x90', 'ʐ').replace('\\xca\\x91', 'ʑ').\
    replace('\\xe2\\x80\\x90', '-').replace('\\xe2\\x80\\x91', '-').\
    replace('\\xe2\\x80\\x92', '-').replace('\\xe2\\x80\\x93', '-').\
    replace('\\xe2\\x80\\x94', '-').replace('\\xe2\\x80\\x94', '-').\
    replace('\\xe2\\x80\\x98', "'").replace('\\xe2\\x80\\x9b', "'").\
    replace('\\xe2\\x80\\x9c', '"').replace('\\xe2\\x80\\x9c', '"').\
    replace('\\xe2\\x80\\x9d', '"').replace('\\xe2\\x80\\x9e', '"').\
    replace('\\xe2\\x80\\x9f', '"').replace('\\xe2\\x80\\xa6', '...').\
    replace('\\xe2\\x80\\xb2', "'").replace('\\xe2\\x80\\xb3', "'").\
    replace('\\xe2\\x80\\xb4', "'").replace('\\xe2\\x80\\xb5', "'").\
    replace('\\xe2\\x80\\xb6', "'").replace('\\xe2\\x80\\xb7', "'").\
    replace('\\xe2\\x81\\xba', "+").replace('\\xe2\\x81\\xbb', "-").\
    replace('\\xe2\\x81\\xbc', "=").replace('\\xe2\\x81\\xbd', "(").\
    replace('\\xe2\\x81\\xbe', ")")

    return text

def getCode(tu):

    global useragent
    code, targetpage = '', ''
    status = False

    try:
        req = Request(tu)
        req.add_header('User-Agent', useragent)
        targetpage = urlopen(req)
        code = str(targetpage.status)
        print('\n[OK] The server could fulfill the request to\n%s' %tu)
        status = True
    except HTTPError as e:
        code = str(e.code)
        print('\n[ERR] HTTP Error: The server couldn\'t fulfill the request to\n%s\n+ Error Code: %s' %(tu, code))
    except URLError as e:
        code = e.reason
        print('\n[ERR] URL Error: We failed to reach in\n%s\n+ Error Code: %s' %(tu, code))

    return (status, targetpage)

def init():

    global inputname, outputname, logname, targeturl
    args = sys.argv[0:]
    optionLen = len(args)

    # e.g.: python mt.py -i input.csv -o output.csv -l misspelling.log
    for i in range(optionLen-1):
        if args[i].upper() == '-I':	# -I: input file name
            data = str(args[i+1])
            inputname = data
            inputfile = True
        elif args[i].upper() == '-O':	# -O: output file name
            data = str(args[i+1])
            outputname = data
        elif args[i].upper() == '-L':	# -L: log file name
            data = str(args[i+1])
            logname = data
        elif args[i].upper() == '-T':	# -T: target URL
            data = str(args[i+1])
            targeturl = data
            inputfile = False
    if inputname == '' or targeturl == '':
        print ('[ERR] Please be sure to include either the input file or the target url.')
        return False
    if outputname.find('.csv') < 0:
        print ('[ERR] Please use ".csv" as the extension of output file.')
        return False
    elif logname.find('.log') < 0:
        print ('[ERR] Please use ".log" as the extension of log file.')
        return False

    return True

if __name__ == '__main__':

    count = 0
    text, output = '', ''
    valid_tags = ['p', 'span']
    chkr = SpellChecker("en_US")
    excludedwords = 'www,href,http,https,html,br'
    result = DataFrame(columns=('misspelling', 'duplication', 'wiki', 'wikiurl', 'url', 'sentence' ))

    if init():
        f = open(logname, 'w')
        df = DataFrame(columns=('link', 'code'))
        if inputfile:
            df = pd.read_csv(inputname)
            print (df.to_string())
        else:
            rows = {'link': targeturl, 'code': -1}
            df = df.append(rows, ignore_index=True)
        if df['link'][0].find('github') >= 0:
            valid_tags = ['article']
        for link in df['link']:
            if link[len(link) - 1] == '/':
                link = link[:-1]
            tokens = link.split('/')
            lasttoken = tokens[len(tokens) - 1]
            if link.find('?') >= 0 or lasttoken.find('#') >= 0 or lasttoken.find('%') >= 0 or (len(tokens) > 3 and excludedfiles.find(lasttoken[-4:]) >= 0):
                continue
            #page = urlopen(link)
            (status, page) = getCode(link)
            if status == False:
                continue
            # Getting contents with re library from html file
            with urlopen(link) as response:
                html = response.read().decode("utf-8")
            if link.find('github') >= 0:
                body = re.search('<article.*/article>', html, re.I|re.S)
                body = body.group()
            else:
                body = re.search('<body.*/body>', html, re.I|re.S)
                body = body.group()
                body = body.replace('<span', '|<span').replace('span>', 'span>|')
            body = body.replace('<p', '|<p').replace('p>', 'p>|').\
                replace('<b>', '').replace('</b>', '').\
                replace('<i>', '').replace('</i>', '').\
                replace('<u>', '').replace('</u>', '').\
                replace('<strong>', '').replace('</strong>', '').\
                replace('<em>', '').replace('</em>', '').\
                replace('<cite>', '').replace('</cite>', '').\
                replace('<small>', '').replace('</small>', '')
            body = re.sub('<script.*?>.*?</script>', ' ', body, 0, re.I|re.S)
            body = re.sub('<.+?>', ' ', body, 0, re.I|re.S)
            body = u' '.join(body.split()).encode('utf-8').strip()
            tokens = str(body).split('|')
            tokens = [x.strip() for x in tokens if x.strip()]
            tokens[0] = tokens[0][2:]
            body = "\n".join(tokens)
            print (body)
            #print (tokens)
            output = output + '\n* ' + link
            for token in tokens:
                text = unescape(token)
                print ('\n + Link: %s' %link)
                if type(text) != 'unicode':
                    mtext = unicode2ascii(str(text.encode('utf-8')))
                    output = output + '\n + ' + mtext[1:]
                    print (' ++ Content: %s' %mtext[1:])
                    mtext = removeUnicode(mtext[1:])
                    chkr.set_text(mtext)
                else:
                    output = output + '\n + ' + text
                    print (' + Content: %s' %(text))
                    chkr.set_text(text)
                for err in chkr:
                    if excludedwords.find(str(err.word)) < 0:
                        #err.word = unicode2ascii(str(err.word.encode('utf-8')))[2:-1]
                        if err.word.find('\\') >= 0:
                            continue
                        #err.word = checkplural(err.word)
                        count = count + 1
                        adding = '[ERR] (' + str(count) + ') ' + str(err.word)
                        print ('%s' %adding)
                        output = output + '\n' + adding
                        rows = [str(err.word), -1, -1, '', link, text]
                        result.loc[len(result)] = rows
        # Counting for duplicated misspellings
        for rowdata in result.values:
            if rowdata[1] == -1:	# rowdata[1]: duplication
                duplicatedcount = len(result.loc[result['misspelling'] == rowdata[0]])
                result.loc[result['misspelling'] == rowdata[0], 'duplication'] = duplicatedcount
            else:
                continue
        # Getting values from Wikipedia
        print ('\n + Finding words misspelled on Wikipedia')
        for rowdata in result.values:
            #time.sleep(0.2)
            rowdata[0] = unicode2ascii(str(rowdata[0].encode('utf-8')))[2:-1]
            if rowdata[0].find('\\') >= 0:
                continue
            if rowdata[1] < 3 and rowdata[2] == -1:	# rowdata[2]: wiki
                tu = 'https://en.wikipedia.org/w/index.php?search=' + rowdata[0]
                req = Request(tu)
                req.add_header('User-Agent', useragent)
                targetpage = urlopen(req)
                soup = BeautifulSoup(targetpage, 'lxml')
                if len(soup.findAll('a', attrs={'href': re.compile('/wiki/Wikipedia:Articles_for_creation')})) > 0:
                    result.loc[result['misspelling'] == rowdata[0], 'wiki'] = False
                    #result.loc[result['misspelling'] == rowdata[0], 'wikiurl'] = browser.current_url
                    result.loc[result['misspelling'] == rowdata[0], 'wikiurl'] = targetpage.geturl()
                    messages = '[ERR] ' + rowdata[0] + ': Not found'
                    output = output + '\n' + messages + '\n + Link: ' + targetpage.geturl()
                    messages = messages + ' @ <a href="' + targetpage.geturl() + '" target="_blank">' + targetpage.geturl() + '</a>'
                    print (messages)
                else:
                    result.loc[result['misspelling'] == rowdata[0], 'wiki'] = True
                    #result.loc[result['misspelling'] == rowdata[0], 'wikiurl'] = browser.current_url
                    result.loc[result['misspelling'] == rowdata[0], 'wikiurl'] = targetpage.geturl()
                    messages = '[OK] ' + rowdata[0] + ': Found\n + Link: ' + targetpage.geturl()
                    print (messages)
                    output = output + '\n' + messages
        # Sorting result values
        result.sort_values(by=['duplication', 'wiki', 'misspelling', 'url'], ascending=[True, True, True, True], inplace=True)
        result.index = range(len(result))
        # Exporting to csv file
        result.to_csv(outputname, header=True, index=True)
        #print (result.to_string())
        #output = output + '\n' + result.to_string()
        f.write(output)
        f.close()
    else:
        f = open(logname, 'w')
        messages = '[ERR] Initialization faliure'
        print (messages)
        output = output + '\n' + messages
        f.write(output)
        f.close()
