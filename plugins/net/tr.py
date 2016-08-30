#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Imported from talisman by quality(quality@botaq.net)
#Official conference - botaq@conference.jabber.ru
#Thanks to Gigabyte, Disabler


import urllib,httplib,re,simplejson
from string import replace
	
	
def translate(t,s,p):
        if p == '':
                reply(type,source, u'иии?')
		return
        trlang = ['sq','ar','bg','ca','zh-CN','zh-TW','hr','cs','da',
		  'nl','en','et','tl','fi','fr','gl','de','el','iw',
		  'hi','hu','id','it','ja','ko','lv','lt','mt','no',
		  'pl','pt','ro','ru','sr','sk','sl','es','sv','th','tr','uk','vi']
	if p.strip()==u'langs':
                msg = u'доступные языки для перевода:\n'
                for tl in trlang: msg += tl+', '
                msg = msg[:-2]
                s.msg(t,msg)
                return
	else:
		if p.count(' ') > 1:
			p = p.split(' ',2)
			if trlang.count(p[0]) and trlang.count(p[1]) and p[2] != '':
				query = urllib.urlencode({'q' : p[2].encode("utf-8"),'langpair':p[0]+'|'+p[1]})
				url = u'http://ajax.googleapis.com/ajax/services/language/translate?v=1.0&%s'.encode("utf-8") % (query)
				search_results = urllib.urlopen(url)
				json = simplejson.loads(search_results.read())
				msg = json['responseData']['translatedText']
			else: msg = u'неправильно указан язык или нет текста для перевода. .tr langs - доступные языки'
		else: msg = u'формат команды: .tr с_какого на_какой текст'
		s.msg(t, msg)
		
		
bot.register_cmd_handler(translate, u'.tr')


def translate_auto(t,s,p):
	if p == '':
		s.msg(t, u'и что ты хочешь этим сказать?')
		return
	par=p.strip()
	rus = [u'а', u'б', u'в', u'г', u'д', u'е', u'ё', u'ж', u'з', u'и', u'й', u'к', u'л', u'м', u'н', u'о', u'п', u'р', u'с', u'т', u'у', u'ф', u'х', u'ц', u'ч', u'ш', u'щ', u'ъ', u'ь', u'ы', u'э', u'ю', u'я']
	eng = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
	k = 0
	i = 0
	lang = 'not'
	while (k != 1):
		if (par[i] in rus):
			lang = 're'
			k = 1
		else:
			if (par[i] in eng):
				lang = 'er'
				k = 1
			else:
				i += 1
				if (i == len(par)-1):
					k = 1
	if lang == 'not':
		s.msg(t, u'невозможно определить язык!')
		return
	p = lang + ' ' + p
	stsp=string.split(p, ' ', 1)
	langpairs={'er': 'en ru', 're': 'ru en','ef': 'en fr','ed': 'en de', 'df': 'de fr','ei': 'en it', 'es': 'en sp', 'ep': 'en pt', 'ek': 'en ko', 'ej': 'en ja'}
	if langpairs.has_key(stsp[0]):
		pair=langpairs[stsp[0]]
		pair=string.split(pair, ' ', 1)
		query = urllib.urlencode({'q' : stsp[1].encode("utf-8"),'langpair':pair[0]+'|'+pair[1]})
		url = u'http://ajax.googleapis.com/ajax/services/language/translate?v=1.0&%s'.encode("utf-8") % (query)
		search_results = urllib.urlopen(url)
		json = simplejson.loads(search_results.read())
		msg = json['responseData']['translatedText']
		s.msg(t,msg)
	else:
		s.msg(t,u'что это за язык?')
		
		
bot.register_cmd_handler(translate_auto, u'.atr')
