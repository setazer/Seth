#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Imported from isida by quality(quality@botaq.net)
# Official conference - botaq@conference.jabber.ru
# Thanks to Disabler - http://isida.googlecode.com/


def calc_handler(bot, msg, cmd):
    param = msg['body'][len(cmd):]
    legal = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '*', '/', '+', '-', '(', ')', '=', '^', '!', ' ', '<',
             '>', '.']
    ppc = 1
    for tt in param:
        all_ok = 0
        for ll in legal:
            if tt == ll:
                all_ok = 1
                break
        if not all_ok:
            ppc = 0
            break
    if param.count('**'):
        ppc = 0

    if ppc:
        try:
            rep = str(eval(param))
        except SyntaxError:
            rep = 'Я не могу это посчитать'
    else:
        rep = 'Выражение недопустимо'
    bot.reply(rep, msg)

bot.register_cmd_handler(calc_handler, '.calc', 4)
