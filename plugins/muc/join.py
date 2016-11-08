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

    # The groupchat_presence event is triggered whenever a
    # presence stanza is received from any chat room, including
    # any presences you send yourself. To limit event handling
    # to a single room, use the events muc::room@server::presence,
    # muc::room@server::got_online, or muc::room@server::got_offline.

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
    bot.room_settings[room]['lang'] = bot.default_lang
    if pwd:
        bot.room_settings[room]['pwd'] = pwd

bot.register_cmd_handler(join_handler, '.join', 50)
