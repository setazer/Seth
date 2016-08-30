#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Imported from isida by quality(quality@botaq.net)
#Official conference - botaq@conference.jabber.ru
#Thanks to Disabler and dr.Schmurge - http://isida.googlecode.com/ 


def replacer(msg):
	msg = rss_replace(msg)
	msg = rss_del_html(msg)
	msg = rss_replace(msg)
	msg = rss_del_nn(msg)
	return msg

	
def rss_del_nn(ms):
	while ms.count('  '):
		ms = ms.replace('  ',' ')
	ms = ms.replace('\r','')
	ms = ms.replace('\t','')
	ms = ms.replace('\n \n','\n')
	while ms.count('\n\n'):
		ms = ms.replace('\n\n','\n')
	ms += '\n'
	return ms

	
def rss_del_html(ms):
	i=0
	lms = len(ms)
	while i < lms:
		if ms[i] == '<':
			for j in range(i, lms):
				if ms[j] == '>':
					break
			ms = ms[:i] + ms[j+1:]
			lms = len(ms)
			i -= 1
		i += 1
	return ms

	
def rss_replace(ms):
	ms = ms.replace('<br>','\n')
	ms = ms.replace('<br />','\n')
	ms = ms.replace('<br/>','\n')
	ms = ms.replace('\n\r','\n')
	ms = ms.replace('<![CDATA[','')
	ms = ms.replace(']]>','')
	ms = ms.replace('&lt;','<')
	ms = ms.replace('&gt;','>')
	ms = ms.replace('&quot;','\"')
	ms = ms.replace('&apos;','\'')
	ms = ms.replace('&amp;','&')
	ms = ms.replace('&middot;',u'В·')
	ms = ms.replace('&nbsp;','')
	ms = ms.replace('&raquo;',u'в–ј')
	ms = ms.replace('&copy;',u'В©')
	mm = ''
	m = 0
	while m<len(ms):
		try:
			if ms[m:m+2] == u'&#':
				if ms[2].lower() == 'x':
					tnum = ms[m+3:ms.find(';',m+3)]
				else:
					tnum = ms[m+2:ms.find(';',m+2)]
				num = isNumber(tnum[:5])
				if num != 'None':
					mm += unicode(num)
					m += 3 + len(tnum)
				else:
					mm += ms[m]
			else:
				mm += ms[m]
		except:
			mm += ms[m]
		m += 1
# &#x2212;
	return mm


def html_encode(body):
	encidx = body.find('encoding=')
	if encidx >= 0:
		enc = body[encidx+10:encidx+30]
		enc = enc[:enc.find('?>')-1]
	else:
		encidx = body.find('charset=')
		if encidx >= 0:
			enc = body[encidx+8:encidx+30]
			enc = enc[:enc.find('"')]
		else:
			enc = chardet.detect(body)['encoding']

	if body == None:
		body = ''
	if enc == None or enc == '':
		enc = 'utf-8'
	return unicode(body,enc)
	

def telcode(t, s, text):
	if len(text):
		query = urllib.urlencode({'text' : text.encode("windows-1251")})
		url = u'http://www.telcode.ru/mob/select.asp?%s'.encode("utf-8") % (query)
		f = urllib.urlopen(url)
		body = f.read()
		f.close()
		body = html_encode(body)
		if body.count(u'не найдено записей'): msg = u'не найдено!'
		else:
			msg = rss_del_html(get_tag(body,'h3'))+' ... '
			city = body.replace('\n','').replace('\r','').split('</h3>')[1].split('<br> <br>')[0].split('<br>')
			for tmp in city: msg += get_tag(tmp,'a')+', '
			msg = msg[:-2]
	else: msg = u'чего искать будем?'
	s.msg(t, msg)

	
def tcode(t, s, text):
	if len(text):
		try: csize = int(text.split('\n')[1])
		except: csize = 3
		if csize < 1: csize = 1
		elif csize > 25: csize = 25
		text = text.split('\n')[0]
		try: url = u'http://www.btk-online.ru/phcode/?srchCId=1&srchTName=&srchCCode=&srchTCode='+str(int(text))
		except: url = u'http://www.btk-online.ru/phcode/?srchCId=1&%s'.encode("utf-8") % (urllib.urlencode({'srchTName': text.encode("windows-1251")}))
		user_agent='Mozilla/5.0 (X11; U; Linux x86_64; ru; rv:1.9.0.4) Gecko/2008120916 Gentoo Firefox/3.0.4'
		req = urllib2.Request(url)
		req.add_header('User-Agent',user_agent)
		body = urllib2.urlopen(req).read()
		body = html_encode(body)
		if body.count('<table id=pcodephones cellspacing=0>\n  <tr><th width'): msg = u'По вашему запросу ничего не найдено.'
		else:
			body = body.split('<table id=pcodephones cellspacing=0>')[1].split('</table>')[0].split('</tr>')[1:]
			if body != [u'\n ']:
				msg = u'Найдено:'
				for tmp in body[:csize]:
					tmp2 = '\n'+replacer(tmp).replace('\n',', ').replace(';',', ')
					tmp3 = tmp2[tmp2.find(u' тариф'):tmp2.find(u',',tmp2.find(u' тариф'))+1]
					msg += tmp2.replace(tmp3,'')
			else: msg = u'по вашему запросу ничего не найдено.'
	else: msg = u'чего искать будем?'
	s.msg(t, msg)
	
	
bot.register_cmd_handler(telcode, u'.telcode')