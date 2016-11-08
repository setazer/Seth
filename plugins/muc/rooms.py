def rooms_handler(bot, msg, cmd):
    if bot.isConference(msg['from'].bare):
        bot.reply('look_private',msg,True)
        msg['type'] = 'chat'
        bot.reply('\n'.join(sorted(bot.room_settings)),msg)

bot.register_cmd_handler(rooms_handler, '.rooms', 100)