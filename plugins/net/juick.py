#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Imported from isida by quality(quality@botaq.net)
#Official conference - botaq@conference.jabber.ru
#Thanks to Disabler - http://isida.googlecode.com/


def get_subtag(body,tag):
	beg = body.find('\"',body.find(tag))+1
	return body[beg:body.find('\"',beg)]

	
def get_tag(body,tag):
	return body[body.find('>',body.find('<'+tag))+1:body.find('</'+tag+'>')]
	
	
def juick_user_info(t, s, text):
	if len(text):
		try: mlen = int(text.split(' ')[1])
		except: mlen = 3
		try: mlim = int(text.split(' ')[2])
		except: mlim = 50
		text = text.split(' ')[0]
		link = 'http://juick.com/'+text.encode('utf-8').replace('\\x','%').replace(' ','%20')+'/friends'
		body = urllib.urlopen(link).read()
		body = rss_replace(html_encode(body))

		if body.count('<h1>Page Not Found</h1>'): msg = u'пользователь '+text+u' не найден'
		else:
			link = 'http://juick.com/'+text.encode('utf-8').replace('\\x','%').replace(' ','%20')+'/readers'
			rbody = urllib.urlopen(link).read()
			rbody = rss_replace(html_encode(rbody))
			link = 'http://juick.com/'+text.encode('utf-8').replace('\\x','%').replace(' ','%20')+'/tags'
			tbody = urllib.urlopen(link).read()
			tbody = rss_replace(html_encode(tbody))
			msg = get_tag(body,'h1')+' - http://juick.com'+get_subtag(body.split('pagetabs')[1].split('</li>')[0],'href')
			tb = body.split('<div id="content">')[1].split('</p>')[0]
			try:
				if len(tb)>=20 and tb.count('I read'):
					msg += '\n'+get_tag(tb,'h2')+' - '
					for tmp in tb.split('<p>')[1].split('<a href="')[1:]: msg += tmp[tmp.find('>')+1:tmp.find('<',tmp.find('>'))]+', '
					msg = msg[:-2]
				else: msg += '\nNo readers'
			except: msg += '\nNo readers'

			if not rbody.count('<title>404 Not Found</title>'):
				try:
					tb = rbody.split('<div id="content">')[1].split('</div>')[0]
					if len(tb)>=20 and tb.count('My read'):
						msg += '\n'+get_tag(tb,'h2')+' - '
						for tmp in tb.split('<p>')[1].split('<a href="')[1:]: msg += tmp[tmp.find('>')+1:tmp.find('<',tmp.find('>'))]+', '
						msg = msg[:-2]
					else: msg += '\nNo readers'
				except: msg += '\nNo readers'

			if not tbody.count('<title>404 Not Found</title>'):
				try:
					tb = tbody.split('<div id="content">')[1].split('</div>')[0]
					msg += u'\nTags: '
					for ttb in tb.split('<span')[1:]: msg += get_tag(ttb,'a')+', '
					msg = msg[:-2]
				except: msg += '\nNo tags'
	else: msg = u'кто нужен то?'
	s.msg(t, msg)
	
	
bot.register_cmd_handler(juick_user_info, u'.juick_user_info')


def juick_user(t, s, text):
	if len(text):
		try: mlen = int(text.split(' ')[1])
		except: mlen = 3
		try: mlim = int(text.split(' ')[2])
		except: mlim = 50
		text = text.split(' ')[0]
		link = 'http://juick.com/'+text.encode('utf-8').replace('\\x','%').replace(' ','%20')
		body = urllib.urlopen(link).read()
		body = rss_replace(html_encode(body))
		if body.count('<title>404 Not Found</title>'):
			msg = u'пользователь '+text+u' не найден'
		else:
			msg = get_tag(body,'h1')+' - http://juick.com'+get_subtag(body.split('pagetabs')[1].split('</li>')[0],'href')
			mes = body.split('<li id="')
			mesg = ''
			for us in mes[1:mlen+1]:
				mesg += '\n'+get_tag(us.split('<small>')[1],'a')+' - '
				mm = rss_del_html(get_tag(us,'div'))
				if len(mm)<mlim: mesg += mm
				else: mesg += mm[:mlim]+'[...]'
				if us.split('</span>')[1].count('<a'): mesg += ' ('+get_tag(us,'span')+'|'+get_tag(us.split('</span>')[1],'a')+')'
				else: mesg += ' ('+get_tag(us,'span')+'|No replies)'
			msg += mesg
	else: msg = u'кто нужен то?'
	s.msg(t, msg)
	
	
bot.register_cmd_handler(juick_user, u'.juick_user')


def juick_msg(t, s, text):
	if len(text):
		try:
			text = text.replace('#','')
			if text.count('/'):
				link = 'http://juick.com/'+text.split('/')[0]
				post = int(text.split('/')[1])
			else: 
				post = 0
				link = 'http://juick.com/'+text.split(' ')[0]
			try: repl_limit = int(text.split(' ')[1])
			except: repl_limit = 3
			body = urllib.urlopen(link).read()
			body = rss_replace(html_encode(body.replace('<div><a href','<div><a ')))
			if body.count('<title>404 Not Found</title>'):
				msg = u'пост #'+text+u' не найден'
			else:
				nname = get_tag(body,'h1')
				if nname.count('(') and nname.count(')'): uname = nname[nname.find('(')+1:nname.find(')')]
				else: uname = nname
				msg = 'http://juick.com/'+uname+'/'+text.split(' ')[0]+'\n'+nname+' - '+get_tag(body.split('<p>')[1],'div')
			repl = get_tag(body.split('<p>')[1],'h2')
			if repl.lower().count('('):
				hm_repl = int(repl[repl.find('(')+1:repl.find(')')])
				msg += u' (Ответов: '+str(hm_repl)+')'
			else:
				hm_repl = 0
				msg += u' (Нет ответов)'
			frm = get_tag(body.split('<p>')[1],'small')
			msg += frm[frm.find(' '):]
			cnt = 1
			if hm_repl:
				if not post:
					for rp in body.split('<li id="')[1:repl_limit+1]:
						msg += '\n'+text.split(' ')[0]+'/'+str(cnt)+' '+get_tag(rp.split('by')[1],'a')+': '+get_tag(rp,'div')
						cnt += 1
				else:
					msg += '\n'+text+' '+get_tag(body.split('<li id="')[post],'div')
			msg = rss_del_html(msg.replace('<a href="http','<a>http').replace('" rel',' <'))
		except:
			msg = u'неверный номер поста'
	else: msg = u'какой пост найти?'
	s.msg(t, msg)
	
	
bot.register_cmd_handler(juick_msg, u'.juick_msg')


def juick_tag_user(t, s, text):
	if len(text):
		try: mlen = int(text.split(' ')[1])
		except: mlen = 5
		text = text.split(' ')[0]
		if mlen > 20: mlen = 20
		link = 'http://juick.com/last?tag='+text.encode('utf-8').replace('\\x','%').replace(' ','%20')
		body = urllib.urlopen(link).read()
		body = rss_replace(html_encode(body))
		if body.count('<p>Tag not found</p>') or body.count('<h1>Page Not Found</h1>'):
			msg = u'тег '+text+u' не найден'
		else:
			usr = body.split('<h2>Users</h2>')[1].split('<h2>Messages</h2>')[0].split('<a href')
			users = ''
			for us in usr[1:mlen+1]:
				uus = us[us.find('>')+1:us.find('<',us.find('>'))]
				users += '\n'+ uus + ' - http://juick.com/'+uus[1:]
			msg = u'тег '+text+u' найден у '+users
	else: msg = u'какой тег найти?'
	s.msg(t, msg)
	
	
bot.register_cmd_handler(juick_tag_user, u'.juick_tag_user')


def juick_tag_msg(t, s, text):
	if len(text):
		try: mlen = int(text.split(' ')[1])
		except: mlen = 3
		try: mlim = int(text.split(' ')[2])
		except: mlim = 120
		text = text.split(' ')[0]
		link = 'http://juick.com/last?tag='+text.encode('utf-8').replace('\\x','%').replace(' ','%20')
		body = urllib.urlopen(link).read()
		body = rss_replace(html_encode(body))
		if body.count('<p>Tag not found</p>') or body.count('<h1>Page Not Found</h1>'):
			msg = u'тег '+text+u' не найден'
		else:
			mes = body.split('<h2>Messages</h2>')[1].split('</div><div id="lcol"><h2>')[0].split('<li class="liav"')
			mesg = ''
			for us in mes[1:mlen+1]:
				mesg += '\nhttp://juick.com/'+get_tag(us.split('<big>')[1],'a')[1:]+'/'+get_tag(us.split('</div>')[1],'a')[1:]+' - '
				mm = rss_del_html(get_tag(us,'div'))
				if len(mm)<mlim: mesg += mm
				else: mesg += mm[:mlim]+'[...]'
				if us.split('</span>')[1].count('<a'): mesg += ' ('+get_tag(us,'span')+'|'+get_tag(us.split('</span>')[1],'a')+')'
				else: mesg += ' ('+get_tag(us,'span')+'|No replies)'
			msg = u'тег '+text+u' найден в сообщениях:'+mesg
	else: msg = u'какой тег найти?'
	s.msg(t, msg)
	
	
bot.register_cmd_handler(juick_tag_msg, u'.juick_tag_msg')	
