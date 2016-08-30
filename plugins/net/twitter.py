#!/usr/bin/env python
# -*- coding: utf8 -*-
#~#######################################################################
#~ Copyright (c) 2012 Timur Timirkhanov                                 #
#~                                                                      #
#~ This file is part of FreQ-bot.                                       #
#~                                                                      #
#~ FreQ-bot is free software: you can redistribute it and/or modify     #
#~ it under the terms of the GNU General Public License as published by #
#~ the Free Software Foundation, either version 3 of the License, or    #
#~ (at your option) any later version.                                  #
#~                                                                      #
#~ FreQ-bot is distributed in the hope that it will be useful,          #
#~ but WITHOUT ANY WARRANTY; without even the implied warranty of       #
#~ MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the        #
#~ GNU General Public License for more details.                         #
#~                                                                      #
#~ You should have received a copy of the GNU General Public License    #
#~ along with FreQ-bot.  If not, see <http://www.gnu.org/licenses/>.    #
#~#######################################################################

def twitter_handler(t, s, p):
 if not p: s.syntax(t, 'twitter')
 else:
    p = p.strip()
    p = p.replace('@', '')
    inl = p.split(' ')
    if len(inl) > 1 and inl[1].isdigit():
        count = inl[1]
    else:
        count = '10'
    result=''
    try:
        data=json.load(urllib.urlopen('https://api.twitter.com/1.1/statuses/user_timeline.json?include_rts=true&trim_user=true&screen_name=%s&count=%s'%(inl[0], count)))
        if not data:
            result=u'Закрытый Twitter'
        elif type(data) is list:
            for d in data:
                result+=d['text']+'\n'
        else:
            result=u'Ошибка Twitter'
            if data['error']:
                result +=' '+data['error']
    except:
        result=u'Ошибка соединения'
    s.msg(t, result)

def twitter_search_handler(t, s, p):
 if not p: s.syntax(t, 'twitter_search')
 else:
    p = p.strip()
    result=''
    try:
        data=json.load(urllib.urlopen('http://search.twitter.com/search.json?q=%s'%(urllib.quote(p), )))
        if not data:
            result=u'Закрытый Twitter'
        elif type(data['results']) is list:
            for d in data['results']:
                result+=d['from_user_name']+' :'+d['text']+'\n'
        else:
            result=u'Ошибка Twitter'
            if data['error']:
                result +=' '+data['error']
    except:
        result=u'Ошибка соединения'
    s.msg(t, result)

bot.register_cmd_handler(twitter_handler, '.twitter')
bot.register_cmd_handler(twitter_search_handler, '.twitter_search')