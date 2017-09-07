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


bot.register_cmd_handler(leave_handler, 'leave', 50)
