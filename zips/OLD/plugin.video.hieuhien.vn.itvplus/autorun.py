# -*- coding: utf-8 -*-

import xbmc, xbmcaddon

addon = xbmcaddon.Addon(id='plugin.video.hieuhien.vn.itvplus')

Auto_mode = addon.getSetting('auto_mode')

if Auto_mode == 'true':				
    xbmc.executebuiltin("RunAddon(plugin.video.hieuhien.vn.itvplus)")