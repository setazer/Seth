#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Slixmpp: The Slick XMPP Library
    Copyright (C) 2010  Nathanael C. Fritz
    This file is part of Slixmpp.

    See the file LICENSE for copying permission.
"""

import logging
from config import *
from argparse import ArgumentParser

import slixmpp
import sys


#
# def join_handler(bot, msg, cmd):
#     param = msg['body'][len(cmd):]
#     bot.plugin['xep_0045'].joinMUC(param,
#                                     bot.nick,
#                                     password=ROOM_PWD,
#                                     wait=True)

def say_handler(bot, msg, cmd):
    param = msg['body'][len(cmd):]
    bot.muc_reply(param.lstrip(), msg)


def exec_handler(bot, msg, cmd):
    param = msg['body'][len(cmd):]

    if slixmpp.JID(bot.plugin['xep_0045'].getJidProperty(msg['from'].bare, msg['mucnick'], 'jid')).bare in bot.admins:
        try:
            exec(param.lstrip(), globals(), locals())
        except Exception as e:
            bot.muc_reply(e.args[0], msg)
    else:
        bot.muc_reply('ACCESS DENIED!', msg)


def exit_handler(bot, msg, cmd):
    bot.disconnect()
    sys.exit()


class MUCBot(slixmpp.ClientXMPP):
    """
    A simple Slixmpp bot that will greets those
    who enter the room, and acknowledge any messages
    that mentions the bot's nickname.
    """

    def __init__(self, jid, password, room, nick):
        slixmpp.ClientXMPP.__init__(self, jid, password)
        self.commands = {}
        self.room = room
        self.nick = nick
        self.admins = ADMINS
        self.room_access = {}
        self.jid_access = {}
        for admin in ADMINS:
            self.jid_access[admin] = 100
        self.roles = {'participant': 1,
                      'moderator': 4}

        self.affiliations = {'none': 1,
                             'member': 3,
                             'admin': 5,
                             'owner': 7}
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
        self.add_event_handler("muc::%s::got_online" % self.room,
                               self.muc_online)

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
        self.plugin['xep_0045'].joinMUC(self.room,
                                        self.nick,
                                        password=ROOM_PWD,
                                        wait=True)
        self.room_access[ROOM.lower()] = {}

    def hasCommand(self, msg, cmd):
        if msg['body'].startswith(self.nick + ': '):
            print(msg['body'] + '2' + msg['mucnick'])
            msg['body'] = msg['body'].replace(self.nick + ': ', '', 1)
            print(msg['body'] + '3')
        return msg['body'].startswith(cmd)

    def muc_reply(self, text, msg):
        self.send_message(mto=msg['from'].bare,
                          mbody=text,
                          mtype='groupchat')

    def muc_message(self, msg):
        # Ignore self messages
        if msg['mucnick'] == self.nick: return

        # Plugin commands handler
        for cmd in self.commands:
            if self.hasCommand(msg, cmd):
                jid_access = self.room_access[msg['from'].bare.lower()][msg['from']]
                if jid_access >= self.commands[cmd]['access']:
                    self.commands[cmd]['handler'](self, msg, cmd, )
                else:
                    self.muc_reply('ACCESS DENIED!', msg)

        if self.nick in msg['body']:
            self.muc_reply("%s: Што!?" % msg['mucnick'], msg)

    def message(self, msg):
        pass

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
            self.room_access[room][jid] = self.jid_access[realjid]
        else:
            self.room_access[room][jid] = self.roles[role] + self.affiliations[affiliation]

        self.muc_reply("Hello, %s %s %s %s %s" % (role,
                                                  affiliation,
                                                  nick, self.room_access[room][jid], realjid), presence)

    def register_cmd_handler(self, handler, cmd, access=0):
        self.commands[cmd] = {'handler': handler, 'access': access}


def main():
    # Setup the hasCommand line arguments.
    parser = ArgumentParser()

    # Output verbosity options.
    parser.add_argument("-q", "--quiet", help="set logging to ERROR",
                        action="store_const", dest="loglevel",
                        const=logging.ERROR, default=logging.INFO)
    parser.add_argument("-d", "--debug", help="set logging to DEBUG",
                        action="store_const", dest="loglevel",
                        const=logging.DEBUG, default=logging.INFO)

    args = parser.parse_args()

    # Setup logging.
    logging.basicConfig(level=args.loglevel,
                        format='%(levelname)-8s %(message)s')

    # Setup the MUCBot and register plugins. Note that while plugins may
    # have interdependencies, the order in which you register them does
    # not matter.
    xmpp = MUCBot(JID, PASSWORD, ROOM, NICK)
    xmpp.register_plugin('xep_0030')  # Service Discovery
    xmpp.register_plugin('xep_0045')  # Multi-User Chat
    xmpp.register_plugin('xep_0199')  # XMPP Ping

    xmpp.register_cmd_handler(say_handler, '.say', 4)
    xmpp.register_cmd_handler(exec_handler, '.exec', 50)
    xmpp.register_cmd_handler(exit_handler, '.exit', 11)
    # Connect to the XMPP server and start processing XMPP stanzas.
    xmpp.connect()
    xmpp.process()


if __name__ == '__main__':
    main()
