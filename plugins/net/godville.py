#-*- coding: utf-8 -*-
import json
import urllib2

def handler_godville_hero(t, s, p):
 if not p:
  s.msg(t, u'ииии?')
  return
 hero = urllib2.quote(p.encode('utf-8'))
 url = 'http://godville.net/gods/api/%s.json' % (hero,)
 try:
  req=urllib2.Request(url)
  res=urllib2.urlopen(req)
  data=res.read()
  res.close()
 except urllib2.HTTPError, e:
  if e.code==404:
   s.msg(t, u'кто это?')
   return
  else:
   s.msg(t, str(e))
   return
 results = json.loads(data)
 hero_info = {}

 #Basic data start
 if 'name' in results: hero_info['hname'] = results['name']
 if 'expired' in results: hero_info['hexpired'] = u'Данные устарели.'
 else: hero_info['hexpired'] = u''
 if 'gender' in results:
  hero_info['hgender'] = u'й' if results['gender'] == 'male' else u'иня'
  hero_info['gend1'] = u'ийся' if results['gender'] == 'male' else u'аяся'
  hero_info['ggender'] = u'а' if results['gender'] == 'male' else u'ини'
  hero_info['gend2'] = u'ый' if results['gender'] == 'male' else u'ая'
  hero_info['gend3'] = u'' if results['gender'] == 'male' else u'ла'
  hero_info['gend4'] = u'' if results['gender'] == 'male' else u'а'
  hero_info['gend5'] = u'ел' if results['gender'] == 'male' else u'ла'
 else:
  hero_info['hgender'] = u'й'
  hero_info['gend1'] = u'ийся'
  hero_info['ggender'] = u'а'
  hero_info['gend2'] = u'ый'
  hero_info['gend3'] = u''
  hero_info['gend4'] = u''
  hero_info['gend5'] = u'ел'
 if 'godname' in results: hero_info['gname'] = results['godname']
 if 'alignment' in results: hero_info['halign'] = results['alignment']
 else: hero_info['halign'] = u'неизвестный'
 if 'pet' in results:
  hero_info['pinfo'] = u'Питомец породы %s %d-го уровня по кличке %s.' % (results['pet']['pet_class'], int(results['pet']['pet_level']), results['pet']['pet_name'])
 else: hero_info['pinfo'] = u'Питомца нет.'
 if 'clan' in results:
  hero_info['guild'] = u'Состоит в гильдии "%s"' % results['clan']
  if 'clan_position' in results: hero_info['guild'] += u' в звании "%s"' % results['clan_position']
 else:
  hero_info['guild']=u'Не состоит в гильдиях'
 if 'motto' in results: hero_info['motto'] = results['motto']
 if 'level' in results: hero_info['level'] = int(results['level'])
 if 'quest' in results: hero_info['qname'] = results['quest']
 if 'bricks_cnt' in results: hero_info['brick'] = int(results['bricks_cnt'])
 if 'gold_approx' in results: hero_info['gold'] = results['gold_approx']
 if 'temple_completed_at' in results:
  if results['temple_completed_at']: hero_info['temple'] = u''
  else: hero_info['temple'] = u' не'
 else: hero_info['temple'] = u' не'
 #Basic data end

 #Operative data start
 if 'godpower' in results: hero_info['prana'] = u', заряженн%s на %d%% праны' % (hero_info['gend2'], int(results['godpower']))
 else: hero_info['prana'] = u''

 if 'inventory_num' in results and 'inventory_max_num' in results: hero_info['inv'] = u'Также припас%s себе %d вещичек (из %d max)' % (hero_info['gend3'], int(results['inventory_num']), int(results['inventory_max_num']))
 else: hero_info['inv'] = u''

 if 'exp_progress' in results: hero_info['nextlvl'] = u' и %.2f%% до следующего' % (100-float(results['exp_progress']))
 else: hero_info['nextlvl'] = u''

 if 'health' in results and 'max_health' in results:
  curh = int(results['health'])
  maxh = int(results['max_health'])
  hero_info['health'] = u', здоров%s на %d%%. ' % (hero_info['gend4'], curh*100/maxh)
 else: hero_info['health'] = u''

 if 'quest_progress' in results: hero_info['questp'] = u' прош%s на %d%%' % (hero_info['gend5'], int(results['quest_progress']))
 else: hero_info['questp'] = u''

 if 'arena_fight' in results:
  if results['arena_fight']: hero_info['arena_fight'] = u''
  else: hero_info['arena_fight'] = u' не'
 else: hero_info['arena_fight'] = u' не'

 if 'diary_last' in results: hero_info['diary_last'] = u'Последняя запись в дневнике: ' + results['diary_last'] 
 else: hero_info['diary_last'] = u''

 if 'distance' in results and 'town_name' in results:
  if results['distance'] == 0: hero_info['town'] = u'Дрыхнет в городе %s.' % results['town_name']
  else: hero_info['town'] = u'Шагает от города %s на расстоянии %d км.' % (results['town_name'], results['distance'])
 else: hero_info['town'] = u''

 #Operative data end

 rep=u'%(hexpired)s %(hname)s - %(halign)s геро%(hgender)s, находящ%(gend1)s под неусыпным надзором бог%(ggender)s %(gname)s%(prana)s. %(guild)s с девизом "%(motto)s". Имеет %(level)d уровень%(nextlvl)s. %(inv)s%(health)sТекущий квест "%(qname)s"%(questp)s. Имеет %(brick)d кирпичей для храма и %(gold)s золотых монет. Храм%(temple)s построен. В настоящее время%(arena_fight)s сражается на арене. %(pinfo)s %(diary_last)s %(town)s' % hero_info

 s.msg(t, rep)

bot.register_cmd_handler(handler_godville_hero, u'.godville')