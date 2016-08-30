#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Imported from isida by quality(quality@botaq.net)
#Thanks to Disabler - http://isida.googlecode.com/


user_agent='Mozilla/5.0 (X11; U; Linux x86_64; ru; rv:1.9.0.4) Gecko/2008120916 Gentoo Firefox/3.0.4'

def header(t, s, text):
	if len(text):
		if text[:7] !='http://': text = 'http://'+text
		req = urllib2.Request(text)
		req.add_header('User-Agent',user_agent)
		try: body = str(urllib2.urlopen(req).headers)
		except: body = u'что-то не получается!'
	else: body = u'что посмотреть?'
	s.msg(t, body)


        
bot.register_cmd_handler(header, u'.header')
