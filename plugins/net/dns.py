#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Imported from talisman by quality(quality@botaq.net)
#Official conference - botaq@conference.jabber.ru
#Thanks to Als - http://svn.xmpp.ru/repos/talisman/trunk


import socket


def dns_query(query):
	try:
		int(query[-1])
	except ValueError:
		try:
			(hostname, aliaslist, ipaddrlist) = socket.gethostbyname_ex(query)
			return u', '.join(ipaddrlist)
		except socket.gaierror:
			return u'не нахожу что-то'
	else:
		try:
			(hostname, aliaslist, ipaddrlist) = socket.gethostbyaddr(query)
		except socket.herror:
			return u'не нахожу что-то'
		return hostname + ' ' + string.join(aliaslist) + ' ' + string.join(aliaslist)

		
def dns(t, s, p):
	if p.strip():
		result = dns_query(p)
		s.msg(t, result)
	else:
		s.msg(t, u'что это было?')

		
bot.register_cmd_handler(dns, u'.dns')