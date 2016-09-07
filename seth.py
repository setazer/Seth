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
import sys


def join_handler(bot, msg, cmd):
    param = msg['body'][len(cmd):].split()
    if len(param) == 2:
        jid, nick = param[0].split('/')
        bot.plugin['xep_0045'].joinMUC(jid,
                                       nick,
                                       password=param[1],
                                       wait=True)
        bot.room_settings[slixmpp.JID(jid).bare.lower()] = {'access': {}}
        bot.add_event_handler("muc::%s::got_online" % jid,
                              bot.muc_online)


def exec_handler(bot, msg, cmd):
    param = msg['body'][len(cmd):]

    if slixmpp.JID(bot.plugin['xep_0045'].getJidProperty(msg['from'].bare, msg['mucnick'], 'jid')).bare in bot.admins:
        try:
            exec(param.lstrip(), globals(), locals())
        except Exception as e:
            bot.reply(e.args[0], msg)
    else:
        bot.reply('ACCESS DENIED!', msg)


def exit_handler(bot, msg, cmd):
    bot.disconnect()
    sys.exit()


class sethbot(slixmpp.ClientXMPP):
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

        self.register_cmd_handler(exec_handler, '.exec', 50)
        self.register_cmd_handler(exit_handler, '.exit', 11)
        self.register_cmd_handler(join_handler, '.join', 50)

    def hasCommand(self, msg, cmd):
        if msg['body'].startswith(self.nick + ': '):
            msg['body'] = msg['body'].replace(self.nick + ': ', '', 1)
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
        else:  # presence
            logging.log(logging.DEBUG, str(msg))

    def muc_message(self, msg):
        # Ignore self messages
        if msg['mucnick'] == self.nick: return

        # Plugin commands handler
        for cmd in self.commands:
            if self.hasCommand(msg, cmd):
                jid_access = self.room_settings[msg['from'].bare.lower()]['access'][msg['from']]
                if jid_access >= self.commands[cmd]['access']:
                    self.commands[cmd]['handler'](self, msg, cmd)
                else:
                    self.reply('ACCESS DENIED!', msg)

        if self.nick in msg['body']:
            self.reply("%s: Што!?" % msg['mucnick'], msg)

    def message(self, msg):
        # Anti-self-spam
        if msg['type'] == 'groupchat':
            return
        for cmd in self.commands:
            if self.hasCommand(msg, cmd):
                jid_access = self.jid_access[msg['from'].bare.lower()]
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
        self.reply("Hello, %s %s %s %s %s" % (role,
                                              affiliation,
                                              nick, self.room_settings[room]['access'][jid], realjid), presence)

    def register_cmd_handler(self, handler, cmd, access=2):
        self.commands[cmd] = {'handler': handler, 'access': access}
