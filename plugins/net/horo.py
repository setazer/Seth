#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Imported from talisman by quality(quality@botaq.net)
#Official conference - botaq@conference.jabber.ru
#Thanks to Als - http://svn.xmpp.ru/repos/talisman/trunk
	

import urllib2,re
from re import compile as re_compile
strip_tags = re_compile(r'<[^<>]+>')


horodb={u'\u0432\u043e\u0434\u043e\u043b\u0435\u0439': u'11', u'\u0440\u0430\u043a': u'4', u'\u0432\u0435\u0441\u044b': u'7', u'\u043a\u043e\u0437\u0435\u0440\u043e\u0433': u'10', u'\u0434\u0435\u0432\u0430': u'6', u'\u0431\u043b\u0438\u0437\u043d\u0435\u0446\u044b': u'3', u'\u0441\u0442\u0440\u0435\u043b\u0435\u0446': u'9', u'\u0441\u043a\u043e\u0440\u043f\u0438\u043e\u043d': u'8', u'\u0442\u0435\u043b\u0435\u0446': u'2', u'\u043b\u0435\u0432': u'5', u'\u043e\u0432\u0435\u043d': u'1', u'\u0440\u044b\u0431\u044b': u'12'}


def horo(t, s, p):
	if p:
		if p==u'all':
			s.msg(t,', '.join(horodb.keys()))
			return
		if horodb.has_key(string.lower(p)):
			req = urllib2.Request('http://horo.gala.net/?lang=ru&sign='+horodb[string.lower(p)])
			req.add_header = ('User-agent', 'Mozilla/5.0')
			r = urllib2.urlopen(req)
			target = r.read()
			od = re.search('<span class=SignName>',target)
			h1 = target[od.end():]
			h1 = h1[:re.search('</span>',h1).start()]
			h1 += '\n'
			od = re.search('<td class=blackTextBold nowrap>',target)
			h2 = target[od.end():]
			h2 = h2[:re.search('</td>',h2).start()]
			h2 += '\n'
			od = re.search('<td class=stext>',target)
			h3 = target[od.end():]
			h3 = h3[:re.search('</td>',h3).start()]
			if len(h3)<5:
				s.msg(t,u'пока что гороскопа нету')
				return
			message = h1+h2+h3
			message = decode(message)
			message=message.strip()
			s.msg(t,unicode(message,'windows-1251'))
		else:
			s.msg(t, u'что это за знак зодиака?')	
			return	
	else:
		s.msg(t,u'для какого знака гороскоп смотреть-то?')
		return


def decode(text):
    return strip_tags.sub('', text.replace('<br>','\n')).replace('&nbsp;', ' ').replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"').replace('\t','').replace('>[:\n','')
	
	
bot.register_cmd_handler(horo, u'.horo')	