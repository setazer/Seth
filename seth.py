#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Slixmpp: The Slick XMPP Library
    Copyright (C) 2010  Nathanael C. Fritz
    This file is part of Slixmpp.

    See the file LICENSE for copying permission.
"""

import logging
from pluginloader import pluginloader
import slixmpp
# import sys
import sqlite3





class SethBot(slixmpp.ClientXMPP):
    """
    A simple Slixmpp bot that will greets those
    who enter the room, and acknowledge any messages
    that mentions the bot's nickname.
    """

    roles = {'none': 0,
             'visitor': 0,
             'participant': 1,
             'moderator': 4}

    affiliations = {'outcast': 0,
                    'none': 1,
                    'member': 3,
                    'admin': 5,
                    'owner': 7}

    def __init__(self, config):

        slixmpp.ClientXMPP.__init__(self, config.JID, config.PASSWORD)
        self.commands = {}
        self.env = config.env
        self.config = config
        self.db = sqlite3.connect(config.DBNAME)
        self.nick = config.NICK
        self.room_settings = {}
        self.plug = pluginloader(self)
        self.jid_access = {admin: 100 for admin in config.ADMINS}

        # The session_start event will be triggered when
        # the bot establishes its connection with the server
        # and the XML streams are ready for use. We want to
        # listen for this event so that we we can initialize
        # our roster.
        self.add_event_handler("session_start", self.start)

        # The groupchat_message event is triggered whenever a message
        # stanza is received from any chat room. If you also also
        # register a handler for the 'message' event, MUC messages
        # will be processed by both handlers.
        self.add_event_handler("groupchat_message", self.muc_message)

        # The groupchat_presence event is triggered whenever a
        # presence stanza is received from any chat room, including
        # any presences you send yourself. To limit event handling
        # to a single room, use the events muc::room@server::presence,
        # muc::room@server::got_online, or muc::room@server::got_offline.

        self.add_event_handler("message", self.message)

        self.add_event_handler("session_end", self.end)

    def start(self, event):
        """
        Process the session_start event.

        Typical actions for the session_start event are
        requesting the roster and broadcasting an initial
        presence stanza.

        Arguments:
            event -- An empty dictionary. The session_start
                     event does not provide any additional
                     data.
        """
        self.get_roster()
        self.send_presence()


        self.init_settings()
        self.autologin()

    def end(self, event):
        self.save_settings()
        self.db.close()
        # sys.exit(0)

    def autologin(self):
        for room in self.room_settings:
            if self.room_settings[room]['autologin']:
                pwd = self.room_settings[room].get('pwd')
                if pwd:
                    self.plugin['xep_0045'].joinMUC(room,
                                                    self.room_settings[room]['nick'],
                                                    password=pwd,
                                                    wait=True)
                else:
                    self.plugin['xep_0045'].joinMUC(room,
                                                    self.room_settings[room]['nick'],
                                                    wait=True)
                self.room_settings[room]['access'] = {}
                self.add_event_handler("muc::%s::got_online" % room,
                                       self.muc_online)

    def has_command(self, msg, cmd):
        if msg['type'] == 'groupchat':
            bot_nick = self.room_settings[msg['from'].bare.lower()]['nick']
        else:
            bot_nick = self.nick
        if msg['body'].startswith(bot_nick + ': '):
            msg['body'] = msg['body'].replace(bot_nick + ': ', '', 1)
        return msg['body'].startswith(cmd)

    def reply(self, text, msg):
        if msg['type'] == 'groupchat' or msg.__class__ is slixmpp.Presence:
            self.send_message(mto=msg['from'].bare,
                              mbody=text,
                              mtype='groupchat')

        elif msg['type'] in ['normal', 'chat']:
            self.send_message(mto=msg['from'],
                              mbody=text,
                              mtype=msg['type'])
        else:
            logging.log(logging.DEBUG, str(msg))

    def init_settings(self):
        cur = self.db.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS room_settings'
                    ' (id INTEGER PRIMARY KEY, room TEXT, setting TEXT, value TEXT)')
        cur.execute('CREATE TABLE IF NOT EXISTS jid_access'
                    ' (id INTEGER PRIMARY KEY, jid TEXT, access INTEGER)')
        settings = cur.execute('SELECT room, setting, value FROM room_settings')
        for row in settings:
            if not self.room_settings.get(row[0]):
                self.room_settings[row[0]] = {}  # Add room
            self.room_settings[row[0]][row[1]] = row[2]  # Add setting
        jid_access = cur.execute('SELECT jid, access FROM jid_access')
        for row in jid_access:
            self.jid_access[row[0]] = row[1]
        cur.close()

    def save_settings(self):
        cur = self.db.cursor()
        rows = []
        for room in self.room_settings:
            for setting in self.room_settings[room]:
                if not setting == 'access':
                    value = self.room_settings[room][setting]
                    rows.append((room, setting, room, setting, value))
        cur.executemany('INSERT OR REPLACE INTO room_settings VALUES'
                        '(COALESCE((SELECT id FROM room_settings WHERE room=? and setting =?),NULL),?,?,?)', rows)
        rows = []
        for jid in self.jid_access:
            access = self.jid_access[jid]
            rows.append((jid, jid, access))
        cur.executemany('INSERT OR REPLACE INTO jid_access VALUES'
                        '(COALESCE((SELECT id FROM jid_access WHERE jid=?),NULL),?,?)', rows)
        self.db.commit()
        cur.close()


    def isConference(self,jid):
        return jid in self.room_settings


    def muc_message(self, msg):
        # Ignore self messages
        bot_nick = self.room_settings[msg['from'].bare.lower()]['nick']
        if msg['mucnick'] == bot_nick: return

        # Plugin commands handler
        for cmd in self.commands:
            if self.has_command(msg, cmd):
                jid_access = self.room_settings[msg['from'].bare.lower()]['access'][msg['from']]
                if jid_access >= self.commands[cmd]['access']:
                    self.commands[cmd]['handler'](self, msg, cmd)
                else:
                    self.reply('ACCESS DENIED!', msg)

        if bot_nick in msg['body']:
            self.reply("%s: Што!?" % msg['mucnick'], msg)

    def message(self, msg):
        # Anti-self-spam
        if msg['type'] == 'groupchat':
            return
        for cmd in self.commands:
            if self.has_command(msg, cmd):
                if self.isConference(msg['from'].bare):
                    jid_access = self.room_settings[msg['from'].bare]['access'][msg['from']]
                else:
                    jid_access = self.jid_access.get(msg['from'].bare.lower(),0)
                if jid_access >= self.commands[cmd]['access']:
                    self.commands[cmd]['handler'](self, msg, cmd)
                else:
                    self.reply('ACCESS DENIED!', msg)

    def muc_online(self, presence):
        """
        Process a presence stanza from a chat room. In this case,
        presences from users that have just come online are
        handled by sending a welcome message that includes
        the user's nickname and role in the room.

        Arguments:
            presence -- The received presence stanza. See the
                        documentation for the Presence stanza
                        to see how else it may be used.
        """

        room = presence['from'].bare.lower()
        jid = presence['from']
        nick = presence['muc']['nick']
        role = presence['muc']['role']
        affiliation = presence['muc']['affiliation']
        realjid = slixmpp.JID(self.plugin['xep_0045'].getJidProperty(room, nick, 'jid')).bare
        if realjid and realjid in self.jid_access:
            self.room_settings[room]['access'][jid] = self.jid_access[realjid]
        else:
            self.room_settings[room]['access'][jid] = self.roles[role] + self.affiliations[affiliation]
        print('Detected: ',role,affiliation,nick)
        # self.reply("Hello, %s %s %s %s %s" % (role,
        #                                       affiliation,
        #                                       nick, self.room_settings[room]['access'][jid], realjid), presence)

    def register_cmd_handler(self, handler, cmd, access=2):
        self.commands[cmd] = {'handler': handler, 'access': access}
