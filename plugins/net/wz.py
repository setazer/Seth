#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Imported from isida by quality(quality@botaq.net)
#Official conference - botaq@conference.jabber.ru
#Thanks to Disabler - http://isida.googlecode.com/


def sfind(mass,stri):
	for a in mass:
		if a.count(stri):
			return a
	return ''					


def weather(t, s, text):
	for tm in text:
		if ord(tm)<33 or ord(tm)>127:
			s.msg(t, u'ошибка в параметрах!')
			return
	text = text.upper()
	link = 'http://weather.noaa.gov/pub/data/observations/metar/decoded/'+text+'.TXT'
	f = urllib.urlopen(link)
	wzz = f.read()
	f.close()

	if wzz.count('Not Found'): msg = u'город не найден!'
	else:
		wzz = wzz.split('\n')

		wzr = []
		wzr.append(wzz[0])			# 0
		wzr.append(wzz[1])			# 1
		wzr.append(sfind(wzz,'Temperature'))	# 2
		wzr.append(sfind(wzz,'Wind'))		# 3
		wzr.append(sfind(wzz,'Relative'))	# 4
		wzr.append(sfind(wzz,'Sky'))		# 5
		wzr.append(sfind(wzz,'Weather'))	# 6
		wzr.append(sfind(wzz,'Visibility'))	# 7
		wzr.append(sfind(wzz,'Pressure'))	# 8

		if wzr[0].count(')'): msg = wzr[0][:wzr[0].find(')')+1]
		else: msg = wzr[0]
		msg += '\n'+ wzr[1]

		wzz1 = wzr[2].find(':')+1 # Temperature
		wzz2 = wzr[2].find('(',wzz1)
		wzz3 = wzr[2].find(')',wzz2)
		msg += '\n'+ wzr[2][:wzz1] + ' ' + wzr[2][wzz2+1:wzz3]

		wzz1 = wzr[3].find('(')
		wzz2 = wzr[3].find(')',wzz1)
		wzz3 = wzr[3].find(':',wzz2)
		msg += '\n'+ wzr[3][:wzz1-1] + wzr[3][wzz2+1:wzz3]

		msg += '\n'+ wzr[4]
		if len(wzr[5]): msg += ','+ wzr[5][wzr[5].find(':')+1:]
		if len(wzr[6]): msg += ','+ wzr[6][wzr[6].find(':')+1:]
		if not (len(wzr[5])+len(wzr[6])): msg += ', clear'

		msg += '\n'+ wzr[7][:-2]
		
		wzz1 = wzr[8].find('(')
		wzz2 = wzr[8].find(':',wzz1)
		wzz3 = wzr[8].find('(',wzz2)
		msg += ', '+ wzr[8][:wzz1-1]+': '+wzr[8][wzz3+1:-1]

	s.msg(t, msg)


def weather_short(t, s, text):
	for tm in text:
		if ord(tm)<33 or ord(tm)>127:
			s.msg(t, u'ошибка в параметрах!')
			return
	text = text.upper()
	link = 'http://weather.noaa.gov/pub/data/observations/metar/decoded/'+text+'.TXT'
	f = urllib.urlopen(link)
	wzz = f.read()
	f.close()

	if wzz.count('Not Found'): msg = u'город не найден!'
	else:
		wzz = wzz.split('\n')

		wzr = []
		wzr.append(wzz[0])			# 0
		wzr.append(sfind(wzz,'Temperature'))	# 2
		wzr.append(sfind(wzz,'Wind'))		# 3
		wzr.append(sfind(wzz,'Relative'))	# 4
		wzr.append(sfind(wzz,'Sky'))		# 5
		wzr.append(sfind(wzz,'Weather'))	# 6

		if wzr[0].count(')'): msg = wzr[0][:wzr[0].find(')')+1]
		else: msg = wzr[0]

		wzz1 = wzr[1].find(':')+1 # Temperature
		wzz2 = wzr[1].find('(',wzz1)
		wzz3 = wzr[1].find(')',wzz2)
		msg += ' | '+ wzr[1][:wzz1] + ' ' + wzr[1][wzz2+1:wzz3]

		wzz1 = wzr[2].find('(')
		wzz2 = wzr[2].find(')',wzz1)
		wzz3 = wzr[2].find(':',wzz2)
		msg += ' | '+ wzr[2][:wzz1-1] + wzr[2][wzz2+1:wzz3]
		msg += ' | '+ wzr[3]
		if len(wzr[4]): msg += ','+ wzr[4][wzr[4].find(':')+1:]
		if len(wzr[5]): msg += ','+ wzr[5][wzr[5].find(':')+1:]
		if not (len(wzr[4])+len(wzr[5])): msg += ', clear'
	s.msg(t, msg)


def weather_raw(t, s, text):
	for tm in text:
		if ord(tm)<33 or ord(tm)>127:
			s.msg(type, jid, nick, u'ошибка в параметрах!')
			return
	text = text.upper()
	link = 'http://weather.noaa.gov/pub/data/observations/metar/decoded/'+text+'.TXT'
	f = urllib.urlopen(link)
	msg = f.read()
	f.close()
	msg = msg[:-1]
	if msg.count('Not Found'): msg = u'город не найден!'
	s.msg(t, msg)


def weather_city(t, s, text):
	for tm in text:
		if ord(tm)<32 or ord(tm)>127:
			s.msg(t, u'ошибка в параметрах!')
			return
	text = text.upper()
	text = text.split(' ')

	link = 'http://weather.noaa.gov/weather/'+text[0]+'_cc.html'
	f = urllib.urlopen(link)
	wzz = f.read()
	f.close()

	if wzz.count('Not Found'): msg = u'я не знаю такой страны!'
	else:
		wzpos = wzz.find('<select name=\"cccc\">')
		wzz = wzz[wzpos:wzz.find('</select>',wzpos)]

		wzz = wzz.split('<OPTION VALUE=\"')
		msg = u'города по запросу: '
		not_add = 1
		for wzzz in wzz:
			if wzzz.lower().count(text[1].lower()):
				msg += '\n'+wzzz.replace('\">',' -')[:-1]
				not_add = 0
		if not_add: msg = u'такой город не найден!'
	s.msg(t, msg)


bot.register_cmd_handler(weather_city, u'.wzcity')
bot.register_cmd_handler(weather_raw, u'.wzz')
bot.register_cmd_handler(weather_short, u'.wzs')
bot.register_cmd_handler(weather, u'.wz')
