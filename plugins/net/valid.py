#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Imported from isida by quality(quality@botaq.net)
#Official conference - botaq@conference.jabber.ru
#Thanks to dr.Schmurge - http://isida.googlecode.com/


def valid(t, s, text):
	if text == '': text = s.nick
	ru_lit, en_lit, caps_lit = 0, 0, 0
	for tmp in text:
		if re.match(u'[a-z]|[A-Z]',tmp): en_lit+=1
		elif re.match(u'[а-я]|[А-Я]',tmp): ru_lit+=1
		if re.match(u'[A-Z]|[А-Я]',tmp): caps_lit+=1
	lt = len(text)
	if ru_lit<en_lit: idx, hl = float(ru_lit)/en_lit, 1
	elif ru_lit>en_lit: idx, hl = float(en_lit)/ru_lit, 2
	else: idx, hl = 0.5, None
	if (ru_lit == lt or en_lit == lt) and float(caps_lit)/lt <= 0.5: msg = u'100% Ъ-ник!'
	elif ru_lit+en_lit == 0: msg = u'ники без букв не Ъ!'
	elif ru_lit+en_lit+text.count(' ')+text.count('.') == lt: msg = u'кошерность ника - '+str(100-int(idx*100))+u'%'
	elif not ru_lit or not en_lit: msg = u'нормальный ник, а вот левые символы фтопку!'
	else: msg = u'кошерность ника - '+str(int(float(ru_lit+en_lit)/lt*100-int(idx*100)))+u'%'
	if float(caps_lit)/lt > 0.5: msg += u' много капса - '+ str(int(float(caps_lit)/lt*100))+u'%'

	msg += u' преобладают буквы: '
	if hl == 1: msg += u'латиница'
	elif hl == 2: msg += u'кирилица'
	else: msg += u'поровну'
	s.msg(t, msg)

	
bot.register_cmd_handler(valid, u'.valid')
