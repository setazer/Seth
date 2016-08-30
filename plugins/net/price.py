#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Imported from isida by quality(quality@botaq.net)
#Official conference - botaq@conference.jabber.ru
#Thanks to ferym - http://veganet.org.ru/


def price(t, s, p):
    try:
        if p.count('http://'):
            s.msg(t, u'формат ввода сайта domain.tld')
            return
        if len(p):
            p = p.split('.')[-2].lower()+'.'+p.split('.')[-1].lower()
            req = 'http://www.webvaluer.org/ru/www.'+p
            r = urllib2.urlopen(req)
            target = r.read()
            od = re.search('<span style=\"color:green; font-weight:bold;\">',target)
            message = target[od.end():]
            message = message[:re.search('</span></h1>',message).start()]
            message = message.replace(',','')
            message = unicode(message.strip(),'utf-8')
            try: pos = message.find(re.findall(r'[0-9]',message)[0])
            except: pos = None
            if pos:
                if pos >= 2: message = message[pos:]+' '+message[:pos]
            s.msg(t, u'оценочная стоимость домена '+p.strip()+u' составляет - '+message)
        else:
            s.msg(t, u'какой сайт оценивать?')
    except:
        s.msg(t, u'не получилось обработать запрос')
    
	
bot.register_cmd_handler(price, u'.price')  
