#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Imported from isida by quality(quality@botaq.net)
# Official conference - botaq@conference.jabber.ru
# Thanks to Disabler - http://isida.googlecode.com/


def true_handler(bot, msg, cmd):
    param = msg['body'][len(cmd):]
    if not param:
        bot.reply('чо чо?',msg)
    else:
        idx = 0
        for tmp in param: idx += ord(tmp)
        idx = int((idx / 100.0 - int(idx / 100)) * 100)
        rep = 'Ваше утверждение верно с вероятностью ' + str(idx) + '%'
    bot.reply(rep, msg)

bot.register_cmd_handler(true_handler, '.true', 3)
