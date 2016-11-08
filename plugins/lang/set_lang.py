def set_lang_handler(bot, msg, cmd):
    param = msg['body'][len(cmd):]
    if param in bot.lang:
        if bot.isConference(msg['from'].bare):
            bot.room_settings[msg['from'].bare]['lang'] = param
        else:
            bot.reply('only_muc',msg,True)
    else:
        # TODO reply with syntax
        pass

bot.register_cmd_handler(set_lang_handler, '.set_lang', 11)