#!/usr/bin/env python
# -*- coding: utf-8 -*-
# автор - quality(quality@botaq.net)
# оф.сайт - http://quality.wen.ru/ & http://www.botaq.net/


def jc(t, s, p):
    for tm in p:
        if ord(tm)<33 or ord(tm)>127:
            s.msg(t, u'пейши по английски комнату, сцуко!!11')
            return
    if p:
        req = urllib2.Request('http://jc.jabber.ru/search.html?search='+p)
        req.add_header = ('User-agent', 'Opera 9.50')
        r = urllib2.urlopen(req)
        target = r.read()
        od = re.search('<div align="left">',target)
        message = target[od.end():]
        message = message[:re.search('\n</ol>',message).start()]
    else:
        req = urllib2.Request('http://jc.jabber.ru')
        req.add_header = ('User-agent', 'Opera 9.50')
        r = urllib2.urlopen(req)
        target = r.read()
        od = re.search('<h3>',target)
        message = target[od.end():]
        message = message[:re.search('</table>',message).start()]
        
    message = jc(message)
    s.msg(t, unicode(message,'utf-8'))
              
			  
bot.register_cmd_handler(jc, u'.jc')

def jc(text):
    return strip_tags.sub('', text.replace('<font size="-2">',' ').replace('</td><td align="right" valign="top">',' ').replace('</font></td></tr><tr bgcolor="#ffffff">','\n').replace('<br><font size="-3">',' ').replace('&nbsp;',' ').replace('</td></tr>\n\n<tr bgcolor="#eeeeee"><td align="right" valign="top">','\n').replace('</td></tr>\n\n<tr bgcolor="#ffffff"><td align="right" valign="top">','\n').replace('<br><font color="gray">','\n').replace('</font></a><br>\n','\nОписание комнаты: ').replace('\n</div>','\n').replace('\n\n\n<ol start=1>','').replace('  ·  ','\n'))
