def echo_handler(bot, msg, cmd):
    param = msg['body'][len(cmd):]
    if msg['type'] == 'groupchat':
        bot.reply(msg['mucnick'] + ': ' + param.lstrip(), msg)
    else:
        bot.reply(param.lstrip(), msg)

def say_handler(bot, msg, cmd):
    param = msg['body'][len(cmd):]
    msg['type']='groupchat'
    bot.reply(param.lstrip(), msg)


bot.register_cmd_handler(echo_handler, 'echo', 3)
bot.register_cmd_handler(say_handler, 'say', 4)
