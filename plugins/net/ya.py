#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Imported from talisman by quality(quality@botaq.net)
#Thanks to ferym - http://veganet.org.ru/


def yandex(t, s, p):
    try:
      if p:
        req = urllib2.Request('http://yandex.ru/msearch?s=all&query='+p.encode('utf-8').replace(' ','%20').replace('@','%40'))
        req.add_header = ('User-agent', 'Mozilla/5.0')
        r = urllib2.urlopen(req)
        target = r.read()
        od = re.search('<li>',target)
        message = target[od.end():]
        message = message[:re.search('</li>',message).start()]
        message = '\n' + message.strip()
        message = decode(message)
        s.msg(t, unicode(message,'UTF-8'))
      else:
        s.msg(t, u'а что искать то?')
    except:
        s.msg(t, u'по вашему запросу ничего не найдено')
              
			  
def decode(text):
    return strip_tags.sub('', text.replace('<br />','\n').replace('<br>','\n').replace('&#151;','-')).replace('&nbsp;',' ').replace('&lt;','<').replace('&gt;','>').replace('&quot;','"').replace('\t','').replace('<a href=\"','').replace('\" target=\"_blank\">','').replace('<b>','').replace('</b>','').replace('</a>','').replace('<div class=\"info\">','').replace('</div','')


bot.register_cmd_handler(yandex, u'.yandex')
