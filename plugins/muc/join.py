import slixmpp

def join_handler(bot, msg, cmd):
    param = msg['body'][len(cmd):].split()
    try:
        jid, nick = param[0].split('/')
    except ValueError:
        jid, nick = (param[0], bot.nick)
    except IndexError:
        return

    try:
        pwd = param[1]
    except IndexError:
        pwd = ''
    bot.add_event_handler("muc::%s::got_online" % jid,
                          bot.muc_online)
    if pwd:

        bot.plugin['xep_0045'].joinMUC(jid,
                                       nick,
                                       password=pwd,
                                       wait=True)
    else:
        bot.plugin['xep_0045'].joinMUC(jid,
                                       nick,
                                       wait=True)

    room = slixmpp.JID(jid).bare.lower()
    bot.room_settings[room]['access'] # mention key to automatically create it with empty value
    bot.room_settings[room]['autologin'] = 1
    bot.room_settings[room]['nick'] = nick
    if pwd:
        bot.room_settings[room]['pwd'] = pwd

bot.register_cmd_handler(join_handler, '.join', 50)
