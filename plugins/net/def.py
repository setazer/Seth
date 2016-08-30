#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Imported from isida by quality(quality@botaq.net)
#Official conference - botaq@conference.jabber.ru
#Thanks to Disabler - http://isida.googlecode.com/


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

	
def defcode(t, s, text):
    if not text: msg = u'а номер?'
    else:
	dcnt = text[0]
	ddef = text[1:4]
	dnumber = text[4:]
	if text[:2] != '79': msg = u'поиск только по мобильным телефонам России!'
	else:
		link = 'http://www.mtt.ru/info/def/index.wbp?def='+ddef+'&number='+dnumber+'&region=&standard=&date=&operator='
		f = urllib.urlopen(link)
		msg = f.read()
		f.close()

		encidx = msg.find('charset=')
		if encidx >= 0:
			enc = msg[encidx+8:encidx+30]
			enc = enc[:enc.index('\">')]
			enc = enc.upper()
		else: enc = 'UTF-8'

		msg = unicode(msg, enc)

		mbeg = msg.find('<INPUT TYPE=\"submit\" CLASS=\"submit\"')
		msg = msg[mbeg:msg.find('</table>',mbeg)]
		msg = msg.split('<tr')
		
		if msg[0].count(u'не найдено'): msg = u'не найдено!'
		else:
			msg.remove(msg[0])
			mmsg = u'Найдено:\n'
			for mm in msg:
				tmm = mm
				tmm = replacer(tmm)
				tmm = tmm[tmm.find('>')+1:]
				tmm = tmm.replace('\n','\t')
				mmsg += tmm[1:-2] + '\n'
			msg = mmsg[:-1]
			
       	s.msg(t, msg)

		
bot.register_cmd_handler(defcode, u'.def')