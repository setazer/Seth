import slixmpp

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
        bot.reply('access_denied', msg, True)


def exit_handler(bot, msg, cmd):
    for room in bot.room_settings:
        bot.plugin['xep_0045'].leaveMUC(room, bot.room_settings[room]['nick'], msg='Shutting down')
    bot.disconnect(wait=True)

bot.register_cmd_handler(exec_handler, '.exec', 50)
bot.register_cmd_handler(exit_handler, '.exit', 50)