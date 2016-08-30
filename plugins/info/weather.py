#!/usr/bin/env python
# -*- coding: utf-8 -*-
#    Weather plugin for FreQ bot
#    Copyright (C) 2010 Timur Timirkhanov <timur@timirkhanov.kz>
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import urllib2
from xml.dom.minidom import parseString

dpart = {0: u'Ночь', 1: u'Утро', 2: u'День', 3: u'Вечер'}
dweek = {1: u'воскресенье', 2: u'понедельник', 3: u'вторник', 4: u'среда', 5: u'четверг', 6: u'пятница', 7: u'суббота'}
dcloud = {0: u'Ясно', 1: u'Малооблачно', 2: u'Облачно', 3: u'Пасмурно'}
dprec = {4: u'дождь', 5: u'ливень', 6: u'снег', 7: u'снег', 8: u'гроза', 9: u'нет данных', 10: u'без осадков'}
dpos = {0: u'возможен ', 1: u''}
dpost = {0: u'возможна ', 1: u''}
dwind = {0: u'северный', 1: u'северо-восточный', 2: u'восточный', 3: u'юго-восточный', 4: u'южный', 5: u'юго-западный', 6: u'западный', 7: u'северо-западный'}


def weather(t, s, p):
    if not p:
        s.msg(t, u'город?')
        return
    param = p.lower()
    try:
        base = db.database('weather')
    except:
        s.msg(t, u'Что-то с базой')
        return
    try:
        code = base.query("select code from cities where name='%s'" % (param)).fetchone()[0]
    except:
        s.msg(t, u'Такой город не найден')
        return
    try:
        req = urllib2.Request(u'http://informer.gismeteo.ru/xml/%s_1.xml' % (code))
    except:
        s.msg(t, u'Не могу присоединиться к интернету')
        return
    try:
        r = urllib2.urlopen(req)
    except:
        s.msg(t, u'Не могу получить данные от сервера')
        return
    sr = ''.join(r.readlines())
    try:
        wzdom = parseString(sr)
    except:
        s.msg(t, u'Ошибка парсинга XML: XML поврежден')
        return
    try:
        days = wzdom.getElementsByTagName("FORECAST")
    except:
        s.msg(t, u'Ошибка парсинга XML: смена формата XML')
        return
    swz = u'Погода по г. %s\r\n' % (p)
    
    for day in days:
        sday = day.attributes['day'].value
        smonth = day.attributes['month'].value
        syear = day.attributes['year'].value
        ipart = int(day.attributes['tod'].value)
        iweek = int(day.attributes['weekday'].value)
        spart = dpart[ipart]
        sweek = dweek[iweek]
        phen = day.getElementsByTagName("PHENOMENA")[0]
        icloud = int(phen.attributes['cloudiness'].value)
        scloud = dcloud[icloud]
        iprec = int(phen.attributes['precipitation'].value)
        sprec = dprec[iprec]
        spos = ''
        if iprec >= 4 and iprec < 8:
            ipos = int(phen.attributes['rpower'].value)
            spos = dpos[ipos]
        elif iprec == 8:
            ipos = int(phen.attributes['spower'].value)
            spos = dpost[ipos]
        pres = day.getElementsByTagName("PRESSURE")[0]
        sminpres = pres.attributes['min'].value
        smaxpres = pres.attributes['max'].value
        temp = day.getElementsByTagName("TEMPERATURE")[0]
        smintemp = temp.attributes['min'].value
        smaxtemp = temp.attributes['max'].value
        wind = day.getElementsByTagName("WIND")[0]
        sminwind = wind.attributes['min'].value
        smaxwind = wind.attributes['max'].value
        iwind = int(wind.attributes['direction'].value)
        swind = dwind[iwind]
        relwet = day.getElementsByTagName("RELWET")[0]
        sminrelwet = relwet.attributes['min'].value
        smaxrelwet = relwet.attributes['max'].value
        heat = day.getElementsByTagName("HEAT")[0]
        sminheat = heat.attributes['min'].value
        smaxheat = heat.attributes['max'].value
        swz = swz + u'%s %s.%s.%s, %s\r\n' % (spart, sday, smonth, syear, sweek) + '%s, %s%s\r\n' % (scloud, spos, sprec) + u'Атмосферное давление: %s--%s мм.рт.ст.\r\n' % (sminpres, smaxpres) + u'Температура: %s \u00B0C\u2013%s\u00B0C \r\n' % (smintemp, smaxtemp) + u'Ветер: %s %s\u2013%s м/с\r\n' % (swind, sminwind, smaxwind) + u'Относительная влажность воздуха: %s\u2013%s %%\r\n' % (sminrelwet, smaxrelwet) + u'Теплоощущение: %s \u00B0C\u2013%s\u00B0C \r\n' % (sminheat, smaxheat)
    swz = swz + u'Погода предоставлена www.gismeteo.ru'
    s.msg(t, swz)
bot.register_cmd_handler(weather, u'.weather')