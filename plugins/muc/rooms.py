def rooms_handler(bot, msg, cmd):
    for room in sorted(bot.room_settings):
        bot.reply(room, msg)

bot.register_cmd_handler(rooms_handler, '.rooms', 100)