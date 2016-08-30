#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Imported from isida by quality(quality@botaq.net)
#Official conference - botaq@conference.jabber.ru
#Thanks to Disabler - http://isida.googlecode.com/


def true(t, s, text):
	if text == '': msg = u'чо чо?'
	else:
		idx = 0
		for tmp in text: idx += ord(tmp)
		idx = int((idx/100.0 - int(idx/100))*100)
		msg = u'ваше утверждение верно с вероятностью '+str(idx)+u'%'
	s.msg(t, msg)

	
bot.register_cmd_handler(true, u'.true')
