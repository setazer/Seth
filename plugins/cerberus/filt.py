#!/usr/bin/env python
# -*- coding: utf8 -*-
#~#######################################################################
#~ Copyright (c) 2008 Burdakov Daniel <kreved@kreved.org>               #
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

from twisted.words.protocols.jabber import jid

filter_actions = ['ignore', 'warning', 'visitor', 'kick', 'ban']
filter_modes = ['presline', 'preslen', 'msglen', 'nicklen']

def filter_mode_handler(t, s, p):
 p = p.strip()
 try:
  mode, length, action = p.split(' ')
 except:
  s.msg(t, 'invalid options')
  return
 if not mode in filter_modes:
  s.msg(t, 'invalid mode')
  return
 if mode != 'presline':
  if not length.isdigit() or len(length)==1:
   s.msg(t, 'invalid length')
   return
 else:
  if not length.isdigit():
   s.msg(t, 'invalid length')
   return
 if action in filter_actions:
  prefix = 'filter_%s_' % (mode,)
  s.room.set_option(prefix+'length', length)
  s.room.set_option(prefix+'action', action)
  s.lmsg(t, 'ok')
 else:
  s.msg(t, 'invalid action')

def get_filter_mode(item, name):
 res = {}
 prefix = 'filter_%s_' % (name,)
 length = item.room.get_option(prefix+'length', '0')
 len = int(length)
 action = item.room.get_option(prefix+'action', config.CERBERUS_MODE)
 if item.room and item.room.bot:
  if (action == 'ban') and not(item.room.bot.can_ban(item)): action = 'kick'
  if (action == 'kick') and not(item.room.bot.can_kick(item)): action = 'visitor'
  if (action == 'visitor') and not(item.room.bot.can_visitor(item)): action = 'warning'
 res['len'] = len
 res['act'] = action
 return res

def filter_join_action(item):
 nick_params = get_filter_mode(item, 'nicklen')
 nicklen = nick_params['len']
 pres_params = get_filter_mode(item, 'preslen')
 statlen = pres_params['len']
 presline_params = get_filter_mode(item, 'presline')
 presline = presline_params['len']
 if nicklen > 0 and len(item.nick) > nicklen:
  reason = u'Your nick is over %d symbols' % (nicklen, )
  action = nick_params['act']
  if action == 'ban': item.room.moderate('nick', item.nick, 'affiliation', 'outcast', reason)
  elif action == 'kick': item.room.moderate('nick', item.nick, 'role', 'none', reason)
  elif action == 'visitor': item.room.moderate('nick', item.nick, 'role', 'visitor', reason)
  elif action == 'warning': item.msg('groupchat', reason)
  elif action <> 'ignore': bot.log.err(escape('unknown filter_reason in %s: %s' % (item.room.jid, action)))
 if statlen > 0 and len(item.status) > statlen:
  reason = u'Your status is over %d symbols' % (statlen)
  action = pres_params['act']
  if action == 'ban': item.room.moderate('nick', item.nick, 'affiliation', 'outcast', reason)
  elif action == 'kick': item.room.moderate('nick', item.nick, 'role', 'none', reason)
  elif action == 'visitor': item.room.moderate('nick', item.nick, 'role', 'visitor', reason)
  elif action == 'warning': item.msg('groupchat', reason)
  elif action <> 'ignore': bot.log.err(escape('unknown filter_reason in %s: %s' % (item.room.jid, action)))
 if presline > 0 and item.status.count('\n') > presline:
  reason = u'Your status has over %d newlines' % (presline)
  action = presline_params['act']
  if action == 'ban': item.room.moderate('nick', item.nick, 'affiliation', 'outcast', reason)
  elif action == 'kick': item.room.moderate('nick', item.nick, 'role', 'none', reason)
  elif action == 'visitor': item.room.moderate('nick', item.nick, 'role', 'visitor', reason)
  elif action == 'warning': item.msg('groupchat', reason)
  elif action <> 'ignore': bot.log.err(escape('unknown filter_reason in %s: %s' % (item.room.jid, action)))

def filter_msg_action(source, text, delayed):
 if not delayed:
  j = jid.JID(source)
  r = j.userhost()
  nick = j.resource
  if r in bot.g:
   room = bot.g[r]
   msglen = int(room.get_option('filter_msglen_length', '0'))
   if msglen > 0 and len(text) > msglen:
    reason = u'Your message is over %d symbols' % (msglen, )
    action = room.get_option('filter_msglen_action', config.CERBERUS_MODE)
    if action == 'ban': room.moderate('nick', nick, 'affiliation', 'outcast', reason)
    elif action == 'kick': room.moderate('nick', nick, 'role', 'none', reason)
    elif action == 'visitor': room.moderate('nick', nick, 'role', 'visitor', reason)
    elif action == 'warning': source.msg('groupchat', reason)
    elif action <> 'ignore': bot.log.err(escape('unknown filter_reason in %s: %s' % (room.jid, action)))

bot.register_cmd_handler(filter_mode_handler, '.filter', 9, g=1)
bot.register_join_handler(filter_join_action)
bot.register_msg_handler(filter_msg_action)
