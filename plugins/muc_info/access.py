#!/usr/bin/env python
# -*- coding: utf8 -*-
#~#######################################################################
#~ Copyright (c) 2011 Timur Timirkhanov                                 #
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
def access_handler(t, item, params):
 if params:
  try:
   q = item.room[params]
  except:
   item.lmsg(t, 'nick_not_found')
   return
 else:
  q = item
 item.lmsg(t, 'muc_access', q.affiliation, q.role, q.show, q.status, time.strftime("%d.%m.%y %H:%M:%S", time.localtime(q.joined)), q.access())

bot.register_cmd_handler(access_handler, ".access", g=1)