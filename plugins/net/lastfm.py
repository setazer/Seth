#!/usr/bin/env python
# -*- coding: utf-8 -*-
#~#######################################################################
#~ Copyright (c) 2010 Timur Timirkahnov                                 #
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
import pylast
lastfm_key = config.LASTFM

def reduce_spaces(text):
 while text.count('  '): text = text.replace('  ',' ')
 return text

def handle_toptracks(t, s, p):
 if not p: s.syntax(t, 'toptracks')
 else:
  p = reduce_spaces(p.strip())
  arr = p.split(' ')
  user = arr[0]
  number = int(arr[1]) if (len(arr)>=2 and arr[1].isdigit()) else 10
  try:
   api = pylast.get_lastfm_network(lastfm_key)
   seq = api.get_user(user).get_top_tracks()
   if seq:
    if len(seq) < number: number = len(seq)
    mesg = u'Любимые треки пользователя %s:\n' % (user)
    for item in seq[:number]:
     mesg +=u'%s - %s [прослушан %s раз(а)]\n' % (item[0].get_artist().get_name(), item[0].get_name(), item[1])
   else:
    mesg = u'У пользователя %s нет любимых треков.' % (user)
  except:
   mesg = u'Невозможно получить доступ к данным.'
  s.msg(t, mesg)

def handle_topartists(t, s, p):
 if not p: s.syntax(t, 'topartists')
 else:
  p = reduce_spaces(p.strip())
  arr = p.split(' ')
  user = arr[0]
  number = int(arr[1]) if (len(arr)>=2 and arr[1].isdigit()) else 10
  try:
   api = pylast.get_lastfm_network(lastfm_key)
   seq = api.get_user(user).get_top_artists()
   if seq:
    if len(seq) < number: number = len(seq)
    mesg = u'Любимые певцы пользователя %s:\n' % (user)
    for item in seq[:number]:
     mesg +=u'%s (%s)\n' % (item[0].get_name(), item[1])
   else:
    mesg = u'У пользователя %s нет любимых певцов.' % (user)
  except:
   mesg = u'Невозможно получить доступ к данным.'
  s.msg(t, mesg)

def handle_topalbums(t, s, p):
 if not p: s.syntax(t, 'topalbums')
 else:
  p = reduce_spaces(p.strip())
  arr = p.split(' ')
  user = arr[0]
  number = int(arr[1]) if (len(arr)>=2 and arr[1].isdigit()) else 10
  try:
   api = pylast.get_lastfm_network(lastfm_key)
   seq = api.get_user(user).get_top_albums()
   if seq:
    if len(seq) < number: number = len(seq)
    mesg = u'Любимые альбомы пользователя %s:\n' % (user)
    for item in seq[:number]:
     mesg +=u'%s (%s)\n' % (item[0].get_name(), item[1])
   else:
    mesg = u'У пользователя %s нет любимых альбомов.' % (user)
  except:
   mesg = u'Невозможно получить доступ к данным.'
  s.msg(t, mesg)

def handle_lasttracks(t, s, p):
 if not p: s.syntax(t, 'lasttracks')
 else:
  p = reduce_spaces(p.strip())
  arr = p.split(' ')
  user = arr[0]
  number = int(arr[1]) if (len(arr)>=2 and arr[1].isdigit()) else 10
  try:
   api = pylast.get_lastfm_network(lastfm_key)
   seq = api.get_user(user).get_recent_tracks()
   if seq:
    if len(seq) < number: number = len(seq)
    mesg = u'Последние треки пользователя %s:\n' % (user)
    for item in seq[:number]:
     mesg +='%s - %s (%s)\n' % (item[0].get_artist().get_name(), item[0].get_name(), item[1])
   else:
    mesg = u'Пользователь %s в последнее время ничего не слушал.' % (user)
  except:
   mesg = u'Невозможно получить доступ к данным.'
  s.msg(t, mesg)

def handle_lastloved(t, s, p):
 if not p: s.syntax(t, 'lastloved')
 else:
  p = reduce_spaces(p.strip())
  arr = p.split(' ')
  user = arr[0]
  number = int(arr[1]) if (len(arr)>=2 and arr[1].isdigit()) else 10
  try:
   api = pylast.get_lastfm_network(lastfm_key)
   seq = api.get_user(user).get_loved_tracks()
   if seq:
    if len(seq) < number: number = len(seq)
    mesg = u'Любимые треки пользователя %s:\n' % (user)
    for item in seq[:number]:
     mesg +=u'%s (%s)\n' % (item[0].get_name(), item[1])
   else:
    mesg = u'У пользователя %s нет любимых треков.' % (user)
  except:
   mesg = u'Невозможно получить доступ к данным.'
  s.msg(t, mesg)
  
def handle_last(t, s, p):
 if not p: s.syntax(t, 'last')
 else:
  p = p.strip()
  try:
   api = pylast.get_lastfm_network(lastfm_key)
   seq = api.get_user(p).get_recent_tracks(limit=1)
   mesg = u'Последний трек пользователя %s:\n' % (p)
   for item in seq:
    mesg +='%s - %s (%s)\n' % (item[0].get_artist().get_name(), item[0].get_name(), item[1])
  except:
   mesg = u'Невозможно получить доступ к данным.'
  s.msg(t, mesg)

def handle_now(t, s, p):
 if not p: s.syntax(t, 'now')
 else:
  p = p.strip()
  try:
   api = pylast.get_lastfm_network(lastfm_key)
   seq = api.get_user(p).get_now_playing()
   if seq:
    mesg = u'Пользователь %s сейчас слушает ' % (p) 
    mesg += '%s - %s' % (seq.get_artist().get_name(), seq.get_name())
   else:
    mesg = u'Пользователь %s сейчас ничего не слушает.' % (p)
  except:
   mesg = u'Невозможно получить доступ к данным.'
  s.msg(t, mesg)

def handle_lastfriends(t, s, p):
 if not p: s.syntax(t, 'lastfriends')
 else:
  p = reduce_spaces(p.strip())
  arr = p.split(' ')
  user = arr[0]
  number = int(arr[1]) if (len(arr)>=2 and arr[1].isdigit()) else 10
  try:
   api = pylast.get_lastfm_network(lastfm_key)
   if number > 10: number=10
   seq = api.get_user(user).get_friends(limit=number)
   if seq:
    mesg = u'Друзья пользователя %s:\n' % (user)
    mesg += ', '.join(item for item in seq)
   else:
    mesg = u'У пользователя %s нет друзей.' % (user)
  except:
   mesg = u'Невозможно получить доступ к данным.'
  s.msg(t, mesg)

def handle_lastneighbours(t, s, p):
 if not p: s.syntax(t, 'lastneighbours')
 else:
  p = reduce_spaces(p.strip())
  arr = p.split(' ')
  user = arr[0]
  number = int(arr[1]) if (len(arr)>=2 and arr[1].isdigit()) else 10
  try:
   api = pylast.get_lastfm_network(lastfm_key)
   if number > 10: number=10
   seq = api.get_user(user).get_neighbours(limit=number)
   if seq:
    mesg = u'Соседи пользователя %s:\n' % (user)
    mesg += ', '.join(item for item in seq)
   else:
    mesg = u'Пользователь %s живет в пустыне.' % (user)
  except:
   mesg = u'Невозможно получить доступ к данным.'
  s.msg(t, mesg)

def handle_taste(t, s, p):
 if not p: s.syntax(t, 'taste')
 else:
  p = reduce_spaces(p.lower().encode('utf-8').replace('\\x','%')).split(' ',1)
  try:
   (user1, user2) = p
  except:
   s.msg(t, u'Необходимо два пользователя')
   return
  try:
   api = pylast.get_lastfm_network(lastfm_key)
   seq = api.get_user(user1).compare_with_user(user2)
   percent = float(seq[0])
   mesg = u'Cовместимость %s и %s равна %1.2f%%. Их объединяет любовь к: ' % (user1, user2, percent*100.0)
   list = seq[1]
   mesg += ', '.join(item.get_name() for item in list)
  except:
   mesg = u'Невозможно получить доступ к данным.'
  s.msg(t, mesg)

bot.register_cmd_handler(handle_toptracks, u'.toptracks')
bot.register_cmd_handler(handle_topartists, u'.topartists')
bot.register_cmd_handler(handle_topalbums, u'.topalbums')
bot.register_cmd_handler(handle_lasttracks, u'.lasttracks')
bot.register_cmd_handler(handle_last, u'.last')
bot.register_cmd_handler(handle_now, u'.now')
bot.register_cmd_handler(handle_lastfriends, u'.lastfriends')
bot.register_cmd_handler(handle_lastneighbours, u'.lastneighbours')
bot.register_cmd_handler(handle_lastloved, u'.lastloved')
bot.register_cmd_handler(handle_taste, u'.taste')