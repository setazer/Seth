#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Imported from isida by quality(quality@botaq.net)
#Official conference - botaq@conference.jabber.ru
#Thanks to Disabler - http://isida.googlecode.com/


def calc(t, s, text):
        legal = ['0','1','2','3','4','5','6','7','8','9','*','/','+','-','(',')','=','^','!',' ','<','>','.']
        ppc = 1
        for tt in text:
                all_ok = 0
                for ll in legal:
                        if tt==ll:
                                all_ok = 1
                                break
                if not all_ok:
                        ppc = 0
                        break
	if text.count('**'):
		ppc = 0

        if ppc:        
                try:
                        text = str(eval(text))
                except:
                        text = u'я не могу это посчитать'
        else:
                text = u'выражение недопустимо'
	s.msg(t, text)

	
bot.register_cmd_handler(calc, u'.calc')