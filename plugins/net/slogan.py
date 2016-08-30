# -*- coding: utf-8 -*-

import urllib, urllib2, re
    
def slogan_rsl(who):
    result = u'Неизвестная ошибка'
    try:
        url = 'http://slogen.ru/pda/index.php'
        nick = who.encode('utf-8')
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        values = {'slogan':nick}
        headers = { 'User-Agent' : user_agent}
        data = urllib.urlencode(values)
        req = urllib2.Request(url, data, headers)
        response = urllib2.urlopen(req)
        the_page = response.read()
        response.close()
        regexp = re.compile('<div class="slogan1">(.*)</div><div')
        str = regexp.findall(the_page)
        result = str[0].decode('utf-8')
    except:
        result = u'Не получилось :('
    return result

def handler_slogan(t, s, p):
    if p: 
        result = slogan_rsl(p.strip())
    else:
        result = slogan_rsl(s.nick)
    s.msg(t, result)

bot.register_cmd_handler(handler_slogan, u'.slogan')