import time
def clean_handler(bot, msg, cmd):
    if bot.isConference(msg['from'].bare):
        param = msg['body'][len(cmd):]
        i_max = int(param) if (param and param.isdigit()) else 18
        msg['type']='groupchat'
        for i in range(i_max):
            bot.reply('',msg)
            time.sleep(1.7)
        bot.reply('Cleaned',msg)

bot.register_cmd_handler(clean_handler, '.clean', 7)
