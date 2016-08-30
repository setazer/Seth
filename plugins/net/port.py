#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Imported from isida by quality(quality@botaq.net)
#Official conference - botaq@conference.jabber.ru
#Thanks to Disabler - http://isida.googlecode.com/


def port(t, s, text):
	if text.count('.') and text.count(':') and len(text) > 5:
		if text.count(' '):
			try: mtype = int(text.split(' ')[1])
			except: mtype = 1
			if mtype < 1: mtype = 1
			elif mtype >5: mtype = 5
			text = text.split(' ')[0]
		else: mtype = 1
		url = u'http://status.blackout-gaming.net/status.php?dns='+text.replace(':','&port=')+u'&style=t'+str(mtype)
		body = urllib.urlopen(url).read()
		body = (body.split('("')[1])[:-3]
		msg = u'статус сервера: '+ body
	else: msg = u'что проверяем?'
	s.msg(t, msg)

	
bot.register_cmd_handler(port, u'.port')
