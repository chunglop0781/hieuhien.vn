# -*- coding: utf-8 -*-

import re
import sys
import time

import xbmc


class player(xbmc.Player):

    def __init__ (self):
        xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "Settings.SetSettingValue", "params": {"setting":"network.usehttpproxy", "value":true}, "id": 1}')
        xbmc.Player.__init__(self)


    def onPlayBackStopped(self):
        xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "Settings.SetSettingValue", "params": {"setting":"network.usehttpproxy", "value":false}, "id": 1}')


    def onPlayBackEnded(self):
        xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "Settings.SetSettingValue", "params": {"setting":"network.usehttpproxy", "value":false}, "id": 1}')

