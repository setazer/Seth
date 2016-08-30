#!/usr/bin/env python
# -*- coding: utf8 -*-
#~#######################################################################
#~ Copyright (c) 2010 Timur Timirkhanov <timur@timirkhanov.kz>               #
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

def m_parse(text):
 text = text.strip()
 if text.count('|'):
  n = text.find('|')
  return (text[:n], text[n+1:])
 else: return (text, '')

def invite_handler(t, s, p):
 if p:
  p, reason = m_parse(p)
  if not p.count('@'):
   s.lmsg(t, 'whom?')
  else:
   if reason=='': reason = u'Вас приглашает '+s.nick
   msg=domish.Element((None, 'message'))
   msg.addUniqueId()
   msg['to']=s.room.jid
   Invite=domish.Element((None, 'invite'))
   Invite['to']=p
   Invite.addElement('reason', content=reason)
   xchild=msg.addElement('x', 'http://jabber.org/protocol/muc#user')
   xchild.addChild(Invite)
   bot.wrapper.send(msg)
   s.msg(t, u'Призван')
 else: s.syntax(t, 'kick')

bot.register_cmd_handler(invite_handler, '.invite', 7, 1)