#!/usr/bin/env python
# -*- coding: utf-8 -*-
# автор - quality(quality@botaq.net)
# оф.сайт - http://quality.wen.ru/ & http://www.botaq.net/


import config


def bug(t, s, text):

    jid = s.realjid
    nick = s.nick
    room = s.room.jid
    time_sent = time.strftime("%H:%M",time.localtime (time.time()))

    if text:
        if len(text)>5:
            body = u'много букоф'
            return
        mmsg = u'сообщение из '+room+u' от '+nick+u'['+jid+u'] в '+time_sent+':\n '+text
        for jid_admins in config.ADMINS:
            bot.muc.msg('chat', jid_admins, mmsg)
            body = u'отправил всем админам'
    else:
        body = u'а шо писать админу то?'
    
    s.msg(t, body)

		
bot.register_cmd_handler(bug, u'.bug', 7)
