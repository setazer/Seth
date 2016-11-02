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
    bot.room_settings[room] = {'access': {}, 'autologin': 1, 'nick': nick}
    if pwd:
        bot.room_settings[room]['pwd'] = pwd


def leave_handler(bot, msg, cmd):
    param = msg['body'][len(cmd):]
    if param:
        if param in bot.room_settings:
            bot.plugin['xep_0045'].leaveMUC(param, bot.room_settings[param]['nick'], msg='Leaving')
            bot.room_settings[param]['autologin'] = 0
            bot.del_event_handler("muc::%s::got_online" % param, bot.muc_online)
    elif bot.isConference(msg['from'].bare):
        room = msg['from'].bare
        bot.plugin['xep_0045'].leaveMUC(room, bot.room_settings[room]['nick'],  msg='Leaving')
        bot.room_settings[room]['autologin'] = 0
        bot.del_event_handler("muc::%s::got_online" % room, bot.muc_online)


def exec_handler(bot, msg, cmd):
    param = msg['body'][len(cmd):]
    if bot.isConference(msg['from'].bare):
        fromjid = slixmpp.JID(bot.plugin['xep_0045'].getJidProperty(msg['from'].bare, msg['from'].resource, 'jid')).bare
    else:
        fromjid = msg['from'].bare
    if fromjid in bot.config.ADMINS:
        try:
            exec(param.lstrip(), globals(), locals())
        except Exception as e:
            bot.reply(e.args[0], msg)
    else:
        bot.reply('ACCESS DENIED!', msg)


def exit_handler(bot, msg, cmd):
    for room in bot.room_settings:
        bot.plugin['xep_0045'].leaveMUC(room, bot.room_settings[room]['nick'], msg='Shutting down')
    bot.disconnect(wait=True)

bot.register_cmd_handler(exec_handler, '.exec', 50)
bot.register_cmd_handler(exit_handler, '.exit', 11)
bot.register_cmd_handler(join_handler, '.join', 50)
bot.register_cmd_handler(leave_handler, '.leave', 50)